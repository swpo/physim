"""test_device.py — W1 gates. Run: <venv-python> test_device.py from repo root."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import device as D
from blobkit.soup import sim_cpu

FC = "probes/blobs/l0/deepsearch/v2_analysis/film_candidates"


def load_world(name):
    return json.load(open(f"{FC}/{name}.json"))["genome"]


def t1_lattice_counts():
    for lat, n, want in [("square", 3, 13), ("hex", 3, 19),
                         ("squareC", 3, 25), ("tri", 3, 10),
                         ("square", 2, 5), ("hex", 2, 7)]:
        offs = D.lattice_offsets(lat, n)
        assert len(offs) == want, (lat, n, len(offs), want)
        # ring 0 = center at origin
        assert np.allclose(offs[0], 0.0)
        # unit NN spacing
        adj = D.true_adjacency(lat, offs)
        d = np.linalg.norm(offs[:, None] - offs[None, :], axis=2)
        nn = d[adj]
        assert np.allclose(nn, 1.0, atol=1e-9), (lat, nn.min(), nn.max())
    print("T1 lattice counts + unit NN spacing: PASS")


def t2_bilinear_exact():
    # bilinear sampling of a plane a + b*y + c*x is exact away from wrap
    N, dx = 64, 0.5
    yy = (np.arange(N) + 0.5) * dx
    f = (0.3 + 0.02 * yy[:, None] + 0.05 * yy[None, :]).astype(np.float32)
    pos = np.array([[10.13, 7.77], [20.5, 20.25], [5.0, 30.9]])
    vals = D.bilinear(f[None], pos, dx)[0]
    want = 0.3 + 0.02 * pos[:, 0] + 0.05 * pos[:, 1]
    assert np.allclose(vals, want, atol=1e-5), (vals, want)
    print("T2 bilinear exactness on linear field: PASS")


def t3_step_parity():
    # step_chunk == locked advance() bitwise on p4g2_044 for 25tu
    g = load_world("p4g2_044")
    S1 = sim_cpu.init_soup(g, L=64.0, seed=11, dtype="f32", workers=1)
    S2 = sim_cpu.init_soup(g, L=64.0, seed=11, dtype="f32", workers=1)
    sim_cpu.advance(S1, 25.0)
    D.step_chunk(S2, int(round(25.0 / S2["dt"])))
    assert S1["t_step"] == S2["t_step"]
    same = np.array_equal(np.asarray(S1["F"]), np.asarray(S2["F"]))
    assert same, "step_chunk NOT bitwise identical to locked advance()"
    print("T3 step_chunk bitwise parity vs locked advance (25tu): PASS")


def t4_env_basic():
    g = load_world("p4g2_044")
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0)]
    env = D.WorldEnv(g, seed=11, device_cfgs=cfgs,
                     budgets=dict(sensor=1e9, motion=100.0, injection=50.0),
                     world_key="test|v0", L=64.0, workers=1)
    nf = env.nf
    obs = env.step()
    st = obs["streams"][0]
    assert st.shape == (nf, 19), st.shape
    assert np.isfinite(st).all()
    assert obs["global_stats"].shape == (nf, 2)
    # budgets decrease
    b0 = obs["budget"]["sensor"]
    obs = env.step({0: dict(move=(1.0, 0.0))})
    assert obs["budget"]["sensor"] < b0
    assert obs["budget"]["motion"] < 100.0
    # port perm is a real permutation and applied
    assert sorted(env.port_perm.tolist()) == list(range(nf))
    # obs contains no coordinates / geometry keys
    assert set(obs.keys()) == {"t", "streams", "global_stats", "rejected",
                               "budget"}
    print("T4 WorldEnv basic obs/budget/anonymity: PASS")


def t5_motion_secret_basis():
    g = load_world("p4g2_044")
    cfgs = [dict(lattice="square", n_rings=3, base_ds=3.0)]
    env = D.WorldEnv(g, seed=11, device_cfgs=cfgs,
                     budgets=dict(sensor=1e9, motion=1e9, injection=0.0),
                     world_key="test|v1", L=64.0, workers=1)
    d = env.devices[0]
    c0 = d.center.copy()
    d.apply_move((1.0, 0.0))
    delta = (d.center - c0 + env.L / 2) % env.L - env.L / 2
    # moved by exactly the secret basis column 0
    assert np.allclose(delta, d.Bm @ np.array([1.0, 0.0]), atol=1e-9)
    assert np.hypot(*delta) > 0.99
    # basis is orthonormal
    assert np.allclose(d.Bm @ d.Bm.T, np.eye(2), atol=1e-12)
    print("T5 motion secret orthonormal basis: PASS")


def t6_injection_mass():
    g = load_world("p4g2_044")
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0)]
    kw = dict(device_cfgs=cfgs, world_key="test|v2", L=64.0, workers=1)
    envA = D.WorldEnv(g, seed=13, budgets=dict(sensor=1e9, motion=0,
                                               injection=100.0), **kw)
    envB = D.WorldEnv(g, seed=13, budgets=dict(sensor=1e9, motion=0,
                                               injection=100.0), **kw)
    # find the port that maps to activator 0
    port_u0 = int(np.where(envA.port_perm == 0)[0][0])
    for i in range(4):
        a = {0: dict(inject=(port_u0, 2.0, 5.0))} if i == 0 else None
        oA = envA.step(a)
        oB = envB.step()
    # injection budget spent
    assert abs(envA.spent["injection"] - 10.0) < 1e-6
    dF = np.asarray(envA.S["F"][0], np.float64) - \
        np.asarray(envB.S["F"][0], np.float64)
    assert np.abs(dF).sum() > 1e-3, "injection had no effect on target field"
    # injection over budget is rejected
    oA = envA.step({0: dict(inject=(port_u0, 100.0, 100.0))})
    assert oA["rejected"], "over-budget injection not rejected"
    print("T6 injection: budget accounting + field effect + rejection: PASS")


def t7_replay_equals_live():
    g = load_world("p4g2_044")
    cfgs = [dict(lattice="hex", n_rings=3, base_ds=3.0),
            dict(lattice="square", n_rings=3, base_ds=3.0)]
    budgets = dict(sensor=1e9, motion=1e9, injection=0.0)
    wk = "test|v3"
    path = "/tmp/ae_test_cache.npz"
    D.run_cached(g, seed=17, T=50.0, path=path, L=64.0, workers=1)
    env = D.WorldEnv(g, seed=17, device_cfgs=cfgs, budgets=budgets,
                     world_key=wk, L=64.0, workers=1)
    ren = D.ReplayEnv(D.CachedRun(path), g, cfgs, budgets, wk)
    policy = lambda i: {0: dict(move=(0.5, -0.3)),
                        1: dict(dilate=0.05 if i % 2 else -0.05)}
    errs = []
    for i in range(10):
        o1 = env.step(policy(i))
        o2 = ren.step(policy(i))
        for di in (0, 1):
            e = np.abs(o1["streams"][di] - o2["streams"][di]).max()
            errs.append(e)
    err = max(errs)
    assert err < 2e-2, f"replay deviates from live: {err}"   # f16 cache tol
    print(f"T7 replay==live for passive policy (max err {err:.2e} < 2e-2 f16): PASS")


def t8_snapshot_branch():
    # snapshot restore -> continued run bitwise matches uninterrupted run
    g = load_world("p4g2_044")
    path = "/tmp/ae_test_cache2.npz"
    D.run_cached(g, seed=19, T=50.0, path=path, L=64.0, workers=1,
                 snap_times=(25.0,))
    c = D.CachedRun(path)
    S = c.snapshot_state(g, 25.0, workers=1)
    D.step_chunk(S, int(round(25.0 / S["dt"])))
    F_branch = np.asarray(S["F"], np.float32)
    F_cached16 = c.fields_at(int(round(50.0 / D.CTRL_TU)))
    err = np.abs(F_branch - F_cached16).max()
    assert err < 2e-2, f"snapshot branch mismatch {err}"     # f16 storage tol
    # exact check vs fresh full-precision run
    S2 = sim_cpu.init_soup(g, L=64.0, seed=19, dtype="f32", workers=1)
    D.step_chunk(S2, int(round(50.0 / S2["dt"])))
    exact = np.array_equal(F_branch, np.asarray(S2["F"], np.float32))
    assert exact, "snapshot branch not bitwise vs uninterrupted"
    print("T8 snapshot branch bitwise vs uninterrupted run: PASS")


def t9_secret_determinism():
    s1 = D.world_secrets("w|s1|r", 12, [dict(lattice="hex", n_rings=3)], 128.)
    s2 = D.world_secrets("w|s1|r", 12, [dict(lattice="hex", n_rings=3)], 128.)
    s3 = D.world_secrets("w|s2|r", 12, [dict(lattice="hex", n_rings=3)], 128.)
    assert json.dumps(s1) == json.dumps(s2)
    assert json.dumps(s1) != json.dumps(s3)
    print("T9 world secrets deterministic per key, differ across keys: PASS")


if __name__ == "__main__":
    t1_lattice_counts()
    t2_bilinear_exact()
    t3_step_parity()
    t4_env_basic()
    t5_motion_secret_basis()
    t6_injection_mass()
    t7_replay_equals_live()
    t8_snapshot_branch()
    t9_secret_determinism()
    print("\nALL W1 GATES PASS")
