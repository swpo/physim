"""Design helpers: run a program through the lab oracle while capturing the full fields; track bodies."""
import copy, dataclasses, json, pickle, sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
import fv_observables as OBS
from physim import labworld as LW
from physim.devices import ProbeDevice
sys.path.insert(0, C.LAB)
from labkit import metrics as M

THR = 0.06
DERIVED = (LW.Derived("eat", OBS.eat), LW.Derived("speed", OBS.speed))
ACT = {"om+": 0, "om-": 1, "Y+": 2, "Y-": 3}   # actuator index in common.world's roster


def load_state(path):
    with open(path, "rb") as fh:
        return pickle.load(fh)


def device(i, centre, node_perm=None):
    lattice, ds, rot, k = (("square", 3.0, 0.3, 13), ("hex", 6.0, 1.1, 19))[i]
    return ProbeDevice(dev_id=i, lattice=lattice, n_rings=3, base_ds=ds, center=np.asarray(centre, float),
                       L=128.0, secret_rot=rot, reflect=False, motion_theta=0.0, motion_reflect=False,
                       node_perm=np.arange(k) if node_perm is None else np.asarray(node_perm))


def oracle(state, devices, world=None, **kw):
    world = world or C.world(derived=DERIVED, **kw)
    o = LW.oracle(world, state, copy.deepcopy(devices))
    C.one_worker(o._stepper.module)
    return o


def capture(o, actions, seed=0, T=50.0, every=1.0):
    """One member: the fields (om, Y, eat, speed) at every `every` tu and the global/device readings."""
    frames = []
    st = o._stepper

    def cap(sim, n, injections=()):
        r = st(sim, n, injections)
        frames.append((sim["t_step"] * 0.02, np.asarray(sim["F"], np.float32).copy()))
        return r
    o._stepper = cap
    times = [round(k * every, 6) for k in range(int(round(T / every)) + 1)]
    qs = [dict(sensor="device0", t=times), dict(sensor="device1", t=times), dict(sensor="global", t=times)]
    try:
        res = o.sample_truth(actions, qs, 1, truth_seed=seed)["samples"]
    finally:
        o._stepper = st
    F0 = np.asarray(o._template["F"], np.float32)
    out = {0.0: F0}
    for t, F in frames:
        out[round(t, 6)] = F
    keep = {t: out[t] for t in times if t in out}
    return keep, res


def wrap(d, L=128.0):
    return (d + L / 2) % L - L / 2


def bodies(om, thr=THR):
    lab, n = M.periodic_label(np.abs(om) > thr, True)
    out = []
    yy, xx = np.indices(om.shape)
    for i in range(1, n + 1):
        m = lab == i
        a = int(m.sum())
        if a < 8:
            continue
        # periodic centroid
        cy = (np.angle(np.exp(2j * np.pi * (yy[m] + 0.5) / 128).mean()) / (2 * np.pi) * 128) % 128
        cx = (np.angle(np.exp(2j * np.pi * (xx[m] + 0.5) / 128).mean()) / (2 * np.pi) * 128) % 128
        circ = float(om[m].sum())
        out.append(dict(label=i, area=a, cy=float(cy), cx=float(cx), sign=int(np.sign(circ)), circ=circ,
                        peak=float(np.abs(om[m]).max())))
    return lab, out


def follow(frames, start_yx, thr=THR, min_area=8):
    """Track the body nearest `start_yx` through the frames by overlap; report splits (>=2 overlapping children)."""
    times = sorted(frames)
    lab, bs = bodies(frames[times[0]][0], thr)
    d = [np.hypot(wrap(b["cy"] - start_yx[0]), wrap(b["cx"] - start_yx[1])) for b in bs]
    cur = bs[int(np.argmin(d))]
    mask = lab == cur["label"]
    hist = [dict(t=times[0], n=1, **{k: cur[k] for k in ("area", "cy", "cx", "sign", "circ", "peak")})]
    events = []
    for t in times[1:]:
        om = frames[t][0]
        lab, bs = bodies(om, thr)
        over = [b for b in bs if (mask & (lab == b["label"])).sum() >= 3 and b["area"] >= min_area]
        if not over:
            hist.append(dict(t=t, n=0))
            events.append(dict(t=t, type="vanished"))
            break
        if len(over) >= 2:
            events.append(dict(t=t, type="split", children=[dict(area=b["area"], sign=b["sign"], cy=b["cy"], cx=b["cx"])
                                                            for b in over]))
        big = max(over, key=lambda b: b["area"])
        # keep following the union of overlapping children (a lineage), report their count
        mask = np.zeros_like(mask)
        for b in over:
            mask |= lab == b["label"]
        hist.append(dict(t=t, n=len(over), area=int(mask.sum()), cy=big["cy"], cx=big["cx"], sign=big["sign"],
                         circ=float(om[mask].sum()), peak=float(np.abs(om[mask]).max())))
    return hist, events


def persistent_split(hist, k=3):
    """First time the followed lineage has >=2 bodies for k consecutive frames."""
    run = 0
    for h in hist:
        run = run + 1 if h.get("n", 0) >= 2 else 0
        if run >= k:
            return h["t"] - (k - 1)
    return None
