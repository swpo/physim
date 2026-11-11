"""adapters -- one thin cardlib.Adapter per world (round 6, study cards). No world code is changed; the other
studies' modules are imported.

    foundry(theta, ...)      the two-kind transport neural automaton of round5/foundry (hidden: the weights)
    gliders()                the Flow-Lenia gliders wind world of track2/gliders_exam (hidden: 4 global parameters)
    vortex(H)                fed vortices with heredity, track1/vortex_world (hidden: eps, nu, e)
    membrane()               phase-membrane cells, track1/membrane_world (hidden: 9 rate parameters)
    noise_field()            control: a field redrawn from scratch at every tick
    free_bodies()            control: bodies that move and never interact

The hidden part and its neighbours. `neighbour(theta, eps, d)` moves the hidden part by eps of its DECLARED PRIOR
along direction d (the same direction for every eps):
    foundry    W' = sqrt(1 - eps^2) W + eps W_fresh for the three weight arrays (round 5's weight neighbour; the
               ten scalars are kept); eps = 1 is an independent draw of the weights
    boxes      theta' = theta + eps * (v - centre), v uniform in the declared box; eps = 1 is a prior draw when
               theta is the centre. Boxes: gliders = track2/gliders_exam/results/prior.json (lR, dm_00, ls_00, lh);
               vortex = round5/vortexexam/prior.json (eps, nu, e; the mutation interval is static here);
               membrane, noise field, free bodies = boxes declared in this file (no exam prior exists).
Aiming. `aim(field, rng, aimed)` returns a unit input pattern on k coordinates' worth of the channel: the k
blocks (bumps) holding the most matter when aimed, k random ones when blind; wind channels push all k blocks
along one random direction, scalar channels use one random sign. k = max(1, blocks / 16).
"""
from __future__ import annotations

import dataclasses
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.dirname(os.path.dirname(HERE))
VEC = os.path.dirname(PROG)
VW1 = os.path.join(VEC, "vw1")
PORT = os.path.join(VW1, "port")
ACT = os.path.join(PROG, "track2", "actuation")
GE = os.path.join(PROG, "track2", "gliders_exam")
VWORLD = os.path.join(PROG, "track1", "vortex_world")
MWORLD = os.path.join(PROG, "track1", "membrane_world")
FOUNDRY = os.path.join(PROG, "round5", "foundry")
for _p in (VW1, PORT):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _paths  # noqa: E402,F401  (the port's: must be the first module of that name)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import cardlib as CL  # noqa: E402

assert os.path.realpath(os.path.dirname(vw.__file__)) == os.path.realpath(os.path.join(VW1, "vw")), vw.__file__
assert os.path.realpath(os.path.dirname(_paths.__file__)) == os.path.realpath(PORT), _paths.__file__


def _path(p):
    if p not in sys.path:
        sys.path.append(p)


def _np(tree):
    return jax.tree_util.tree_map(lambda a: np.asarray(a, np.float64), tree)


