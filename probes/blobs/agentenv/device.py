"""device.py — Track A probe-device layer (W1). EVALUATOR-SIDE code.

Implements the TRACKA_AGENTENV_SPEC measurement v3 PROBE-DEVICE:
  device = rigid lattice patch of k sensor nodes (square|tri|hex, undisclosed
  to agents) centered on a movable point, with co-located center injection,
  2 anonymous motion controls (secret rotated/reflected basis), one dilation
  control, and k x n_ports anonymized scalar streams (bilinear samples).

Barrier rules honored here:
  - agent-facing obs = streams + per-port global mean/var + budget counters
    + channel COUNTS only; no coordinates, no lattice type, no port names.
  - port ids = secret permutation of the na+nc sim fields (per world).
  - node stream order = secret permutation per device (ring structure hidden).
  - evaluator truth (positions, port map, blob lists) only via .truth().

Sim: blobkit 0.3.4 sim_cpu state (init_soup) + a LOCAL verbatim-op-order
stepper (_step_chunk) so control can run at 5tu granularity (the locked
advance() is chunked to CREC=25tu). Parity-gated bitwise in test_device.py.
Injection uses the documented ic/poke stamp machinery (genome.poke) applied
per-substep => a true source term dF/dt += amp * gauss while active.

No locked blobkit files are edited or monkeypatched.
"""
import hashlib
import json
import os

import numpy as np
import scipy.fft as sfft

from blobkit import genome as G
from blobkit.soup import sim_cpu
from blobkit.soup.sim_v1 import blob_list_fast

CTRL_TU = 5.0          # control/sensor cadence (== locked REC grid)
MAX_STEP = 1.5         # max |component| of a motion action, field units
INJ_SIGMA = 2.0        # injection stamp sigma (field units), undisclosed
DIL_BOUNDS = (0.5, 3.0)


# ------------------------------------------------------------------ lattices
def lattice_offsets(lattice, n_rings):
    """Node offsets (k,2) [unit spacing, (dy,dx)] for shells 0..n_rings-1
    (ring 0 = center). Canonical order: by ring, then angle.

    square  : Z^2, L1(diamond) shells        -> n_rings=3: 13 nodes
    squareC : Z^2, Linf(Chebyshev) shells    -> n_rings=3: 25 nodes
    hex     : A2 triangular packing shells   -> n_rings=3: 19 nodes
    tri     : honeycomb (3-coordinated), graph-distance shells
              -> n_rings=3: 1+3+6 = 10 nodes
    """
    R = n_rings - 1
    pts = []
    if lattice in ("square", "squareC"):
        for iy in range(-R, R + 1):
            for ix in range(-R, R + 1):
                r = (abs(iy) + abs(ix)) if lattice == "square" else max(abs(iy), abs(ix))
                if r <= R:
                    pts.append((r, float(iy), float(ix)))
    elif lattice == "hex":
        # A2: v1=(0,1), v2=(sqrt3/2, 1/2); shell = hex ring m
        v1 = np.array([0.0, 1.0])
        v2 = np.array([np.sqrt(3) / 2, 0.5])
        seen = set()
        for a in range(-2 * R, 2 * R + 1):
            for b in range(-2 * R, 2 * R + 1):
                m = max(abs(a), abs(b), abs(a + b))   # hex ring index
                if m <= R and (a, b) not in seen:
                    seen.add((a, b))
                    p = a * v1 + b * v2
                    pts.append((m, p[0], p[1]))
    elif lattice == "tri":
        # honeycomb: sites of a 3-coordinated lattice, shells by graph distance
        # build by BFS from center over honeycomb adjacency
        v1 = np.array([0.0, np.sqrt(3)])
        v2 = np.array([1.5, np.sqrt(3) / 2])
        basis = [np.array([0.0, 0.0]), np.array([1.0, 0.0])]
        sites = {}
        for a in range(-2 * R - 2, 2 * R + 3):
            for b in range(-2 * R - 2, 2 * R + 3):
                for s, off in enumerate(basis):
                    p = a * v1 + b * v2 + off
                    sites[(a, b, s)] = p
        # adjacency: sublattice 0 at (a,b) connects to sublattice 1 at
        # (a,b), (a,b-1), (a-1,b)  [within-cell + two neighbor cells]
        def nbrs(key):
            a, b, s = key
            if s == 0:
                return [(a, b, 1), (a, b - 1, 1), (a - 1, b, 1)]
            return [(a, b, 0), (a, b + 1, 0), (a + 1, b, 0)]
        dist = {(0, 0, 0): 0}
        frontier = [(0, 0, 0)]
        for d in range(1, R + 1):
            nxt = []
            for k in frontier:
                for nb in nbrs(k):
                    if nb in sites and nb not in dist:
                        dist[nb] = d
                        nxt.append(nb)
            frontier = nxt
        for k, d in dist.items():
            p = sites[k]
            pts.append((d, p[0], p[1]))
        # normalize: honeycomb NN distance is 1 (unit spacing) already
    else:
        raise ValueError(f"unknown lattice {lattice!r}")
    # canonical order: ring, then angle, then radius
    def keyf(t):
        r, y, x = t
        ang = np.arctan2(y, x) % (2 * np.pi)
        return (r, round(ang, 9), round(np.hypot(y, x), 9))
    pts.sort(key=keyf)
    return np.array([[y, x] for _, y, x in pts], float)


