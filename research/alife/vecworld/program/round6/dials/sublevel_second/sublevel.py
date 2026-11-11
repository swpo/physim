"""sublevel -- the phase_membrane world with a hidden finer level (round 6, dials, designer sublevel_second).

DESIGN-STAGE CODE: small CPU checks only. Nothing in vw or in track1/membrane_world is changed; this module wraps
track1/membrane_world/membrane_jax.py (the PUBLIC law) and adds one hidden field and one coupling per candidate.

Public law (membrane_jax): S substrate, K catalyst, L lipid, phi phase;  A = c S K (1-K) phi (catalyst made from
substrate), P = b K S (lipid made from substrate), both capped at half the substrate.

Candidates for the hidden finer level (each adds one hidden field; `lam` is the dial; lam = 0 with the hidden
field at its equilibrium, which is 0 at lam = 0, is the public law, checked bit for bit in check_zero.py):

  'kpool'  intracellular catalyst precursor Q (moves like K): a fraction lam of A enters Q and matures at rate rho
               Q' = div(DK g grad Q) + lam A - rho Q            K' = ... + (1 - lam) A + rho Q - dK K
  'lpool'  intracellular lipid precursor R (moves like L without the link drift): a fraction lam of P enters R
               R' = div(DL g grad R) + lam P - rho R            L' = ... + (1 - lam) P + rho R - dL L
  'dorm'   two-state catalyst K = Ka + Ki (Ki inactive, moves and decays like K): active catalyst goes dormant
           where the substrate is below s_c and wakes at rate k_on
               Ki' = div(DK g grad Ki) + lam k_off sig((s_c - S) / w_c) Ka - k_on Ki - dK Ki ;  A, P use Ka
           (the observed catalyst is the total K, as in the public law)
  'bound'  substrate bound to the medium, B (immobile, not eaten, not washed out): S <-> B
               B' = lam k_a S - k_d B                           S' = ... - lam k_a S + k_d B
           (retardation factor 1 + lam k_a / k_d at equilibrium)

In balanced (slow) conditions 'kpool' and 'lpool' deliver exactly the public fluxes (rho Q = lam A), 'bound' sits
at B = (lam k_a / k_d) S with no net exchange, and 'dorm' is silent while S stays above s_c: the public law is
the adiabatic limit of each. Hidden numbers used here are illustrative pilot values, never exam values.
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.abspath(os.path.join(HERE, "..", "..", ".."))            # .../vecworld/program
MWDIR = os.path.join(PROG, "track1", "membrane_world")
if MWDIR not in sys.path:
    sys.path.insert(0, MWDIR)

import _paths  # noqa: F401,E402   (track1/membrane_world: puts the vw library on the path)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
import membrane_jax as MJ  # noqa: E402
import membrane_world as MW  # noqa: E402

CANDS = ("kpool", "lpool", "dorm", "bound")
EXTRA = {"kpool": "Q", "lpool": "R", "dorm": "Ki", "bound": "B"}
# illustrative hidden values (time units; one tick = 10): PILOT ONLY, never to be reused as an exam
HID0 = dict(lam=0.0, rho=0.005, k_off=0.05, k_on=0.004, s_c=0.25, w_c=0.03, k_a=0.02, k_d=0.01)


def make_native_step(cfg: MJ.Config, cand: str):
    """native_step(theta, x, f) -> x' for the hidden world; x has the public fields and EXTRA[cand]."""
    assert cand in CANDS, cand
    h = float(cfg.dt)
    lap, mob_div, upwind_div, roll = MJ.lap, MJ.mob_div, MJ.upwind_div, MJ.roll
    ek = EXTRA[cand]

    def native_step(q, x, f):
        S, K, L, phi, E = x["S"], x["K"], x["L"], x["phi"], x[ek]
        lam = q["lam"]
        g = phi * phi
        Ka = K - E if cand == "dorm" else K
        auto = q["c"] * S * Ka * (1 - K) * phi
        kdec = q["dK"]
        prodL = q["b"] * Ka * S
        lim = jnp.minimum(1.0, 0.5 * S / jnp.maximum(h * (auto + prodL), 1e-12))
        auto, prodL = auto * lim, prodL * lim
        zero = jnp.zeros_like(S)
        dS = dK = dL = zero
        if cand == "kpool":
            E2 = jnp.maximum(E + h * (mob_div(E, g, q["DK"]) + lam * auto - q["rho"] * E), 0)
            dK = q["rho"] * E - lam * auto
        elif cand == "lpool":
            E2 = jnp.maximum(E + h * (mob_div(E, g, q["DL"]) + lam * prodL - q["rho"] * E), 0)
            dL = q["rho"] * E - lam * prodL
        elif cand == "dorm":
            off = lam * q["k_off"] * jax.nn.sigmoid((q["s_c"] - S) / q["w_c"]) * Ka
            E2 = jnp.maximum(E + h * (mob_div(E, g, q["DK"]) + off - q["k_on"] * E - kdec * E), 0)
        else:  # bound
            ex = q["k_d"] * E - lam * q["k_a"] * S
            E2 = jnp.maximum(E - h * ex, 0)
            dS = ex
        S2 = jnp.maximum(S + h * (q["DS"] * lap(S) - auto - prodL + q["F"] * (1 - S) + f + dS), 0)
        K2 = jnp.maximum(K + h * (mob_div(K, g, q["DK"]) + auto - kdec * K + dK), 0)
        w = 4 * phi * (1 - phi)
        pre = q["DL"] * q["chi"] * g * 0.5
        vy = pre * (roll(w, -1, 0) - roll(w, 1, 0))
        vx = pre * (roll(w, -1, 1) - roll(w, 1, 1))
        adv = upwind_div(L, vy, vx)
        L2 = jnp.maximum(L + h * (mob_div(L, g, q["DL"]) - adv + prodL - q["dL"] * L + dL), 0)
        phi2 = jnp.clip(phi + h * q["Dp"] * lap(phi) + h * q["r"] * phi * (1 - phi) * (phi - 0.5 + q["a"] * (L - q["th"])),
                        0, 1)
        if cand == "dorm":
            E2 = jnp.minimum(E2, K2)
        return {"S": S2, "K": K2, "L": L2, "phi": phi2, ek: E2}

    return native_step


