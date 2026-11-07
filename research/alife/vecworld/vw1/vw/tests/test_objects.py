"""vw.objects: the blob tracker as a pure JAX CoarseGrain.

Synthetic periodic fields exercise every declared rule (wrap-around bodies, fusion, fission, births
with full slots, deaths, fallback, ties, overflow). Where the VW-0 host tracker
(../integrate/lenia_world.Tracker) is present, every tick is also compared with it: slot map, presence,
ages, events, uids and globals exactly, continuous features to 1e-12.
"""
import functools
import os
import sys
from collections import deque
from types import SimpleNamespace

import jax
import jax.numpy as jnp
import numpy as np
import pytest
import scipy.ndimage as ndi

import vw
from vw import objects as OB

VEC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
NF, NS = OB.NF, OB.NS
EV = OB.EVENTS
DISC = [0, NF + 2, NF + 3, NF + 4]          # present, age, event, uid


def host_tracker(shape, K, m_min, sigma=1.0, thr=0.1):
    """The VW-0 numpy tracker on a stand-in level of the given shape, or None if VW-0 is absent."""
    if not os.path.exists(os.path.join(VEC, "integrate", "lenia_world.py")):
        return None
    sys.dont_write_bytecode = True
    for p in ("integrate", "spec", "level0"):
        if os.path.join(VEC, p) not in sys.path:
            sys.path.append(os.path.join(VEC, p))
    import lenia_world as LW
    C, H, W = shape
    l0 = SimpleNamespace(C=C, H=H, W=W, HW=H * W, shape=tuple(shape), screen={})
    return LW.Tracker(l0, K, m_min, blur=sigma, thr=thr)


def bump(H, W, cy, cx, sy, sx=None, amp=1.0):
    sx = sy if sx is None else sx
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - cx + W / 2) % W - W / 2
    return amp * np.exp(-0.5 * (dy / sy) ** 2 - 0.5 * (dx / sx) ** 2)


def field(H, W, bumps, frac=0.3):
    S = np.zeros((H, W))
    for b in bumps:
        S = S + bump(H, W, *b)
    return np.stack([(1 - frac) * S, frac * S])


@functools.lru_cache(maxsize=None)
def compiled(shape, K, m_min, caps=()):
    bt = OB.BlobTracker(shape=shape, K=K, m_min=m_min, sigma=1.0, threshold=0.1, **dict(caps))
    return bt, jax.jit(bt.init_memory), jax.jit(bt.update_memory)


def run(frames, K, m_min, **caps):
    """JAX memories (jit) and host memories (or None) along a sequence of fields."""
    shape = frames[0].shape
    bt, init, upd = compiled(shape, K, m_min, tuple(sorted(caps.items())))
    mj = [np.asarray(init(jnp.asarray(frames[0])))]
    for f in frames[1:]:
        mj.append(np.asarray(upd(jnp.asarray(mj[-1]), jnp.asarray(f))))
    ht = host_tracker(shape, K, m_min)
    mh = None
    if ht is not None:
        mh = [ht.update_one(None, frames[0].ravel())]
        for f in frames[1:]:
            mh.append(ht.update_one(mh[-1], f.ravel()))
    return bt, mj, mh


def check_host(bt, mj, mh):
    if mh is None:
        return
    for t, (a, b) in enumerate(zip(mj, mh)):
        assert a.shape == (bt.n_m,) and b.shape == (bt.n_m_host,)
        da, db = bt.split(a), bt.split(np.asarray(b))
        assert np.array_equal(da["map"], db["map"]), f"slot map differs at tick {t}"
        assert np.array_equal(da["table"][:, DISC], db["table"][:, DISC]), f"discrete slot data differ at tick {t}"
        assert np.array_equal(da["globals"], db["globals"]), f"globals differ at tick {t}"
        np.testing.assert_allclose(da["table"], db["table"], rtol=1e-12, atol=1e-12)


def table(bt, m):
    return bt.split(m)["table"]