def true_adjacency(lattice, offs, tol=1e-6):
    """Ground-truth nearest-neighbor adjacency (k,k bool) at unit spacing."""
    k = len(offs)
    d = np.linalg.norm(offs[:, None, :] - offs[None, :, :], axis=2)
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    return d <= dmin + tol


def rot2(theta, reflect=False):
    c, s = np.cos(theta), np.sin(theta)
    Rm = np.array([[c, -s], [s, c]])
    if reflect:
        Rm = Rm @ np.array([[1.0, 0.0], [0.0, -1.0]])
    return Rm


# -------------------------------------------------------------- probe device
class ProbeDevice:
    """One rigid sensor array. All geometry secret; agent sees streams only."""

    def __init__(self, dev_id, lattice, n_rings, base_ds, center, L,
                 secret_rot, reflect, motion_theta, motion_reflect,
                 node_perm, dil_bounds=DIL_BOUNDS):
        self.dev_id = dev_id
        self.lattice = lattice
        self.n_rings = n_rings
        self.base_ds = float(base_ds)
        self.center = np.array(center, float)   # (y, x) world coords
        self.L = float(L)
        self.secret_rot = float(secret_rot)
        self.reflect = bool(reflect)
        self.Rm = rot2(secret_rot, reflect)     # lattice orientation
        self.Bm = rot2(motion_theta, motion_reflect)  # motion basis (cols)
        self.offs = lattice_offsets(lattice, n_rings)  # canonical (k,2)
        self.k = len(self.offs)
        self.node_perm = np.asarray(node_perm, int)    # stream slot -> node
        self.dilation = 1.0
        self.dil_bounds = dil_bounds

    # geometry (evaluator-side)
    def node_positions(self):
        """World coords (k,2) in CANONICAL node order."""
        world = self.center[None, :] + self.dilation * self.base_ds * \
            (self.offs @ self.Rm.T)
        return world % self.L

    # controls (called by WorldEnv with budget already checked)
    def apply_move(self, a):
        a = np.clip(np.asarray(a, float), -MAX_STEP, MAX_STEP)
        d = self.Bm @ a                          # secret basis
        self.center = (self.center + d) % self.L
        return float(np.abs(a).sum())            # cost in control units

    def apply_dilate(self, dgain):
        dgain = float(np.clip(dgain, -1.0, 1.0))
        old = self.dilation
        self.dilation = float(np.clip(self.dilation * np.exp(dgain),
                                      *self.dil_bounds))
        return abs(np.log(self.dilation / old))  # cost = |log change| actual

    def sample(self, fields, dx):
        """Bilinear sample all port fields at node positions.
        fields: (n_ports, N, N) view in PORT order. Returns (n_ports, k)
        in STREAM order (node_perm applied)."""
        pos = self.node_positions()              # canonical order
        vals = bilinear(fields, pos, dx)         # (n_ports, k)
        inv = np.empty_like(self.node_perm)
        inv[self.node_perm] = np.arange(self.k)
        # stream slot j carries node node_perm[j]
        return vals[:, self.node_perm]