def block_means(F, G):
    """(Q, H, W) -> (Q, G, G) block means."""
    Q, H, W = F.shape
    return F.reshape(Q, G, H // G, G, W // G).mean((2, 4))


def _topk_pattern(matter, rng, aimed, comps):
    """matter (Gy, Gx) per block; -> unit pattern (comps * Gy * Gx,): k blocks, one direction or sign."""
    n = matter.size
    k = max(1, n // 16)
    idx = np.argsort(matter.ravel())[::-1][:k] if aimed else rng.choice(n, size=k, replace=False)
    p = np.zeros((comps, n))
    if comps == 2:
        phi = rng.uniform(0, 2 * np.pi)
        p[0, idx], p[1, idx] = np.sin(phi), np.cos(phi)
    else:
        p[0, idx] = rng.choice([-1.0, 1.0])
    p = p.ravel()
    return p / np.linalg.norm(p)


def _box_neighbour(names, lo, hi, to_theta, seed):
    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    cen = 0.5 * (lo + hi)

    def nb(theta, eps, d, base=None):
        rng = np.random.default_rng([int(seed), int(d)])
        v = rng.uniform(lo, hi)
        b = cen if base is None else np.asarray(base, float)
        return to_theta(dict(zip(names, b + eps * (v - cen))))
    return nb


# ----------------------------------------------------------------------------- foundry
def foundry(theta=None, index: int = 0, H: int = 64, name: str = "foundry", nb_seed: int = 2026) -> CL.Adapter:
    """The foundry family at H x H (the law is local: the same weights define the world at any size). Block size
    8 px for the view and for the wind at every H."""
    _path(FOUNDRY)
    import tnca as TN
    G = H // 8
    fam = TN.Family(H=H, W=H, GW=G)
    s = (H * H) / 64 ** 2
    trk = TN.tracker(fam, K=min(128, int(24 * s)), max_raw=int(64 * s), max_kept=int(32 * s))

    def neighbour(th, eps, d):
        return TN.perturb_theta({k: np.asarray(v) for k, v in th.items()}, int(nb_seed) + 1000 * (int(d) + 1), int(index),
                                float(eps))

    def aim(field, rng, aimed):
        return _topk_pattern(block_means(field.sum(0)[None], G)[0], rng, aimed, 2)

    return CL.Adapter(
        name=name, family="foundry", init=lambda th, k: TN.init(th, k, fam), tick=lambda th, x, nz, u: TN.tick(th, x, nz, u, fam),
        m=fam.NW, sigma_u=fam.sigma_w, grid=lambda x: TN.block_view(x, G), fine=lambda x: TN.block_view(x, 2 * G),
        trk=trk, trk_field=TN.tracker_field, theta0=None if theta is None else _np(theta), neighbour=neighbour, aim=aim,
        G=G, Hpx=H, burn=50, late_gap=1950, state_batch=32 if H == 64 else 8,
        grid_names=("mean_c0", "mean_c1", "mean_S2"),
        meta=dict(lattice=[2, H, H], substeps_per_tick=fam.NSUB, input="wind 2 x %d x %d, noise std %.2f" % (G, G, fam.sigma_w),
                  hidden="240 weights of the law net (+ 10 scalars, kept by the neighbours)",
                  prior="round5/foundry/tnca.py draw_theta; neighbour = round 5's weight neighbour",
                  views="block means of each kind and of S^2 on 8 px blocks; blob tracker on S / mean(S) > 2"))


def foundry_theta(prior_seed: int, index: int):
    _path(FOUNDRY)
    import tnca as TN
    return TN.draw_theta(int(prior_seed), int(index))


def diffusion_theta(prior_seed: int, index: int):
    """Round 5's control: no affinity, no conversion (diffusion with noise)."""
    th = dict(foundry_theta(prior_seed, index))
    th["beta"] = np.asarray(0.0)
    th["kappa"] = np.asarray(0.0)
    return th


# ----------------------------------------------------------------------------- gliders
def gliders() -> CL.Adapter:
    for p in (ACT, GE):
        _path(p)
    _path(FOUNDRY)
    import gworld as GW
    import flowlenia_jax as FJ
    import phi as PH
    import tnca as TN
    lev0, cfg, _ = FJ.make_level("A_gliders", GW.NOISE_STD)
    _, trv, _ = PH.phi_objects_jax("A_gliders")
    prior = json.load(open(os.path.join(GE, "results", "prior.json")))
    names, lo, hi = prior["names"], prior["lo"], prior["hi"]
    to_theta = lambda d: _np(GW.theta_to_params(d))
    nb = _box_neighbour(names, lo, hi, to_theta, seed=6101)
    sw = GW.SIGMA_W

    def aim(field, rng, aimed):
        return _topk_pattern(block_means(field.sum(0)[None], GW.G)[0], rng, aimed, 2)

    return CL.Adapter(
        name="gliders", family="gliders", init=lambda p, k: lev0.init(p, k), tick=lambda p, A, nz, u: GW.tick(p, A, nz, u, sw),
        m=GW.NW, sigma_u=sw, grid=lambda x: TN.block_view(x, 8), fine=lambda x: TN.block_view(x, 16),
        trk=trv.bt, trk_field=lambda x: x, theta0=_np(GW.theta_to_params({})), neighbour=lambda th, e, d: nb(th, e, d), aim=aim,
        G=8, Hpx=GW.H, burn=GW.BURN, late_gap=600, state_batch=4, grid_names=("mean_c0", "mean_c1", "mean_S2"),
        meta=dict(lattice=[2, GW.H, GW.W], substeps_per_tick=GW.STRIDE, input="wind 2 x 8 x 8, noise std %.2f" % sw,
                  hidden="lR, dm_00, ls_00, lh (4 global parameters of the Flow-Lenia law)",
                  prior="track2/gliders_exam/results/prior.json (uniform box, shrunk by 0.6); theta = the centre",
                  views="Phi_coarse (block means of 2 channels and of S^2, 16 px blocks); the port's blob tracker (12 slots)"))


# ----------------------------------------------------------------------------- fed vortices
def vortex(H: int = 64, n_sub: int = 250, lab_t: float = 300.0) -> CL.Adapter:
    _path(VWORLD)
    import vortex_jax as VJ
    import vortex_world as VW
    af = (128.0 * 128.0) / (H * H)
    cfg = VJ.Config(H=H, W=H, G=H // 16, n_sub=n_sub, mut_dt=50.0 * af, lab_t=lab_t, mut_r=6.0, sigma_a=0.005)
    lev = VJ.make_level(cfg)
    _, trk = VW.phi_vortices(cfg)
    th0 = _np(dict(lev.params))
    pr = json.load(open(os.path.join(PROG, "round5", "vortexexam", "prior.json")))
    keep = [i for i, n in enumerate(pr["names"]) if n in ("eps", "nu", "e")]
    names = [pr["names"][i] for i in keep]
    lo, hi = [pr["lo"][i] for i in keep], [pr["hi"][i] for i in keep]

    def to_theta(d):
        t = dict(th0)
        t.update({k: np.asarray(v, np.float64) for k, v in d.items()})
        return t
    nb = _box_neighbour(names, lo, hi, to_theta, seed=6102)
    G = 8
    Gb = cfg.G

    def fields(x):
        w = jnp.abs(x["om"])
        return jnp.stack([x["om"], w, x["Y"], w * x["b"] / (x["a"] + x["b"] + 1e-3)])

    def aim(field, rng, aimed):
        return _topk_pattern(block_means(field.sum(0)[None], Gb)[0], rng, aimed, 1)

    return CL.Adapter(
        name=f"vortex{H}", family="vortex", init=lev.init, tick=lev.step, m=cfg.m, sigma_u=cfg.sigma_a,
        grid=lambda x: block_means(fields(x), G), fine=lambda x: block_means(fields(x), 2 * G),
        trk=trk, trk_field=VW.kinds_field, theta0=th0, neighbour=lambda th, e, d: nb(th, e, d), aim=aim,
        G=G, Hpx=H, burn=100, late_gap=400, state_batch=8 if H == 64 else 2,
        grid_names=("om", "abs_om", "Y", "abs_om_fb"),
        meta=dict(lattice=[4, H, H], substeps_per_tick=n_sub, input="stirring %d bumps, noise std %.3f" % (cfg.m, cfg.sigma_a),
                  hidden="eps (selection), nu (viscosity), e (eating rate)",
                  prior="round5/vortexexam/prior.json (uniform box; pilot, never an exam); theta = the centre",
                  views="block means of (om, |om|, Y, |om| f_b) on %d px blocks; vortex tracker (%d slots); "
                        "kind share = share of kind-b vortices" % (H // G, trk.K),
                  timeline="labels at t = %.0f (tick %d), mutation every %.0f t after; the card window starts at tick 100"
                           % (lab_t, int(round(lab_t / cfg.tick_time)), cfg.mut_dt)))


# ----------------------------------------------------------------------------- membrane cells
MEMBRANE_BOX = ("r", "a", "th", "F", "b", "dL", "c", "dK", "chi")      # +-10% uniform box, declared here


def membrane(n_sub: int = 20) -> CL.Adapter:
    _path(MWORLD)
    import membrane_jax as MJ
    import membrane_world as MW
    cfg = MJ.Config(n_sub=n_sub)
    lev = MJ.make_level(cfg)
    _, trk = MW.phi_cells(cfg)
    th0 = _np(dict(lev.params))
    cen = np.array([float(th0[k]) for k in MEMBRANE_BOX])

    def to_theta(d):
        t = dict(th0)
        t.update({k: np.asarray(v, np.float64) for k, v in d.items()})
        return t
    nb = _box_neighbour(MEMBRANE_BOX, 0.9 * cen, 1.1 * cen, to_theta, seed=6103)
    G = 8

    def fields(x):
        return jnp.stack([x["S"], x["K"], x["L"], x["phi"]])

    def aim(field, rng, aimed):
        return _topk_pattern(block_means(field.sum(0)[None], cfg.G)[0], rng, aimed, 1)

    return CL.Adapter(
        name="membrane", family="membrane", init=lev.init, tick=lev.step, m=cfg.m, sigma_u=cfg.sigma_a,
        grid=lambda x: block_means(fields(x), G), fine=lambda x: block_means(fields(x), 2 * G),
        trk=trk, trk_field=MW.cells_field, theta0=th0, neighbour=lambda th, e, d: nb(th, e, d), aim=aim,
        G=G, Hpx=cfg.H, burn=200, late_gap=600, state_batch=8, grid_names=("S", "K", "L", "phi"),
        meta=dict(lattice=[4, cfg.H, cfg.W], substeps_per_tick=n_sub, input="substrate %d bumps, noise std %.2f" % (cfg.m, cfg.sigma_a),
                  hidden=", ".join(MEMBRANE_BOX) + " (9 rate parameters)",
                  prior="declared in this study: uniform +-10% box around the default of each; no exam prior exists",
                  views="block means of (S, K, L, phi) on 16 px blocks; cell tracker (%d slots)" % trk.K))


# ----------------------------------------------------------------------------- control: pure noise
def noise_field() -> CL.Adapter:
    """A field redrawn at every tick (no memory, no response to inputs): nothing is predictable past its mean."""
    _path(FOUNDRY)
    import tnca as TN
    fam = TN.FAM

    def draw(th, key):
        g = jax.random.normal(key, (fam.C, fam.H, fam.W))
        g = TN.blur(TN.blur(TN.blur(g, 1), 1), 2)
        g = g / jnp.sqrt(jnp.mean(g * g, axis=(-2, -1), keepdims=True))
        x = jnp.exp(th["contrast"] * g)
        return x / x.mean((-2, -1), keepdims=True) * th["dens"][:, None, None]

    def tick(th, x, nz, u):
        return draw(th, nz.rng()) + 0.0 * x

    th0 = dict(dens=np.array([0.2, 0.2]), contrast=np.asarray(1.0))
    nb = _box_neighbour(("d0", "d1", "contrast"), [0.16, 0.16, 0.8], [0.24, 0.24, 1.2],
                        lambda d: dict(dens=np.array([d["d0"], d["d1"]]), contrast=np.asarray(d["contrast"])), seed=6104)
    return CL.Adapter(
        name="ctl_noise", family="control", init=draw, tick=tick, m=fam.NW, sigma_u=fam.sigma_w,
        grid=lambda x: TN.block_view(x, 8), fine=lambda x: TN.block_view(x, 16), trk=TN.tracker(fam),
        trk_field=TN.tracker_field, theta0=th0, neighbour=lambda th, e, d: nb(th, e, d),
        aim=lambda f, rng, aimed: _topk_pattern(block_means(f.sum(0)[None], 8)[0], rng, aimed, 2),
        G=8, Hpx=64, burn=10, late_gap=200, state_batch=32, grid_names=("mean_c0", "mean_c1", "mean_S2"),
        meta=dict(lattice=[2, 64, 64], substeps_per_tick=1, input="ignored by the law",
                  hidden="densities and contrast of the noise", prior="declared here: +-20% box",
                  views="as the foundry"))


# ----------------------------------------------------------------------------- control: non-interacting bodies
NB_FREE, R_FREE, MASS_FREE, BG_FREE = 8, 2.5, 40.0, 0.02


def free_bodies() -> CL.Adapter:
    """Eight blobs of two kinds; each keeps a preferred speed, turns by its own noise, feels the wind at its
    centre, and never sees another blob (the field is the sum of the blobs)."""
    _path(FOUNDRY)
    import tnca as TN
    fam = TN.FAM
    H = fam.H
    yy, xx = np.mgrid[0:H, 0:H].astype(float)
    kind = np.arange(NB_FREE) % 2

    def init(th, key):
        k1, k2 = jax.random.split(key)
        pos = jax.random.uniform(k1, (NB_FREE, 2)) * H
        ang = jax.random.uniform(k2, (NB_FREE,)) * 2 * jnp.pi
        vel = th["v0"] * jnp.stack([jnp.sin(ang), jnp.cos(ang)], -1)
        return dict(pos=pos, vel=vel)

    def tick(th, x, nz, u):
        wind = TN.wind_field(TN.wind_coeff(nz, u, fam), fam)                 # (2, H, W)
        iy = jnp.floor(x["pos"][:, 0]).astype(jnp.int32) % H
        ix = jnp.floor(x["pos"][:, 1]).astype(jnp.int32) % H
        w = wind[:, iy, ix].T                                                # (NB, 2)
        xi = nz.stream(3).normal((NB_FREE, 2))
        sp = jnp.sqrt((x["vel"] ** 2).sum(-1, keepdims=True) + 1e-12)
        vel = x["vel"] + th["gamma"] * (th["v0"] - sp) * x["vel"] / sp + th["sig"] * xi + th["wq"] * w
        return dict(pos=jnp.mod(x["pos"] + vel, H), vel=vel)

    def render(x):
        dy = jnp.asarray(yy)[None] - x["pos"][:, 0, None, None]
        dx = jnp.asarray(xx)[None] - x["pos"][:, 1, None, None]
        dy = dy - H * jnp.round(dy / H)
        dx = dx - H * jnp.round(dx / H)
        b = MASS_FREE / (2 * jnp.pi * R_FREE ** 2) * jnp.exp(-(dy ** 2 + dx ** 2) / (2 * R_FREE ** 2))   # (NB, H, W)
        k = jnp.asarray(kind)
        return jnp.stack([(b * (k == 0)[:, None, None]).sum(0), (b * (k == 1)[:, None, None]).sum(0)]) + BG_FREE

    th0 = dict(v0=np.asarray(0.6), gamma=np.asarray(0.1), sig=np.asarray(0.05), wq=np.asarray(0.2))
    nb = _box_neighbour(("v0", "gamma", "sig", "wq"), [0.48, 0.08, 0.04, 0.16], [0.72, 0.12, 0.06, 0.24],
                        lambda d: {k: np.asarray(v) for k, v in d.items()}, seed=6105)
    return CL.Adapter(
        name="ctl_freebodies", family="control", init=init, tick=tick, m=fam.NW, sigma_u=fam.sigma_w,
        grid=lambda x: TN.block_view(render(x), 8), fine=lambda x: TN.block_view(render(x), 16), trk=TN.tracker(fam),
        trk_field=lambda x: TN.tracker_field(render(x)), theta0=th0, neighbour=lambda th, e, d: nb(th, e, d),
        aim=lambda f, rng, aimed: _topk_pattern(block_means(f.sum(0)[None], 8)[0], rng, aimed, 2),
        G=8, Hpx=64, burn=20, late_gap=600, state_batch=32, grid_names=("mean_c0", "mean_c1", "mean_S2"),
        meta=dict(lattice=[2, 64, 64], substeps_per_tick=1, input="wind 2 x 8 x 8 (the foundry's), felt at the body's centre",
                  hidden="preferred speed, relaxation rate, turning noise, wind coupling", prior="declared here: +-20% box",
                  views="as the foundry, on the rendered field"))


def with_theta(ad: CL.Adapter, theta, name: str, **kw) -> CL.Adapter:
    return dataclasses.replace(ad, theta0=_np(theta), name=name, **kw)
