"""c34 Marangoni rods through PhySim's runner with labworld's correlated noise, at a chosen (dt, grid).

The world is the continuum model; (dt, n) is a discretization of the fixed 128 x 128 world-unit box (dx = 128 / n).
One public tick is 0.05 native time (as at the native resolution), so a tick takes 0.05 / dt native steps.
Devices, sources (INJ_SIGMA = 2 world units) and the noise correlation length are in world units.

Prepared state: the battery's native seed-0 state at native t = 300 (marangoni/out/prep_s0.npz, 19 rods), Fourier-
interpolated to the n x n grid when n != 128 (s clipped at 0, c through log c; both keep their totals); om is the flow of that state (one step on a copy).
"""
import copy, json, sys, time
from pathlib import Path

import numpy as np
from numpy.fft import fft2, ifft2
from scipy import ndimage

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402
from physim.blobround6 import OracleRunner  # noqa: E402
from physim.devices import ProbeDevice  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
W = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
LAB = "/home/user/physim/research/alife"
PREP = Path("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/out")
FIELDS = ("phi", "q1", "q2", "s", "c", "om")      # om: the module's own vorticity output (noise 0, not driven)
DRIVEN = ("phi", "q1", "q2", "s", "c")
NOISE_SD = 0.01                                    # per sqrt(native time)
NOISE_FORM = {"phi": "conserved", "q1": "additive", "q2": "additive", "s": "proportional",
              "c": "proportional", "om": "additive"}
ELL = 2.0                                          # noise correlation length (Gaussian sd), world units
GAINS = {"phi": 0.01, "q1": 0.1, "q2": 0.1, "s": 0.01, "c": 0.01}   # rods_runner envelope result
TICK_NATIVE_T = 0.05
L_BOX = 128.0
PROGRAMS = {"sham": [],
            "surf": [{"t": 5.0, "kind": "inject", "device": 0, "port": 3, "amp": 3.0, "dur": 10.0}]}
TRUTH_SEED, PRED_SEED, PRED2_SEED = 202, 101, 303
TIMES = [float(t) for t in range(1, 51)]
GROUPS = ("device0", "device1", "global")


def world(dt=0.05, n=128, noise=NOISE_SD, noise_corr="default", overrides=None):
    spt = int(round(TICK_NATIVE_T / dt))
    assert abs(spt * dt - TICK_NATIVE_T) < 1e-12
    dx = L_BOX / n
    ports = {f: LW.Port(gain=GAINS[f]) for f in DRIVEN}
    nz = {f: (NOISE_FORM[f], 0.0 if f == "om" else noise) for f in FIELDS}
    corr = {f: ELL for f in DRIVEN} if noise_corr == "default" else dict(noise_corr)
    ov = {"dt": dt, "dx": dx}
    ov.update(overrides or {})
    return LW.LabWorld(path=W, fields=FIELDS, steps_per_tick=spt, native_dt=dt, ports=ports, noise=nz,
                       overrides=ov, dx=dx, sys_path=(LAB,), carry=(), noise_corr=corr)


def fourier_resample(a, n):
    """Band-limited resampling of a periodic square array to n x n (same box)."""
    m = a.shape[0]
    if m == n:
        return a.copy()
    A = np.fft.fftshift(np.fft.fft2(a))
    B = np.zeros((n, n), complex)
    lo = min(m, n)
    cm, cn = m // 2, n // 2
    B[cn - lo // 2: cn + (lo - lo // 2), cn - lo // 2: cn + (lo - lo // 2)] = \
        A[cm - lo // 2: cm + (lo - lo // 2), cm - lo // 2: cm + (lo - lo // 2)]
    return np.fft.ifft2(np.fft.ifftshift(B)).real * (n * n) / (m * m)


def prepared(n=128, dt=0.05):
    z = np.load(PREP / "prep_s0.npz")
    info = json.loads((PREP / "prep_s0.json").read_text())
    m = world(dt=dt, n=n).load()
    s = m.init(0, (n, n))
    for f in DRIVEN:
        a = z[f].astype(np.float64)
        if f == "c":        # positive with sharp ring exclusion: interpolate log c, keep the total
            v = np.exp(fourier_resample(np.log(a), n))
            v *= a.mean() / v.mean()
        elif f == "s":      # non-negative: clip, keep the total
            v = np.maximum(fourier_resample(a, n), 0)
            v *= a.mean() / v.mean()
        else:
            v = fourier_resample(a, n)
        s[f] = v
    s1 = m.step(copy.deepcopy(s))
    s["om"] = s1["om"].copy()
    return s, info


def devices(info, shift=(0.0, 0.0)):
    """Device 0 on the median rod's deepest pixel, device 1 on the largest other rod (world units; native pixel
    centres)."""
    c0 = np.array(info["sites"]["centre"], float) + 0.5 + np.array(shift)
    c1 = np.array(info["sites"]["other"], float) + 0.5 + np.array(shift)
    d0 = ProbeDevice(dev_id=0, lattice="square", n_rings=3, base_ds=3.0, center=c0 % L_BOX, L=L_BOX,
                     secret_rot=0.3, reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(13))
    d1 = ProbeDevice(dev_id=1, lattice="hex", n_rings=3, base_ds=6.0, center=c1 % L_BOX, L=L_BOX,
                     secret_rot=1.1, reflect=False, motion_theta=0.0, motion_reflect=False, node_perm=np.arange(19))
    return [d0, d1]


def nbodies(phi, min_area_wu=6.0, dx=1.0):
    """phi > 0 components (8-connected, periodic) of area >= 6 world units^2."""
    lab, n = ndimage.label(phi > 0, structure=np.ones((3, 3)))
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for i, j in zip(a, b):
            if i and j and i != j:
                lab[lab == j] = i
    ids, areas = np.unique(lab[lab > 0], return_counts=True)
    return int((areas * dx * dx >= min_area_wu).sum())


class Watch:
    """Wraps the stepper: per member, body counts after every stepper call and a final snapshot (first members)."""

    def __init__(self, inner, dx, snap_members=2):
        self.inner, self.dx, self.snap_members = inner, dx, snap_members
        self.members = []

    def __call__(self, sim, n, injections=()):
        if sim["t_step"] == 0:
            self.members.append(dict(bodies=[], snap=None))
        rec = self.members[-1]
        sim = self.inner(sim, n, injections=injections)
        F = sim["F"]
        if not np.isfinite(F).all():
            raise RuntimeError("non-finite")
        rec["bodies"].append((round(sim["t_step"] * 0.02, 2), nbodies(F[0], dx=self.dx)))
        if len(self.members) <= self.snap_members:
            rec["snap"] = np.array(F, dtype=np.float32)
        return sim


def oracle(w, s, devs, watch=True):
    stepper = LW.LabStepper(w, dict(w.aux(s), _grid=s["phi"].shape))
    st = Watch(stepper, w.dx) if watch else stepper
    o = OracleRunner(_template=LW.template(w, s), _devices=devs, _port_perm=np.arange(len(FIELDS)),
                     _adjust_mix=np.eye(3), _stepper=st)
    return o, st


def q(sensors, times):
    return [{"sensor": g, "t": times} for g in sensors]


def readouts(F, devs, dx):
    return {"device0": devs[0].sample(F, dx), "device1": devs[1].sample(F, dx),
            "global": np.stack((F.mean(axis=(1, 2)), F.var(axis=(1, 2))), axis=1)}
