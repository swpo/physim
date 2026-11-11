"""xlaw -- the law switch of study A (round 6, dials): round 5's ladder harness with one hidden term.

The hidden law is the designer's `defect_gliders/dlaw.tick` with only the stress-conversion strength live:
    q = {g: 0, xw: p["xw"], m: 0, x: 0, t: 0},  threshold W0 = 0.12 and ramp DW = 0.05 (dlaw's constants).
The strength rides in the parameter pytree as p["xw"] (a traced scalar per member), so ONE compiled program
runs eta = 0 and eta = 4, and the public law is the same program at p["xw"] = 0. With xw = 0 the tick is
bitwise equal to gworld.tick on CPU (check_a.py; on a GPU the scatter-add of the reintegration is not
bit-deterministic, so the job measures the one-tick difference instead).

Pieces (nothing in vw, track2, round4, round5 or defect_gliders is changed; they are imported):
  xtick            dlaw.tick behind gworld.tick's signature
  xparams          gworld.theta_to_params + {"xw": eta}
  build_world_x    sbi_lib.build_world with the hidden law as level 0 (Lab and exams)
  XRunner          sbi_lib.VRunner with xtick (the true-form training family)
  sim_episodes_x   ladder_lib.sim_episodes with a per-member eta
  one_tick_check   the zero point of the switch at any batch size, on the current backend
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
DIALS = os.path.dirname(HERE)
PROG = os.path.dirname(os.path.dirname(DIALS))
VEC = os.path.dirname(PROG)
PORT = os.path.join(VEC, "vw1", "port")
_DIRS = [os.path.join(DIALS, "defect_gliders"), os.path.join(PROG, "round5", "ladder"),
         os.path.join(PROG, "round4", "sbi"), os.path.join(PROG, "track2", "gliders_exam"),
         os.path.join(PROG, "track2", "actuation"), PORT]
for _p in _DIRS:
    if _p not in sys.path:
        sys.path.insert(0, _p)
# gworld.py and wind.py insert fixed /home/user/evalwork paths in front of sys.path. Importing the port's
# modules first pins this checkout's copies (a missing request path then fails here, not on a rented machine).
import _paths  # noqa: E402,F401
import vw  # noqa: E402
import flowlenia_jax as FJ  # noqa: E402
import phi as PH  # noqa: E402
import aworld  # noqa: E402,F401
import wind  # noqa: E402,F401
import ladder_lib as LL  # noqa: E402
import ladder_net as NN  # noqa: E402
import dlaw as DL  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.core import Noise  # noqa: E402
from vw.harness import program_dense  # noqa: E402

SL, GW, PL = LL.SL, LL.GW, LL.PL
SIG, NW, NC, NO, G = LL.SIG, LL.NW, LL.NC, LL.NO, LL.G
N_OBS = NC + NO
HH, WW = GW.H, GW.W
W0, DW, KXW = DL.W0, DL.DW, DL.KXW


def module_files():
    """Where the imported study modules came from (the job asserts they all sit under one checkout)."""
    names = ["vw", "_paths", "flowlenia_jax", "phi", "aworld", "wind", "gworld", "pilot", "sbi_lib", "ladder_lib",
             "ladder_net", "dlaw", "xlaw"]
    return {n: os.path.abspath(getattr(sys.modules[n], "__file__", "?")) for n in names if n in sys.modules}


def assert_one_checkout():
    bad = {n: f for n, f in module_files().items() if not f.startswith(VEC + os.sep)}
    if bad:
        raise RuntimeError(f"modules imported from outside {VEC}: {bad}")


# ----------------------------------------------------------------------------- the law
def xtick(p, A, nz, u_w, sigma_w):
    """One tick of the hidden world, gworld.tick's signature. p carries 'xw' (the dial eta)."""
    z = jnp.zeros((), A.dtype)
    q = {"g": z, "xw": p["xw"], "m": z, "x": z, "t": z}
    A2, _ = DL.tick(p, q, jnp.zeros((2, HH, WW), A.dtype), A, jnp.zeros((HH, WW), A.dtype), nz, u_w, sigma_w)
    return A2


def xparams(names, theta, eta) -> dict:
    """Parameter pytree of one hidden world: round 5's parameters + the strength of the hidden term."""
    p = dict(GW.theta_to_params(dict(zip(names, map(float, theta)))))
    p["xw"] = jnp.asarray(float(eta))
    return p