def bilinear(fields, pos, dx):
    """Periodic bilinear sampling. fields (nf,N,N); pos (k,2) world (y,x).
    Grid cell centers at (i+0.5)*dx (program convention)."""
    N = fields.shape[-1]
    gy = pos[:, 0] / dx - 0.5
    gx = pos[:, 1] / dx - 0.5
    i0 = np.floor(gy).astype(int)
    j0 = np.floor(gx).astype(int)
    fy = (gy - i0)[None, :]
    fx = (gx - j0)[None, :]
    i0 %= N; j0 %= N
    i1 = (i0 + 1) % N
    j1 = (j0 + 1) % N
    f = fields.astype(np.float32, copy=False)
    v00 = f[:, i0, j0]; v01 = f[:, i0, j1]
    v10 = f[:, i1, j0]; v11 = f[:, i1, j1]
    return (v00 * (1 - fy) * (1 - fx) + v01 * (1 - fy) * fx
            + v10 * fy * (1 - fx) + v11 * fy * fx)


# ------------------------------------------------------- secret world layout
def world_secrets(world_key, n_fields, device_cfgs, L):
    """Deterministic per-world secrets: port perm + device placements/bases.
    world_key: string, e.g. 'p4g2_044|s928|roster1|v0'."""
    h = int(hashlib.sha256(world_key.encode()).hexdigest()[:16], 16)
    rng = np.random.default_rng(h)
    port_perm = rng.permutation(n_fields)        # port p -> field port_perm[p]
    devs = []
    # place devices: first random, later ones 30-45 units away from previous
    centers = []
    for i, cfg in enumerate(device_cfgs):
        if not centers:
            c = rng.uniform(0, L, 2)
        else:
            # 18-30u: spans the perturbation-propagation detectability edge
            # (calibrated on p4g2_044: z~6-8 at 20u, z~0.1 at 35u)
            ang = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(18.0, 30.0)
            c = (centers[-1] + r * np.array([np.sin(ang), np.cos(ang)])) % L
        centers.append(c)
        k = len(lattice_offsets(cfg["lattice"], cfg["n_rings"]))
        devs.append(dict(
            center=c.tolist(),
            secret_rot=float(rng.uniform(0, 2 * np.pi)),
            reflect=bool(rng.integers(2)),
            motion_theta=float(rng.uniform(0, 2 * np.pi)),
            motion_reflect=bool(rng.integers(2)),
            node_perm=rng.permutation(k).tolist(),
        ))
    return dict(port_perm=port_perm.tolist(), devices=devs)


