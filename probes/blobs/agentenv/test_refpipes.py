"""test_refpipes.py — W2 gates on a SYNTHETIC controlled world (fast, exact
truth). Pipeline logic is gated here; real-sim performance is measured by
adequacy.py. Run: <venv-python> probes/blobs/agentenv/test_refpipes.py"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import device as D
import refpipes as R


# ------------------------------------------------------------- synthetic env
class SynthEnv:
    """WorldEnv-compatible synthetic world: analytic ports sampled at device
    nodes through the SAME anonymization path (secret rot, node perm, secret
    motion basis). Ports: 0..2 informative (bumps+GRF), 3 dead, 4 white."""

    def __init__(self, device_cfgs, world_key, L=64.0, seed=0,
                 bump_amp=2.0, grf_amp=0.15, bump_speed=(0.10, 0.06),
                 n_bumps=3, sig_bump=4.0):
        self.L = L
        self.rng = np.random.default_rng(seed)
        self.nf = 5
        sec = D.world_secrets(world_key, self.nf, device_cfgs, L)
        self.port_perm = np.asarray(sec["port_perm"], int)
        self.devices = []
        for i, (cfg, ds) in enumerate(zip(device_cfgs, sec["devices"])):
            self.devices.append(D.ProbeDevice(
                dev_id=i, lattice=cfg["lattice"], n_rings=cfg["n_rings"],
                base_ds=cfg["base_ds"], center=ds["center"], L=L,
                secret_rot=ds["secret_rot"], reflect=ds["reflect"],
                motion_theta=ds["motion_theta"],
                motion_reflect=ds["motion_reflect"],
                node_perm=ds["node_perm"]))
        self.t = 0.0
        self.bumps = [self.rng.uniform(0, L, 2) for _ in range(n_bumps)]
        self.bv = [np.array(bump_speed) * self.rng.choice([-1, 1], 2)
                   for _ in range(n_bumps)]
        self.bump_amp, self.grf_amp, self.sig = bump_amp, grf_amp, sig_bump
        # GRF: random fourier modes with OU coefficients, per informative port
        self.nm = 24
        self.kvec = {}
        self.ph = {}
        self.a = {}
        self.tau = {0: 8.0, 1: 20.0, 2: 40.0}
        for p in range(3):
            lam = self.rng.uniform(14, 36, self.nm)
            ang = self.rng.uniform(0, 2 * np.pi, self.nm)
            self.kvec[p] = (2 * np.pi / lam)[:, None] * \
                np.stack([np.sin(ang), np.cos(ang)], 1)
            self.ph[p] = self.rng.uniform(0, 2 * np.pi, self.nm)
            self.a[p] = self.rng.standard_normal(self.nm)
        self.budgets = dict(sensor=np.inf, motion=np.inf, injection=np.inf)
        self.spent = dict(sensor=0.0, motion=0.0, injection=0.0)

    def field_vals(self, p_field, pos):
        """Analytic field p at positions (k,2)."""
        if p_field == 3:
            return np.full(len(pos), 0.7)
        if p_field == 4:
            return 0.5 * self.rng.standard_normal(len(pos))
        v = np.zeros(len(pos))
        wb = [1.0, 0.7, 0.4][p_field]
        for c in self.bumps:
            d = (pos - c + self.L / 2) % self.L - self.L / 2
            v += wb * self.bump_amp * np.exp(-(d ** 2).sum(1)
                                             / (2 * self.sig ** 2))
        K = self.kvec[p_field]
        phase = pos @ K.T + self.ph[p_field]
        v += self.grf_amp * (np.cos(phase) @ self.a[p_field]) / np.sqrt(self.nm)
        return v

    def _advance(self, dt=5.0):
        self.t += dt
        for j in range(len(self.bumps)):
            self.bumps[j] = (self.bumps[j] + self.bv[j] * dt) % self.L
        for p in range(3):
            th = np.exp(-dt / self.tau[p])
            self.a[p] = th * self.a[p] + np.sqrt(1 - th ** 2) * \
                self.rng.standard_normal(self.nm)

    def step(self, actions=None, read=True):
        actions = actions or {}
        for di, act in actions.items():
            dev = self.devices[di]
            if act.get("move") is not None:
                self.spent["motion"] += dev.apply_move(act["move"])
            if act.get("dilate") is not None:
                self.spent["motion"] += dev.apply_dilate(act["dilate"])
        self._advance()
        obs = dict(t=self.t, streams={}, rejected=[],
                   budget=dict(self.spent),
                   global_stats=np.zeros((self.nf, 2), np.float32))
        for d in self.devices:
            if read:
                pos = d.node_positions()
                vals = np.stack([self.field_vals(pf, pos)
                                 for pf in self.port_perm])
                obs["streams"][d.dev_id] = vals[:, d.node_perm].astype(
                    np.float32)
                self.spent["sensor"] += d.k * 5.0
            else:
                obs["streams"][d.dev_id] = np.full(
                    (self.nf, d.k), np.nan, np.float32)
        return obs

    def truth_positions(self, di):
        d = self.devices[di]
        return d.node_positions()[d.node_perm]      # stream order


def procrustes_similarity(P, X):
    """Best X ~ s*(P@Rt)+t. Returns (s, Rt, t, corr)."""
    Pc = P - P.mean(0)
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Pc.T @ Xc)
    Rt = U @ Vt
    s = S.sum() / max((Pc ** 2).sum(), 1e-12)
    fit = s * Pc @ Rt
    num = (fit * Xc).sum()
    den = np.sqrt((fit ** 2).sum() * (Xc ** 2).sum())
    return s, Rt, X.mean(0) - s * P.mean(0) @ Rt, num / max(den, 1e-12)


def collect_passive(env, n_reads, dev_ids=(0,)):
    hist = {d: R.History() for d in dev_ids}
    for _ in range(n_reads):
        obs = env.step({}, read=True)
        for d in dev_ids:
            hist[d].add(obs)
    return hist


def g1_geometry():
    ok_all = True
    for lat, want_k in [("hex", 19), ("square", 13)]:
        cfgs = [dict(lattice=lat, n_rings=3, base_ds=3.0)]
        env = SynthEnv(cfgs, world_key=f"synth|{lat}", seed=3)
        hist = collect_passive(env, 300)[0]
        r1 = R.r1_geometry(env, hist, 0)
        assert r1["ok"]
        dev = env.devices[0]
        # truth in STREAM order
        P = dev.offs[dev.node_perm] * dev.base_ds
        adj_true = D.true_adjacency(lat, dev.offs)[
            np.ix_(dev.node_perm, dev.node_perm)]
        A = r1["adj"]
        tp = (A & adj_true).sum()
        f1 = 2 * tp / max(A.sum() + adj_true.sum(), 1)
        s, Rt, tvec, corr = procrustes_similarity(P, r1["X"])
        print(f"  G1[{lat}]: lattice={r1['lattice']} adjF1={f1:.3f} "
              f"embed corr={corr:.4f} center_stream={r1['center']} "
              f"(true center stream={list(dev.node_perm).index(0)})")
        ok = (r1["lattice"] == lat) and f1 >= 0.85 and corr >= 0.97
        ok_all &= ok
    assert ok_all, "G1 failed"
    print("G1 geometry bootstrap (hex+square): PASS")


def g2_motion_basis():
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0)]
    env = SynthEnv(cfgs, world_key="synth|motion", seed=5, bump_speed=(0.02, 0.01))
    hist = collect_passive(env, 300)[0]
    r1 = R.r1_geometry(env, hist, 0)
    # park a bump at patch edge so calibration has signal (seek phase would
    # find one anyway; this keeps the unit test fast + deterministic)
    env.bumps[0] = (env.devices[0].center + np.array([3.0, 2.0])) % env.L
    B_emb, qual, spend = R.r1_motion_probe(env, r1, 0, hist=hist)
    assert B_emb is not None, "motion probe failed"
    dev = env.devices[0]
    P = dev.offs[dev.node_perm] * dev.base_ds
    s, Rt, tvec, corr = procrustes_similarity(P, r1["X"])
    # world disp d shows up in embedding as s * Rt.T @ (Rm.T @ d):
    # node world pos = c + Rm @ p_canon; X ~ s * Rt.T @ p_canon
    B_true = s * Rt.T @ dev.Rm.T @ dev.Bm
    angs = []
    for c in range(2):
        v1, v2 = B_emb[:, c], B_true[:, c]
        ca = v1 @ v2 / max(np.linalg.norm(v1) * np.linalg.norm(v2), 1e-12)
        angs.append(np.degrees(np.arccos(np.clip(ca, -1, 1))))
    # scale consistency: |B_emb| columns should match |B_true| columns
    scl = [np.linalg.norm(B_emb[:, c]) / np.linalg.norm(B_true[:, c])
           for c in range(2)]
    print(f"  G2: axis angle errors {angs[0]:.1f} deg / {angs[1]:.1f} deg, "
          f"scale ratios {scl[0]:.2f}/{scl[1]:.2f}, qual={qual:.2f}, "
          f"spend={spend}")
    assert max(angs) < 25.0, f"motion basis angle error {angs}"
    assert all(0.5 < r < 2.0 for r in scl), f"scale ratios {scl}"
    print("G2 motion basis recovery: PASS")


def g3_particulate():
    # particulate world
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0)]
    env = SynthEnv(cfgs, world_key="synth|part", seed=7,
                   bump_amp=2.0, grf_amp=0.10, n_bumps=4)
    hist = collect_passive(env, 300)[0]
    r1 = R.r1_geometry(env, hist, 0)
    r2 = R.r2_particulate(hist, r1, 0)
    # smooth world (no bumps)
    env2 = SynthEnv(cfgs, world_key="synth|smooth", seed=9,
                    bump_amp=0.0, grf_amp=0.5)
    hist2 = collect_passive(env2, 300)[0]
    r1b = R.r1_geometry(env2, hist2, 0)
    r2b = R.r2_particulate(hist2, r1b if r1b.get("ok") else dict(ok=True, center=0), 0)
    print(f"  G3: particulate world verdict={r2['particulate']} "
          f"(bim={r2['bim'].max():.2f} fano={r2['fano']:.1f}); "
          f"smooth world verdict={r2b['particulate']} "
          f"(bim={r2b['bim'].max():.2f} fano={r2b['fano']:.1f})")
    assert r2["particulate"] and not r2b["particulate"]
    # size scan: park a bump right at the device and scan
    env3 = SynthEnv(cfgs, world_key="synth|size", seed=11,
                    bump_amp=2.0, grf_amp=0.03, n_bumps=1,
                    bump_speed=(0.0, 0.0), sig_bump=4.0)
    env3.bumps[0] = env3.devices[0].center.copy()
    hist3 = collect_passive(env3, 120)[0]
    r13 = R.r1_geometry(env3, hist3, 0)
    r23 = R.r2_particulate(hist3, r13, 0)
    scan = R.r2_size_scan(env3, r13, r23, 0)
    assert scan["ok"], scan
    r_est = scan["r_est_ds"] * env3.devices[0].base_ds
    r_true = 4.0 * np.sqrt(2 * np.log(2))     # half-max radius of the bump
    ratio = r_est / r_true
    print(f"  G3 size: est={r_est:.2f}u true={r_true:.2f}u ratio={ratio:.2f} "
          f"({scan['n_prof']} profiles)")
    assert 0.55 < ratio < 1.8, ratio
    print("G3 particulateness + size scan: PASS")


def g4_tracking():
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0)]
    env = SynthEnv(cfgs, world_key="synth|track", seed=13,
                   bump_amp=2.0, grf_amp=0.05, n_bumps=1,
                   bump_speed=(0.10, 0.06), sig_bump=4.0)
    # start bump near the device so acquisition is immediate
    env.bumps[0] = (env.devices[0].center + np.array([2.0, -1.0])) % env.L
    hist = collect_passive(env, 250)[0]
    r1 = R.r1_geometry(env, hist, 0)
    # bump has been drifting during passive phase; move it back near device
    env.bumps[0] = (env.devices[0].center + np.array([-2.0, 1.5])) % env.L
    r2 = R.r2_particulate(hist, r1, 0)
    B_emb, qual, spend = R.r1_motion_probe(env, r1, 0)
    assert B_emb is not None
    env.bumps[0] = (env.devices[0].center + np.array([1.0, 1.0])) % env.L
    log = R.r3_track(env, r1, r2, B_emb, 0, n_steps=150, duty=1.0,
                     excursion_cap=1e9)
    # truth: distance device center to bump over the tracking window
    d_end = np.linalg.norm((env.devices[0].center - env.bumps[0]
                            + env.L / 2) % env.L - env.L / 2)
    locked = [b for _, b in log["locked_read"]]
    frac2 = np.mean(locked[len(locked) // 2:])   # second half (post-acquire)
    print(f"  G4: locked-read frac (2nd half)={frac2:.2f} "
          f"end distance={d_end:.2f}u motion spend={log['spend_motion']:.0f}")
    assert frac2 > 0.6 and d_end < 5.0
    print("G4 closed-loop tracking on drifting bump: PASS")


def g5_p1():
    rng = np.random.default_rng(0)
    # AR(2) process per channel
    T, C = 400, 6
    a1, a2 = 1.5, -0.6
    S = np.zeros((T, C))
    e = 0.3 * rng.standard_normal((T, C))
    for t in range(2, T):
        S[t] = a1 * S[t - 1] + a2 * S[t - 2] + e[t]
    hist = R.History()
    class FakeObs(dict):
        pass
    for i in range(T):
        hist.t.append((i + 1) * 5.0)
        hist.streams.append({0: S[i].reshape(2, 3)})
        hist.glob.append(np.zeros((2, 2)))
    H = [50.0, 100.0]
    pers = R.p1_persistence(hist, 0, H)
    ar2 = R.p1_ar2(hist, 0, H)
    # score on truth: simulate 40 more steps
    S2 = S.copy().tolist()
    for t in range(40):
        S2.append((a1 * np.array(S2[-1]) + a2 * np.array(S2[-2])
                   + 0.3 * rng.standard_normal(C)).tolist())
    S2 = np.array(S2)
    for Hh, nst in [(50.0, 10), (100.0, 20)]:
        y = S2[T - 1 + nst]
        cp = R.gauss_crps(*pers[Hh], y).mean()
        ca = R.gauss_crps(*ar2[Hh], y).mean()
        print(f"  G5 H={Hh:.0f}: CRPS pers={cp:.3f} ar2={ca:.3f}")
    assert np.isfinite(cp) and np.isfinite(ca)
    print("G5 P1 forecast machinery: PASS")


def g6_p2():
    rng = np.random.default_rng(1)
    T, k = 400, 19
    A = 0.1 * rng.standard_normal((T, k))
    # events: every ~20 frames a burst crossing on some nodes
    for t in range(10, T, 18):
        A[t:t + 3, rng.integers(0, k, 4)] += 2.0
    hist = R.History()
    for i in range(T):
        hist.t.append((i + 1) * 5.0)
        hist.streams.append({0: A[i].reshape(1, k)})
        hist.glob.append(np.zeros((1, 2)))
    out = R.p2_forecast(hist, 0, 0, 1.0, win_tu=50.0, n_win=10, duty=1.0)
    assert all(np.isfinite(v).all() for v in out.values())
    print(f"  G6 rates: pers={out['persistence'][0]:.1f} "
          f"mean={out['mean'][0]:.1f} informed[0]={out['informed'][0]:.1f}")
    print("G6 P2 event-rate machinery: PASS")


def g7_p3():
    rng = np.random.default_rng(2)
    T, nf, k = 20, 3, 13
    base = np.zeros((T, nf, k))
    resp_shape = np.exp(-0.5 * ((np.arange(T) - 8.0) / 3.0) ** 2)[:, None, None]
    kernel = rng.standard_normal((1, nf, k))
    calib = []
    for amp in (1.0, 2.0):
        r_ = base + amp * resp_shape * kernel
        r_[3] = np.nan     # a missing read
        calib.append(dict(amp=amp, dur=10.0, resp=r_))
    pred = R.p3_template_predict(calib, dict(amp=3.0, dur=10.0), T, k, nf)
    true = base + 3.0 * resp_shape * kernel
    err = np.abs(pred[5:] - true[5:]).max() / np.abs(true).max()
    print(f"  G7 template scaling rel err={err:.3f}")
    assert err < 0.05
    print("G7 P3 template predictor: PASS")


if __name__ == "__main__":
    g1_geometry()
    g2_motion_basis()
    g3_particulate()
    g4_tracking()
    g5_p1()
    g6_p2()
    g7_p3()
    print("\nALL W2 GATES PASS")