# ----------------------------------------------------------------------------- building blocks
def test_blur_is_scipy_gaussian_filter_bit_for_bit():
    rng = np.random.default_rng(0)
    for shape, sigma in (((32, 48), 1.0), ((128, 128), 1.0), ((40, 24), 2.0), ((17, 23), 1.3)):
        S = rng.random(shape) ** 3 * 2.0
        ref = ndi.gaussian_filter(S, sigma, mode="wrap")
        assert np.array_equal(np.asarray(jax.jit(lambda s: OB.gaussian_blur_wrap(s, sigma))(S)), ref)
        assert np.array_equal(np.asarray(OB.gaussian_blur_wrap(jnp.asarray(S), sigma)), ref)
    from scipy.ndimage._filters import _gaussian_kernel1d
    assert np.array_equal(OB.gaussian_kernel1d(1.0), _gaussian_kernel1d(1.0, 0, 4))


def ref_labels(mask):
    """Smallest raster index of each pixel's 8-connected component on the torus (BFS), H*W off."""
    H, W = mask.shape
    out = np.full(H * W, H * W)
    for p in range(H * W):
        if not mask.flat[p] or out[p] < H * W:
            continue
        comp, q = [p], deque([p])
        out[p] = p
        while q:
            y, x = divmod(q.popleft(), W)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    n = ((y + dy) % H) * W + (x + dx) % W
                    if mask.flat[n] and out[n] == H * W:
                        out[n] = 0
                        comp.append(n)
                        q.append(n)
        out[comp] = min(comp)
    return out


def test_periodic_components_on_random_masks():
    rng = np.random.default_rng(1)
    lab = jax.jit(OB.periodic_components)
    for shape in ((16, 20), (33, 17), (24, 24)):
        for dens in (0.2, 0.35, 0.5, 0.6):
            m = rng.random(shape) < dens
            assert np.array_equal(np.asarray(lab(m)), ref_labels(m))
    spiral = np.zeros((21, 21), bool)            # a long path: many rounds of propagation
    spiral[1::4, 1:-1] = True
    spiral[3::8, -2] = True
    spiral[5::8, 1] = True
    assert np.array_equal(np.asarray(lab(spiral)), ref_labels(spiral))


def test_numpy_sum_order():
    rng = np.random.default_rng(2)
    for n in range(1, 13):
        a = rng.standard_normal((50, n)) * 10.0 ** rng.uniform(-3, 3, (50, n))
        pad = np.concatenate([a, np.zeros((50, 12 - n))], 1)
        got = np.asarray(OB.numpy_sum(jnp.asarray(pad), jnp.full((50,), n)))
        assert np.array_equal(got, a.sum(1))


# ----------------------------------------------------------------------------- tracking rules
def test_wraparound_bodies_across_both_edges_and_the_corner():
    H, W = 48, 40
    f = field(H, W, [(0.0, 0.0, 2.5), (0.5, 20.0, 2.0), (24.0, W - 0.5, 2.0, 3.0), (24.0, 20.0, 2.0)])
    bt, mj, mh = run([f, np.roll(f, (1, -2), (1, 2))], K=6, m_min=2.0)
    check_host(bt, mj, mh)
    T0 = table(bt, mj[0])
    assert T0[:, 0].sum() == 4                      # four bodies, none split by an edge
    cy, cx = T0[:4, NF], T0[:4, NF + 1]
    # births by decreasing mass: corner body first (largest), then the left/right body
    np.testing.assert_allclose([cy[0] % H, cx[0] % W], [0.0, 0.0], atol=1e-9)
    assert abs(((cy[1] - 24.0 + H / 2) % H) - H / 2) < 1e-9 and abs(((cx[1] - (W - 0.5)) + W / 2) % W - W / 2) < 1e-9
    T1 = table(bt, mj[1])
    assert np.all(T1[:4, NF + 3] == EV["none"]) and np.all(T1[:4, NF + 2] == 1)
    np.testing.assert_allclose(T1[:4, 11], 1.0, atol=1e-9)        # vy: moved +1 row
    np.testing.assert_allclose(T1[:4, 10], -2.0, atol=1e-9)       # vx: moved -2 columns (min-image)
    smap = bt.split(mj[0])["map"].reshape(H, W)
    assert smap[0, 0] == smap[H - 1, W - 1] == smap[0, W - 1] == smap[H - 1, 0] == 1