# ------------------------------------------------ local stepper (verbatim ops)
def step_chunk(S, n_steps, injections=None):
    """Advance sim state S by n_steps WITHOUT recording. Op order verbatim
    from blobkit.soup.sim_cpu.advance (parity-gated bitwise in tests).
    injections: list of dicts(field=int, y=float, x=float, amp=float)
    applied as a source term amp*gauss per TIME UNIT via genome.poke."""
    na, N = S["na"], S["N"]
    fdt, rng, workers = S["fdt"], S["rng"], S["workers"]
    F, E = S["F"], S["E"]
    lam, k1, u0f = S["lam"], S["k1"], S["u0f"]
    Wf, Kf, Wid = S["Wf"], S["Kf"], S["Wid"]
    thr_f, sc_f, inv_tau = S["thr_f"], S["sc_f"], S["inv_tau"]
    bilin, tanh_rows = S["bilin"], S["tanh_rows"]
    nsig, noise = S["nsig"], S["noise"]
    dt = S["dt"]
    g = S["g"]; dx = S["dx"]
    injections = injections or []

    for _ in range(n_steps):
        # source injections (perturbation; RNG stream untouched)
        for inj in injections:
            F = G.poke(F, g, inj["field"], inj["x"], inj["y"],
                       inj["amp"] * dt, INJ_SIGMA, dx)
        U = F[:na]; X = F[na:]
        Z = U - u0f
        R = np.empty_like(F)
        np.multiply(U, U, out=R[:na]); R[:na] *= -U
        R[:na] += lam * U; R[:na] += k1
        R[:na] -= np.tensordot(Kf, X, axes=(1, 0))
        for (i, c, c2, coef) in bilin:
            R[i] -= fdt(coef) * X[c] * X[c2]
        Rch = np.tensordot(Wid, Z, axes=(1, 0))
        for c in tanh_rows:
            acc = None
            for a in range(na):
                if Wf[c, a] != 0.0:
                    v = np.tanh(np.clip(Z[a] - thr_f[c], 0, None) / sc_f[c])
                    v *= Wf[c, a]
                    acc = v if acc is None else acc + v
            if acc is not None:
                Rch[c] = acc
        Rch -= X; Rch *= inv_tau
        R[na:] = Rch
        F = F + fdt(dt) * R
        if noise > 0:
            F[:na] += nsig * rng.standard_normal((na, N, N), dtype=fdt) \
                if fdt == np.float32 else \
                nsig * rng.standard_normal((na, N, N))
        F = sfft.irfft2(sfft.rfft2(F, workers=workers) * E, s=(N, N),
                        workers=workers)
        S["t_step"] += 1
        S["F"] = F
    return S