def level_x(params):
    lev0, _, _ = FJ.make_level("A_gliders", GW.NOISE_STD)

    def step(p, A, nz, u):
        return xtick(p, A, nz, u, SIG)
    return vw.Level(init=lev0.init, step=step, input_dim=NW, params=params,
                    conserved={"mass": lambda A: A.sum()},
                    name=f"FlowLenia[A_gliders]+wind(sigma_w={SIG})^tick + stress conversion (xw in params)")


def build_world_x(params, burn: int = GW.BURN):
    """sbi_lib.build_world with the hidden law (same ports, coarse-grainings, burn-in and replay)."""
    pc = PH.phi_coarse(GW.CFG, G)
    po, _, _ = PH.phi_objects_jax("A_gliders")
    spec = vw.WorldSpec(base=level_x(params), chain=(PH.pair(pc, po),),
                        inport=vw.InputPort(admissible=vw.Admissible(k=None, lo=-1.0, hi=1.0), in_map=tuple(range(NW))),
                        outport=vw.ObservePort(noise=0.0, quantum=SL.QUANTUM, out_map=tuple(range(N_OBS)),
                                               out_sign=tuple([1.0] * N_OBS)),
                        burn_in=int(burn), replay="initial", name="gliders_wind_hidden4_incomplete_law",
                        public_notes="wind input: 128 coefficients (2 x 8 x 8), cost |u|^2 / (2 sigma_w^2) nats")
    return vw.World(spec, world_seed=0, params=params)