def make_level(cfg: MJ.Config, cand: str, hidden: dict | None = None, theta: dict | None = None) -> vw.Level:
    """The hidden world as a vw.Level: the public tick (channel held over n_sub native steps) with the hidden
    field. Same noise stream as membrane_jax.make_level, so with lam = 0 the public fields are the public world's."""
    q0 = {k: jnp.asarray(v, jnp.float64) for k, v in {**MJ.THETA, **HID0, **(theta or {}), **(hidden or {})}.items()}
    ns = make_native_step(cfg, cand)
    B = jnp.asarray(MJ.bump_basis(cfg))
    n = cfg.n_sub
    init_pub = MJ.make_init(cfg)
    ek = EXTRA[cand]

    hh = float(cfg.dt)

    def init(q, key):
        # the hidden field starts at its adiabatic equilibrium with the public initial fields (pools: the content
        # that delivers the public flux, rho E = lam * flux; bound: no net exchange; dorm: nothing dormant), so a
        # world does not begin with an empty hidden level. lam = 0 gives E = 0 exactly.
        x = init_pub(q, key)
        S, K, phi = x["S"], x["K"], x["phi"]
        if cand in ("kpool", "lpool"):
            auto = q["c"] * S * K * (1 - K) * phi
            prodL = q["b"] * K * S
            lim = jnp.minimum(1.0, 0.5 * S / jnp.maximum(hh * (auto + prodL), 1e-12))
            E = q["lam"] * (auto if cand == "kpool" else prodL) * lim / q["rho"]
        elif cand == "bound":
            E = q["lam"] * q["k_a"] / q["k_d"] * S
        else:
            E = jnp.zeros((cfg.H, cfg.W))
        return dict(x, **{ek: E})

    def step(q, x, noise, u):
        f = (MJ.channel(cfg, noise, u) @ B).reshape(cfg.H, cfg.W) / cfg.tick_time
        return jax.lax.fori_loop(0, n, lambda i, xx: ns(q, xx, f), x)

    return vw.Level(init=init, step=step, input_dim=cfg.m, params=q0, differentiable=True,
                    name=f"membrane+{cand}{cfg.H}x{cfg.W}/dt{cfg.dt:g}x{n}")