# ----------------------------------------------------------------- world env
class WorldEnv:
    """Agent-facing world wrapper. step(actions) -> obs with ONLY:
    anonymized streams, per-port global mean/var, budget counters, t.

    budgets: dict(sensor=node-tu, motion=control units, injection=|amp|*tu)
    device_cfgs: [dict(lattice=..., n_rings=..., base_ds=...)]
    """

    def __init__(self, genome, seed, device_cfgs, budgets, world_key,
                 L=128.0, workers=3, record_truth=True):
        self.g = genome
        self.seed = seed
        self.L = L
        self.S = sim_cpu.init_soup(genome, L=L, seed=seed, dtype="f32",
                                   workers=workers)
        self.na, self.nc = self.S["na"], self.S["nc"]
        self.nf = self.na + self.nc
        sec = world_secrets(world_key, self.nf, device_cfgs, L)
        self.port_perm = np.asarray(sec["port_perm"], int)
        self.devices = []
        for i, (cfg, ds) in enumerate(zip(device_cfgs, sec["devices"])):
            self.devices.append(ProbeDevice(
                dev_id=i, lattice=cfg["lattice"], n_rings=cfg["n_rings"],
                base_ds=cfg["base_ds"], center=ds["center"], L=L,
                secret_rot=ds["secret_rot"], reflect=ds["reflect"],
                motion_theta=ds["motion_theta"],
                motion_reflect=ds["motion_reflect"],
                node_perm=ds["node_perm"]))
        self.budgets = dict(budgets)
        self.spent = dict(sensor=0.0, motion=0.0, injection=0.0)
        self.t = 0.0
        self.dt_ctrl = CTRL_TU
        self.steps_per_ctrl = int(round(CTRL_TU / self.S["dt"]))
        self._active_inj = []       # dicts(field,y,x,amp,t_end,dev)
        self.record_truth = record_truth
        self.truth_log = dict(t=[], blobs=[], dev_centers=[], dev_dil=[])
        self._record_truth_now()

    # ------------------------------------------------------------- internal
    def _record_truth_now(self):
        if not self.record_truth:
            return
        S = self.S
        bl_all = []
        for i in range(self.na):
            u = np.asarray(S["F"][i], np.float64)
            bl = blob_list_fast(u, S["thr_a"][i], S["dx"], self.L)
            bl_all.append([[b["y"], b["x"], b["area"], b["peak"]] for b in bl])
        self.truth_log["t"].append(self.t)
        self.truth_log["blobs"].append(bl_all)
        self.truth_log["dev_centers"].append(
            [d.center.copy().tolist() for d in self.devices])
        self.truth_log["dev_dil"].append([d.dilation for d in self.devices])

    def _budget_left(self, key):
        return self.budgets.get(key, np.inf) - self.spent[key]

    # --------------------------------------------------------------- public
    @property
    def n_ports(self):
        return self.nf

    def k_total(self):
        return sum(d.k for d in self.devices)

    def step(self, actions=None, read=True):
        """actions: {dev_id: {'move': (a1,a2), 'dilate': g,
                              'inject': (port, amp, dur)}}.
        read=False: skip sensor sampling (no sensor cost, streams=None).
        Advances CTRL_TU. Returns obs dict (anonymized)."""
        actions = actions or {}
        rejected = []
        for di, act in actions.items():
            dev = self.devices[di]
            if "move" in act and act["move"] is not None:
                a = np.clip(np.asarray(act["move"], float),
                            -MAX_STEP, MAX_STEP)
                cost = float(np.abs(a).sum())
                if cost <= self._budget_left("motion") + 1e-9:
                    self.spent["motion"] += dev.apply_move(a)
                else:
                    rejected.append((di, "move"))
            if "dilate" in act and act["dilate"] is not None:
                dg = float(np.clip(act["dilate"], -1.0, 1.0))
                tgt = float(np.clip(dev.dilation * np.exp(dg),
                                    *dev.dil_bounds))
                cost = abs(np.log(tgt / dev.dilation))
                if cost <= self._budget_left("motion") + 1e-9:
                    self.spent["motion"] += dev.apply_dilate(act["dilate"])
                else:
                    rejected.append((di, "dilate"))
            if "inject" in act and act["inject"] is not None:
                port, amp, dur = act["inject"]
                cost = abs(float(amp)) * float(dur)
                if cost <= self._budget_left("injection") + 1e-9:
                    self.spent["injection"] += cost
                    self._active_inj.append(dict(
                        field=int(self.port_perm[int(port)]),
                        dev=di, amp=float(amp),
                        t_end=self.t + float(dur)))
                else:
                    rejected.append((di, "inject"))

        # advance one control interval, applying active injections
        self._active_inj = [j for j in self._active_inj if j["t_end"] > self.t]
        injs = []
        for j in self._active_inj:
            dev = self.devices[j["dev"]]
            injs.append(dict(field=j["field"], y=dev.center[0],
                             x=dev.center[1], amp=j["amp"]))
        step_chunk(self.S, self.steps_per_ctrl, injections=injs)
        self.t += self.dt_ctrl
        self._record_truth_now()

        # observations
        obs = dict(t=self.t, streams={}, global_stats=None, rejected=rejected,
                   budget={k: self._budget_left(k) for k in self.spent})
        fields = np.asarray(self.S["F"])[self.port_perm]   # port order
        gm = fields.mean(axis=(1, 2)).astype(np.float32)
        gv = fields.var(axis=(1, 2)).astype(np.float32)
        obs["global_stats"] = np.stack([gm, gv], axis=1)   # (n_ports, 2)
        sensor_cost = self.k_total() * self.dt_ctrl
        if read and sensor_cost <= self._budget_left("sensor") + 1e-9:
            self.spent["sensor"] += sensor_cost
            for d in self.devices:
                obs["streams"][d.dev_id] = d.sample(fields, self.S["dx"])
        else:
            for d in self.devices:
                obs["streams"][d.dev_id] = np.full(
                    (self.nf, d.k), np.nan, np.float32)
        return obs

    # ----------------------------------------------------- evaluator access
    def truth(self):
        """EVALUATOR-ONLY: secrets + truth log (never shown to agents)."""
        return dict(
            port_perm=self.port_perm.tolist(),
            devices=[dict(dev_id=d.dev_id, lattice=d.lattice,
                          n_rings=d.n_rings, base_ds=d.base_ds,
                          center=d.center.tolist(), dilation=d.dilation,
                          secret_rot=d.secret_rot, reflect=d.reflect,
                          motion_basis=d.Bm.tolist(),
                          node_perm=d.node_perm.tolist(),
                          offsets=d.offs.tolist(),
                          positions=d.node_positions().tolist())
                     for d in self.devices],
            log=self.truth_log)