def test_fusion_survivor_and_velocity():
    H, W = 48, 64
    frames = [field(H, W, [(24, 14, 2.5, 2.5, 1.0), (24, 40, 2.5, 2.5, 0.7)]),
              field(H, W, [(24, 18, 2.5, 2.5, 1.0), (24, 36, 2.5, 2.5, 0.7)]),
              field(H, W, [(24, 23, 2.5, 2.5, 1.0), (24, 31, 2.5, 2.5, 0.7)])]
    bt, mj, mh = run(frames, K=4, m_min=2.0)
    check_host(bt, mj, mh)
    T1, T2 = table(bt, mj[1]), table(bt, mj[2])
    assert T2[:, 0].sum() == 1
    s = int(np.flatnonzero(T2[:, 0])[0])
    assert T2[s, NF + 3] == EV["fusion"] and T2[1 - s, NF + 3] == EV["fused"]
    mm = T1[:2, 1]
    np.testing.assert_allclose(T2[s, 10], (mm * T1[:2, 10]).sum() / mm.sum(), rtol=1e-12)
    g = bt.split(mj[2])["globals"]
    assert g[3] == 1 and g[2] == 0


def test_fission_parent_and_product():
    H, W = 48, 64
    frames = [field(H, W, [(24, 28, 2.0, 2.0), (24, 34, 2.0, 2.0, 0.8)]),
              field(H, W, [(24, 30, 2.0, 2.0), (24, 36, 2.0, 2.0, 0.8)]),
              field(H, W, [(24, 27, 2.0, 2.0), (24, 41, 2.0, 2.0, 0.8)])]
    bt, mj, mh = run(frames, K=4, m_min=2.0)
    check_host(bt, mj, mh)
    T1, T2 = table(bt, mj[1]), table(bt, mj[2])
    assert T1[0, 0] == 1 and T1[1:, 0].sum() == 0
    assert T2[0, NF + 3] == EV["fission"] and T2[1, NF + 3] == EV["fission"]
    assert T2[0, 10] == T1[0, 10] and T2[1, 10] == T1[0, 10]      # parent keeps, product inherits
    assert T2[0, NF + 4] == T1[0, NF + 4] and T2[1, NF + 4] == 2 and T2[1, NF + 2] == 0
    assert bt.split(mj[2])["globals"][4] == 1


def test_births_with_full_slots_and_freed_slots_wait_a_tick():
    H, W = 48, 48
    b = [(8, 8, 2.0, 2.0, 1.0), (8, 32, 2.0, 2.0, 0.9), (32, 8, 2.0, 2.0, 0.8), (32, 32, 2.0, 2.0, 0.7)]
    frames = [field(H, W, b), field(H, W, b[1:]), field(H, W, b[1:]), field(H, W, b[1:])]
    bt, mj, mh = run(frames, K=2, m_min=2.0)
    check_host(bt, mj, mh)
    T0 = table(bt, mj[0])
    assert list(T0[:, NF + 3]) == [EV["birth"]] * 2 and list(T0[:, NF + 4]) == [1, 2]
    np.testing.assert_allclose(T0[:, NF:NF + 2], [[8, 8], [8, 32]], atol=1e-9)
    smap = bt.split(mj[0])["map"].reshape(H, W)
    assert smap[32, 8] == 0 and smap[32, 32] == 0                  # untracked: no free slot
    T1 = table(bt, mj[1])
    assert T1[0, NF + 3] == EV["death"] and T1[0, 0] == 0 and T1[1, 0] == 1
    assert bt.split(mj[1])["map"].reshape(H, W)[32, 8] == 0        # slot freed this tick is not reused
    T2 = table(bt, mj[2])
    assert T2[0, NF + 3] == EV["birth"] and T2[0, NF + 4] == 3
    np.testing.assert_allclose(T2[0, NF:NF + 2], [32, 8], atol=1e-9)
    assert list(bt.split(mj[3])["globals"]) == [4, 3, 1, 0, 0]