def build(cfg: MJ.Config, cand: str | None = None, hidden: dict | None = None, theta: dict | None = None,
          u_max: float = 0.2, quantum: float = 1e-3):
    """(WorldSpec observed at level 2 = population on the cell list, parts). cand None = the public world
    (membrane_world.build unchanged)."""
    if cand is None:
        specs, parts = MW.build(cfg, theta, u_max=u_max, quantum=quantum)
        return specs["population"], parts
    lev = make_level(cfg, cand, hidden, theta)
    p1, tr = MW.phi_cells(cfg)
    p2 = MW.phi_population(tr.K, cfg.tick_time, MW.W_RATE, MW.M_DIV)
    inport = vw.InputPort(admissible=vw.Admissible(lo=-u_max, hi=u_max), in_map=tuple(range(cfg.m)))
    n1 = tr.n_out + len(vw.objects.GLOBALS)
    s1 = vw.WorldSpec(chain=(p1,), outport=vw.ObservePort(quantum=quantum, out_map=tuple(range(n1))),
                      name=f"membrane{cfg.H}+{cand}/cells", base=lev, inport=inport, burn_in=0, replay="initial",
                      public_notes=MW.NOTE)
    s2 = vw.stack(s1, p2, name=f"membrane{cfg.H}+{cand}/population")
    s2 = s2.replace(inport=inport, outport=vw.ObservePort(quantum=quantum, out_map=(0, 1, 2)))
    return s2, {"level": lev, "phi1": p1, "phi2": p2, "tracker": tr, "cfg": cfg}


def project(x: dict) -> dict:
    """Hidden state -> public state (the coarse-graining Psi of the refinement: forget the hidden field)."""
    return {k: x[k] for k in MJ.FIELDS}


def small_cfg(size: int = 64) -> MJ.Config:
    """A box of size x size px with the public bump spacing (8 px) and everything else at the defaults."""
    return MJ.Config(H=size, W=size, G=size // 8)


# ----------------------------------------------------------------------------- views of the cell list (numpy)
def list_views(L1: np.ndarray, K: int, size: int, block: int = 16):
    """From level-1 vectors (..., K*12 + 5): the block raster of the list (cell mass and catalyst mass per block,
    2 x (size/block)^2 numbers, as vortexexam's scored level-1 view) and the population pair (N, mean size)."""
    T = L1[..., :K * 12].reshape(L1.shape[:-1] + (K, 12))
    pres = T[..., 0] > 0.5
    mass = np.where(pres, T[..., 1], 0.0)
    kmass = mass * T[..., 2]
    cx = (np.arctan2(T[..., 4], T[..., 3]) * size / (2 * np.pi)) % size
    cy = (np.arctan2(T[..., 6], T[..., 5]) * size / (2 * np.pi)) % size
    nb = size // block
    bi = (np.clip((cy // block).astype(int), 0, nb - 1) * nb + np.clip((cx // block).astype(int), 0, nb - 1))
    onehot = (bi[..., None] == np.arange(nb * nb)) & pres[..., None]                 # (..., K, nb*nb)
    rm = (onehot * mass[..., None]).sum(-2)
    rk = (onehot * kmass[..., None]).sum(-2)
    n = pres.sum(-1).astype(float)
    size_mean = mass.sum(-1) / np.maximum(n, 1.0)
    return np.concatenate([rm, rk], -1), np.stack([n, size_mean], -1)