# ------------------------------------------------------------ cached replay
def run_cached(genome, seed, T, path, L=128.0, workers=3,
               snap_times=(), keep_fields=True):
    """Simulate (world, seed) once with NO devices; store f16 field frames at
    CTRL_TU cadence + truth blob lists + full-precision snapshots (for P3
    branch runs: F f32 + RNG state). Returns metadata dict."""
    S = sim_cpu.init_soup(genome, L=L, seed=seed, dtype="f32", workers=workers)
    na, nc = S["na"], S["nc"]
    nf = na + nc
    n_ctrl = int(round(T / CTRL_TU))
    steps_per = int(round(CTRL_TU / S["dt"]))
    N = S["N"]
    frames = np.empty((n_ctrl + 1, nf, N, N), np.float16) if keep_fields else None
    ts, blobs = [], []
    snaps = {}
    snap_left = sorted(snap_times)

    def rec(i, t):
        if keep_fields:
            frames[i] = np.asarray(S["F"], np.float32).astype(np.float16)
        bl_all = []
        for a in range(na):
            u = np.asarray(S["F"][a], np.float64)
            bl = blob_list_fast(u, S["thr_a"][a], S["dx"], L)
            bl_all.append([[b["y"], b["x"], b["area"], b["peak"]] for b in bl])
        ts.append(t)
        blobs.append(bl_all)

    rec(0, 0.0)
    for i in range(1, n_ctrl + 1):
        t = i * CTRL_TU
        step_chunk(S, steps_per)
        rec(i, t)
        while snap_left and t >= snap_left[0] - 1e-9:
            ts_ = snap_left.pop(0)
            snaps[ts_] = dict(F=np.asarray(S["F"], np.float32).copy(),
                              rng_state=S["rng"].bit_generator.state,
                              t=t)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    meta = dict(world=genome.get("id"), seed=seed, T=T, L=L, N=N, na=na,
                nc=nc, dx=S["dx"], ctrl_tu=CTRL_TU, t=ts)
    np.savez(path,
             frames=frames if keep_fields else np.zeros(0, np.float16),
             meta=json.dumps(meta), blobs=json.dumps(blobs),
             snaps=np.array(list(snaps.keys()), float),
             **{f"snapF_{k:g}": v["F"] for k, v in snaps.items()},
             **{f"snapR_{k:g}": np.frombuffer(
                 json.dumps(v["rng_state"]).encode(), np.uint8)
                for k, v in snaps.items()})
    return meta


class CachedRun:
    """Loads a cached run; supports offline device replay (motion/dilation
    against stored frames — sensors are passive, so replay == live for any
    non-injecting policy) and snapshot restoration for live P3 branches."""

    def __init__(self, path):
        z = np.load(path, allow_pickle=False)
        self.frames = z["frames"]                 # (T+1, nf, N, N) f16
        self.meta = json.loads(str(z["meta"]))
        self.blobs = json.loads(str(z["blobs"]))
        self.snap_times = z["snaps"].tolist()
        self._z = z

    def snapshot_state(self, genome, t_snap, workers=3):
        """Rebuild a live sim state S at t_snap from stored F + RNG state."""
        S = sim_cpu.init_soup(genome, L=self.meta["L"],
                              seed=self.meta["seed"], dtype="f32",
                              workers=workers)
        F = self._z[f"snapF_{t_snap:g}"]
        rs = json.loads(bytes(self._z[f"snapR_{t_snap:g}"]).decode())
        S["F"] = np.array(F, np.float32)
        S["rng"].bit_generator.state = rs
        S["t_step"] = int(round(t_snap / S["dt"]))
        return S

    def fields_at(self, i_ctrl):
        return self.frames[i_ctrl].astype(np.float32)