# ----------------------------------------------------------------------------- batched simulator
class XRunner(SL.VRunner):
    """sbi_lib.VRunner with the hidden law: P must carry 'xw' (B,). Same keys, streams and outputs."""

    def _init_burn(self, P, k, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(p, kk, sg):
            A = self.init0(p, fold(kk, GW._ST_INIT))
            m = bt.init_memory(A)
            kp = fold(fold(kk, GW._ST_BURN), GW._ST_PROC)
            zw = jnp.zeros((NW,))

            def body(c, t):
                A, m = c
                A = xtick(p, A, Noise(kp, t), zw, sg)
                return (A, bt.update_memory(m, A)), None
            (A, m), _ = jax.lax.scan(body, (A, m), jnp.arange(self.burn))
            return A, m
        return jax.vmap(one)(P, k, sig)

    def _run(self, P, A, m, key, t0, uw, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(p, A, m, kk, t0, uw, sg):
            kp = fold(kk, GW._ST_PROC)

            def rec(A, m):
                d = bt.split(m)
                return self.obs(A, m), d["table"][:, GW.NF:], d["globals"]

            def body(c, w):
                A, m, t = c
                A = xtick(p, A, Noise(kp, t), w, sg)
                m = bt.update_memory(m, A)
                return (A, m, t + 1), rec(A, m)
            r0 = rec(A, m)
            (A, m, _), outs = jax.lax.scan(body, (A, m, t0), uw)
            cat = lambda a, b: jnp.concatenate([a[None], b], 0)
            return tuple(cat(a, b) for a, b in zip(r0, outs)) + (A, m)
        return jax.vmap(one)(P, A, m, key, t0, uw, sig)


def params_batch_x(names, thetas, etas) -> dict:
    P = dict(LL.params_batch(names, thetas))
    P["xw"] = jnp.asarray(np.asarray(etas, float))
    return P


def sim_episodes_x(RN, names, thetas, etas, keys, seed, P=16, H=16, chunk=256, classes=None, log=None):
    """ladder_lib.sim_episodes under the hidden law with per-member eta (B,): the same keys, programs,
    quantisation and outputs; RN is an XRunner. With etas = 0 the outputs equal ladder_lib.sim_episodes's
    bit for bit on CPU (check_a.py)."""
    th = np.atleast_2d(np.asarray(thetas, float))
    et = np.asarray(etas, float)
    B = len(th)
    rng0 = np.random.default_rng([int(seed), 0])
    if classes is None:
        classes = rng0.choice(list(LL.MIXC), size=B)
    classes = np.asarray(classes)
    OBS = np.zeros((B, P + H + 1, N_OBS), np.float32)
    UU = np.zeros((B, P + H, NW), np.float32)
    nats = np.zeros(B)
    for s in range(0, B, chunk):
        e = min(s + chunk, B)
        nb = e - s
        Pp = params_batch_x(names, SL._pad(th[s:e], chunk), SL._pad(et[s:e], chunk))
        k = SL._pad_keys(keys[s:e], chunk)
        sig = jnp.full((chunk,), SIG)
        A, m = RN.init_burn(Pp, k, sig)
        kd = GW.dyn_keys(k)
        y1, _, _, A, m = RN.run(Pp, A, m, kd, jnp.zeros((chunk,), jnp.int64), jnp.zeros((chunk, P, NW)), sig)
        y1 = SL.quantize(np.asarray(y1)[:nb])
        U = np.zeros((chunk, H, NW))
        for b in range(nb):
            prog = LL.CLASSES[classes[s + b]](np.random.default_rng([int(seed), 1, s + b]), y1[b], H, SL.EP_CAP)
            U[b] = program_dense(prog, H, NW)
            nats[s + b] = GW.nats_of(U[b])
        y2, _, _, A, m = RN.run(Pp, A, m, kd, jnp.full((chunk,), P, jnp.int64), jnp.asarray(U), sig)
        y2 = SL.quantize(np.asarray(y2)[:nb])
        OBS[s:e] = np.concatenate([y1, y2[:, 1:]], 1)
        UU[s:e, P:] = U[:nb]
        if log:
            log(f"  sim_episodes_x {e}/{B}")
    return {"obs": OBS, "U": UU, "cls": classes, "nats": nats, "eta": et}


# ----------------------------------------------------------------------------- the zero point of the switch
_ONE = {}


def one_tick_check(B=4, seed=11, burn=2):
    """One tick from identical states under (a) gworld.tick, (a2) gworld.tick again, (b) xtick with xw = 0,
    (c) xtick with xw = 4, B members with wind inputs above the trigger (peak field above 0.17) and the
    default parameters. Returns the largest absolute differences of the level-0 field."""
    if "f" not in _ONE:
        lev0, _, _ = FJ.make_level("A_gliders", GW.NOISE_STD)

        def start(p, k):
            A = lev0.init(p, jax.random.fold_in(k, 1))
            kp = jax.random.fold_in(k, 2)

            def body(A, t):
                return GW.tick(p, A, Noise(kp, t), jnp.zeros((NW,)), SIG), None
            A, _ = jax.lax.scan(body, A, jnp.arange(burn))
            return A

        def pub(p, A, k, u):
            return GW.tick(p, A, Noise(jax.random.fold_in(k, 3), jnp.zeros((), jnp.int64)), u, SIG)

        def hid(p, A, k, u):
            return xtick(p, A, Noise(jax.random.fold_in(k, 3), jnp.zeros((), jnp.int64)), u, SIG)
        _ONE["f"] = (jax.jit(jax.vmap(start)), jax.jit(jax.vmap(pub)), jax.jit(jax.vmap(hid)))
    start, pub, hid = _ONE["f"]
    rng = np.random.default_rng(seed)
    U = np.zeros((B, 2, G, G))
    for b in range(B):
        i, j = rng.integers(0, G - 1, 2)
        U[b, :, i:i + 2, j:j + 2] = 0.3 * rng.choice([-1, 1], size=(2, 1, 1))
    U = jnp.asarray(U.reshape(B, NW))
    ks = jax.random.split(jax.random.key(seed), B)
    names = LL.SETS[4]
    cen = np.array([1.0, 0.0, 1.0, 1.0])
    P0 = params_batch_x(names, np.tile(cen, (B, 1)), np.zeros(B))
    P4 = params_batch_x(names, np.tile(cen, (B, 1)), np.full(B, 4.0))
    Pg = {k: v for k, v in P0.items() if k != "xw"}
    A0 = start(Pg, ks)
    a = np.asarray(pub(Pg, A0, ks, U))
    a2 = np.asarray(pub(Pg, A0, ks, U))
    b = np.asarray(hid(P0, A0, ks, U))
    c = np.asarray(hid(P4, A0, ks, U))
    mass = lambda x: x.reshape(B, 2, -1).sum(-1)
    return {"B": int(B), "backend": jax.default_backend(),
            "max_abs_xw0_minus_gworld": float(np.abs(b - a).max()),
            "max_abs_gworld_rerun": float(np.abs(a2 - a).max()),
            "max_abs_xw4_minus_gworld": float(np.abs(c - a).max()),
            "bitwise_xw0_equals_gworld": bool(np.array_equal(a, b)),
            "bitwise_gworld_rerun": bool(np.array_equal(a, a2)),
            "level0_max": float(a.max()),
            "channel0_mass_lost_xw4_fraction": float(1.0 - (mass(c)[:, 0] / mass(a)[:, 0]).mean()),
            "total_mass_rel_change_xw4": float(np.abs(mass(c).sum(1) / mass(a).sum(1) - 1.0).max())}