def test_empty_field_and_death():
    H, W = 32, 32
    z = np.zeros((2, H, W))
    frames = [z, field(H, W, [(10, 10, 2.0)]), field(H, W, [(10, 11, 2.0)]), z, z]
    bt, mj, mh = run(frames, K=3, m_min=2.0)
    check_host(bt, mj, mh)
    m0 = mj[0]
    assert np.all(m0[:bt.HW + bt.K * NS] == 0) and list(bt.split(m0)["globals"]) == [1, 0, 0, 0, 0]
    assert table(bt, mj[1])[0, NF + 3] == EV["birth"]
    assert table(bt, mj[3])[0, NF + 3] == EV["death"] and table(bt, mj[3])[0, 0] == 0
    assert np.all(table(bt, mj[4]) == 0)
    assert list(bt.split(mj[4])["globals"]) == [2, 1, 1, 0, 0]


def test_ties_births_overlaps_and_fallback():
    H, W = 48, 96
    # equal masses (integer translates): births by component index (raster order)
    f0 = field(H, W, [(30, 20, 2.0), (10, 60, 2.0)])
    bt, mj, mh = run([f0], K=3, m_min=2.0)
    check_host(bt, mj, mh)
    np.testing.assert_allclose(table(bt, mj[0])[:2, NF:NF + 2], [[10, 60], [30, 20]], atol=1e-9)
    # equal overlaps: a mirror-symmetric fusion; the stable order gives the component to slot 0
    sym = [field(H, W, [(24, 28, 2.5), (24, 52, 2.5)]), field(H, W, [(24, 31, 2.5), (24, 49, 2.5)]),
           field(H, W, [(24, 37, 2.5), (24, 43, 2.5)])]
    bt, mj, mh = run(sym, K=3, m_min=2.0)
    check_host(bt, mj, mh)
    T2 = table(bt, mj[2])
    assert T2[0, NF + 3] == EV["fusion"] and T2[1, NF + 3] == EV["fused"]
    T1 = table(bt, mj[1])
    assert abs(T1[0, 10] - 3.0) < 1e-5 and abs(T1[0, 10] + T1[1, 10]) < 1e-9
    assert abs(T2[0, 10]) < 1e-9                                  # +3 and -3 average to 0
    # fallback: a fast elongated body jumps past its old mask; two equidistant candidates
    run_ = [field(H, W, [(24, 8 + 12 * t, 1.5, 4.0)]) for t in range(3)]
    run_.append(field(H, W, [(21, 44, 0.9), (27, 44, 0.9)]))
    bt, mj, mh = run(run_, K=3, m_min=1.0)
    check_host(bt, mj, mh)
    T3 = table(bt, mj[3])
    assert T3[0, NF + 3] == EV["none"] and T3[0, NF + 4] == 1     # slot 0 continued by fallback
    np.testing.assert_allclose(T3[0, NF:NF + 2], [21, 44], atol=1e-3)     # the first of two equidistant
    assert T3[1, NF + 3] == EV["birth"]


def test_overflow_is_counted_not_silent():
    H, W = 48, 48
    f = field(H, W, [(8, 8, 2.0), (8, 32, 2.0, 2.0, 0.9), (32, 8, 2.0, 2.0, 0.8), (32, 32, 0.6, 0.6, 0.6)])
    bt, mj, _ = run([f, f], K=4, m_min=2.0, max_raw=8, max_kept=8)
    assert list(bt.split(mj[1])["overflow"]) == [0, 0, 4, 3]       # 4 raw components, 3 kept (one too light)
    bt, mj, _ = run([f, f], K=4, m_min=2.0, max_raw=2, max_kept=8)
    assert list(bt.split(mj[1])["overflow"]) == [2, 0, 4, 2]
    assert table(bt, mj[1])[:, 0].sum() == 2
    bt, mj, _ = run([f, f], K=4, m_min=2.0, max_raw=8, max_kept=1)
    assert list(bt.split(mj[1])["overflow"]) == [0, 2, 4, 3]
    assert table(bt, mj[1])[:, 0].sum() == 1