class ReplayEnv:
    """WorldEnv-compatible interface over a CachedRun (passive policies only:
    move/dilate fine, injection forbidden). Same secrets/anonymization."""

    def __init__(self, cached, genome, device_cfgs, budgets, world_key):
        self.c = cached
        self.L = cached.meta["L"]
        self.dx = cached.meta["dx"]
        self.na, self.nc = cached.meta["na"], cached.meta["nc"]
        self.nf = self.na + self.nc
        sec = world_secrets(world_key, self.nf, device_cfgs, self.L)
        self.port_perm = np.asarray(sec["port_perm"], int)
        self.devices = []
        for i, (cfg, ds) in enumerate(zip(device_cfgs, sec["devices"])):
            self.devices.append(ProbeDevice(
                dev_id=i, lattice=cfg["lattice"], n_rings=cfg["n_rings"],
                base_ds=cfg["base_ds"], center=ds["center"], L=self.L,
                secret_rot=ds["secret_rot"], reflect=ds["reflect"],
                motion_theta=ds["motion_theta"],
                motion_reflect=ds["motion_reflect"],
                node_perm=ds["node_perm"]))
        self.budgets = dict(budgets)
        self.spent = dict(sensor=0.0, motion=0.0, injection=0.0)
        self.i = 0
        self.t = 0.0
        self.dev_center_log = [[d.center.copy().tolist()
                                for d in self.devices]]
        self.dev_dil_log = [[d.dilation for d in self.devices]]

    def _budget_left(self, key):
        return self.budgets.get(key, np.inf) - self.spent[key]

    def k_total(self):
        return sum(d.k for d in self.devices)

    def step(self, actions=None, read=True):
        if self.i >= len(self.c.frames) - 1:
            raise IndexError("cached run exhausted")
        actions = actions or {}
        rejected = []
        for di, act in actions.items():
            dev = self.devices[di]
            if act.get("move") is not None:
                a = np.clip(np.asarray(act["move"], float),
                            -MAX_STEP, MAX_STEP)
                cost = float(np.abs(a).sum())
                if cost <= self._budget_left("motion") + 1e-9:
                    self.spent["motion"] += dev.apply_move(a)
                else:
                    rejected.append((di, "move"))
            if act.get("dilate") is not None:
                dg = float(np.clip(act["dilate"], -1.0, 1.0))
                tgt = float(np.clip(dev.dilation * np.exp(dg),
                                    *dev.dil_bounds))
                cost = abs(np.log(tgt / dev.dilation))
                if cost <= self._budget_left("motion") + 1e-9:
                    self.spent["motion"] += dev.apply_dilate(act["dilate"])
                else:
                    rejected.append((di, "dilate"))
            if act.get("inject") is not None:
                raise RuntimeError("ReplayEnv cannot inject (passive cache)")
        self.i += 1
        self.t = self.i * CTRL_TU
        self.dev_center_log.append([d.center.copy().tolist()
                                    for d in self.devices])
        self.dev_dil_log.append([d.dilation for d in self.devices])
        fields = self.c.fields_at(self.i)[self.port_perm]
        gm = fields.mean(axis=(1, 2)).astype(np.float32)
        gv = fields.var(axis=(1, 2)).astype(np.float32)
        obs = dict(t=self.t, streams={}, rejected=rejected,
                   global_stats=np.stack([gm, gv], axis=1),
                   budget={k: self._budget_left(k) for k in self.spent})
        sensor_cost = self.k_total() * CTRL_TU
        if read and sensor_cost <= self._budget_left("sensor") + 1e-9:
            self.spent["sensor"] += sensor_cost
            for d in self.devices:
                obs["streams"][d.dev_id] = d.sample(fields, self.dx)
        else:
            for d in self.devices:
                obs["streams"][d.dev_id] = np.full(
                    (self.nf, d.k), np.nan, np.float32)
        return obs

    def truth(self):
        return dict(
            port_perm=self.port_perm.tolist(),
            devices=[dict(dev_id=d.dev_id, lattice=d.lattice,
                          n_rings=d.n_rings, base_ds=d.base_ds,
                          center=d.center.tolist(), dilation=d.dilation,
                          secret_rot=d.secret_rot, reflect=d.reflect,
                          motion_basis=d.Bm.tolist(),
                          node_perm=d.node_perm.tolist(),
                          offsets=d.offs.tolist(),
                          positions=d.node_positions().tolist())
                     for d in self.devices],
            blobs=self.c.blobs, t=self.c.meta["t"],
            dev_centers=self.dev_center_log, dev_dil=self.dev_dil_log)