def moving_blobs(seed, H=40, W=48, T=24, n=5):
    rng = np.random.default_rng(seed)
    p = rng.uniform(0, [H, W], (n, 2))
    v = rng.normal(0, 1.5, (n, 2))
    s = rng.uniform(1.2, 3.0, (n, 2))
    a = rng.uniform(0.3, 1.2, n)
    out = []
    for t in range(T):
        live = [(p[i, 0] + t * v[i, 0], p[i, 1] + t * v[i, 1], s[i, 0], s[i, 1], a[i] * (1 + 0.3 * np.sin(t + i)))
                for i in range(n) if not (i == n - 1 and 8 <= t < 14)]
        out.append(field(H, W, live, frac=0.2 + 0.05 * (t % 3)))
    return out


def test_random_moving_blobs_match_host():
    if host_tracker((2, 8, 8), 2, 1.0) is None:
        pytest.skip("VW-0 host tracker not available")
    events = np.zeros(4)
    for seed in range(6):
        bt, mj, mh = run(moving_blobs(seed), K=4, m_min=3.0)
        check_host(bt, mj, mh)
        events += bt.split(mj[-1])["globals"][1:]
    assert np.all(events > 0)                                       # births, deaths, fusions, fissions all seen


# ----------------------------------------------------------------------------- module contract
def test_pure_under_jit_and_vmap():
    frames = np.stack(moving_blobs(7, T=6))
    cg, bt = vw.blob_tracker(frames.shape[1:], K=4, m_min=3.0, sigma=1.0, threshold=0.1)
    assert not cg.differentiable and not cg.opaque and cg.has_memory
    m_e = [bt.init_memory(jnp.asarray(f)) for f in frames]
    m_v = jax.jit(jax.vmap(cg.init_memory))(jnp.asarray(frames))
    assert np.array_equal(np.stack(m_e), m_v)
    u_e = np.stack([bt.update_memory(m_e[i], jnp.asarray(frames[(i + 1) % 6])) for i in range(6)])
    u_v = jax.jit(jax.vmap(cg.update_memory))(m_v, jnp.asarray(np.roll(frames, -1, 0)))
    assert np.array_equal(u_e, u_v)
    assert np.array_equal(np.asarray(jax.jit(cg.update_memory)(m_v[2], frames[3])), u_e[2])
    y = jax.jit(jax.vmap(cg.phi))(jnp.asarray(frames), u_v)
    assert y.shape == (6, 4 * NF)
    jaxpr = str(jax.make_jaxpr(cg.update_memory)(m_v[0], frames[0]))
    assert "callback" not in jaxpr


def test_tracker_in_a_world_matches_its_own_replay():
    H, W = 32, 32

    def init(p, key):
        c = jax.random.uniform(key, (3, 2), minval=0, maxval=H)
        yy, xx = jnp.mgrid[0:H, 0:W]
        S = sum(jnp.exp(-0.5 * (((yy - c[i, 0] + H / 2) % H - H / 2) ** 2 + ((xx - c[i, 1] + W / 2) % W - W / 2) ** 2) / 4.0)
                for i in range(3))
        return jnp.stack([0.7 * S, 0.3 * S])

    def step(p, x, noise, u):
        sh = jax.random.randint(noise.rng(), (2,), -1, 2)
        return jnp.roll(x, (sh[0], sh[1]), (1, 2)) * (1.0 + 0.01 * u.sum())

    lev = vw.Level(init=init, step=step, input_dim=4, differentiable=False, name="drift")
    cg, bt = vw.blob_tracker((2, H, W), K=4, m_min=2.0, sigma=1.0, threshold=0.1)
    w = vw.World(vw.WorldSpec(base=lev, chain=(cg,), outport=vw.ObservePort(noise=0.0)), 0)
    d = w.designer
    _, rec = d.rollout(d.ensemble(3, seed=1), None, T=8, rec=("x", "L1"))
    for b in range(3):
        X = rec["x"][b].reshape(-1, 2, H, W)
        m = bt.init_memory(jnp.asarray(X[0]))
        assert np.array_equal(rec["L1"][b, 0], bt.phi(None, m))
        for t in range(1, 9):
            m = bt.update_memory(m, jnp.asarray(X[t]))
            assert np.array_equal(rec["L1"][b, t], bt.phi(None, m))
    assert not w.spec.opaque and not w.spec.differentiable
    with pytest.raises(vw.NotDifferentiable):
        d.fisher(wrt=None, n=4)
