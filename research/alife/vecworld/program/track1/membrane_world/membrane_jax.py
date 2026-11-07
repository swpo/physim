"""membrane_jax -- the phase_membrane world (autopoiesis lab 1) as a pure JAX vw.Level.

Source law: physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py with its defaults
(kin = 'logistic', gate = gateK = 1, nophase = 0, scale = 1, IC = 'noise'). Explicit Euler on a periodic
128^2 grid (dx = 1), 5-point Laplacian, face-averaged mobilities, first-order upwind link drift:

    S'   = max(S + dt (DS lap S - A - P + F (1 - S) + f), 0)                 A = c S K (1-K) phi,  P = b K S
    K'   = max(K + dt (div(DK g grad K) + A - dK K), 0)                      g = phi^2 (face mean)
    L'   = max(L + dt (div(DL g grad L) - div(L v) + P - dL L), 0)            v = DL chi g grad(4 phi (1-phi))
    phi' = clip(phi + dt Dp lap phi + dt r phi (1-phi)(phi - 1/2 + a (L - th)), 0, 1)
with A, P scaled by lim = min(1, 0.5 S / max(dt (A + P), 1e-12)) (consumption capped at half the substrate).
Every update uses the old fields (the source's order of operations is kept, so f = 0 is the source step to
round-off). Nothing is conserved (WORLDS.md section 1).

Differences from the numpy source (declared, not hidden):
  * the initial-field draws come from JAX keys (same law: smoothed normal phi, std-normalised, clipped;
    uniform K and L; the extra 0.01 U phi on K); the smoothing is vw.objects.gaussian_blur_wrap, which is
    scipy.ndimage.gaussian_filter(mode='wrap') bit for bit; the reproduction check starts from numpy's state;
  * the unused switches (kin = 'gs', gate, gateK, nophase, scale, IC = 'spots') are dropped;
  * f is new: the declared substrate channel (below). With f = 0 the native step is the source step.
  * v1's (PhySim LabWorld) pixel noise -- additive on phi, proportional on S, K, L -- is replaced by the
    channel: the only randomness of the law.

Substrate channel (the agent's input; EXAM section 3.3 option 1, a matched actuation channel).
u in R^m (m = G*G), one coefficient per bump of a public basis b_j: periodic Gaussians of std `bump_w` px
and peak 1 centred on a G x G grid. Every tick the world applies u~ = u + eta, eta ~ N(0, sigma_a^2 I)
(also when u = 0), and adds the substrate source f = sum_j u~_j b_j / tick_time inside the S update of
every native step of the tick (held input), so a tick delivers sum_j u~_j b_j of substrate (peak u~_j at
bump j): feeding (u > 0) or withdrawal (u < 0). Everything downstream is a function of u~ and the initial
state, so KL(P_u || P_0) <= sum_t |u_t|^2 / (2 sigma_a^2) for any program, at every level and port (data
processing), with equality on the channel itself. Why S: it is a concentration whose law already has
additive source terms (the chemostat feed F (1 - S), consumption), so a shift is an amount of substrate with
a state-independent meaning (a pipette); and in this world S stays in [0.11, 0.99] without and [0.09, 1.02] with
the channel noise (results/explore.json), far from its clip at 0, so a smooth shift of the declared size is not
rectified. phi is bistable and sits near its bottom well (phi < 1e-3 on 39% of the box), where the per-step clip at
0 would rectify any negative push (a zero-mean channel there would bias the bath up); K and L are ~0 outside cells
(K < 1e-6 on 36% of the box), where an additive shift has no meaning. They carry no noise and no input.

One vw tick = n_sub native steps of dt (default dt 0.5, n_sub 20: 10 time units). State x = {'S','K','L',
'phi'} (H, W) float64. Parameters (the candidate hidden theta) are a flat dict of float64 scalars; grid, dt,
n_sub and the channel geometry are static configuration.
"""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass

import jax

jax.config.update("jax_enable_x64", True)
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import _paths  # noqa: F401,E402
import vw  # noqa: E402
from vw.objects import gaussian_blur_wrap  # noqa: E402

THETA = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, b=0.05, dL=0.02, c=0.2, dK=0.02,
             chi=2.0, noise_amp=0.2, noise_mean=0.0, noise_KL=0.1, noise_K=0.6)
FIELDS = ("S", "K", "L", "phi")


@dataclass(frozen=True)
class Config:
    H: int = 128
    W: int = 128
    dt: float = 0.5             # native step (the eval suite's; the source default is 1.0)
    n_sub: int = 20             # native steps per vw tick (tick_time = dt * n_sub = 10 time units)
    G: int = 16                 # channel grid G x G (bump spacing H / G = 8 px)
    bump_w: float = 4.0         # bump std (px)
    sigma_a: float = 0.01       # channel noise std per coefficient per tick (substrate units at the peak)

    @property
    def m(self) -> int:
        return self.G * self.G

    @property
    def tick_time(self) -> float:
        return self.n_sub * self.dt


def replace(cfg: Config, **kw) -> Config:
    return dataclasses.replace(cfg, **kw)


def with_dt(cfg: Config, dt: float) -> Config:
    """The same tick (tick_time) at another native step."""
    n = int(round(cfg.tick_time / dt))
    assert abs(n * dt - cfg.tick_time) < 1e-12
    return dataclasses.replace(cfg, dt=float(dt), n_sub=n)


# ----------------------------------------------------------------------------- stencils (source order)
def roll(u, s, ax):
    return jnp.roll(u, s, ax)


def lap(u):
    return roll(u, 1, 0) + roll(u, -1, 0) + roll(u, 1, 1) + roll(u, -1, 1) - 4 * u


def mob_div(u, g, D):
    out = jnp.zeros_like(u)
    for ax in (0, 1):
        gf = 0.5 * (g + roll(g, -1, ax))
        flux = D * gf * (roll(u, -1, ax) - u)
        out = out + (flux - roll(flux, 1, ax))
    return out


def upwind_div(rho, vy, vx):
    out = jnp.zeros_like(rho)
    for v, ax in ((vy, 0), (vx, 1)):
        vf = 0.5 * (v + roll(v, -1, ax))
        flux = vf * jnp.where(vf > 0, rho, roll(rho, -1, ax))
        out = out + (flux - roll(flux, 1, ax))
    return out


def make_native_step(cfg: Config):
    """native_step(theta, x, f) -> x': one dt step of the source law with substrate source field f (H, W)."""
    h = float(cfg.dt)

    def native_step(q, x, f):
        S, K, L, phi = x["S"], x["K"], x["L"], x["phi"]
        g = phi * phi
        auto = q["c"] * S * K * (1 - K) * phi
        kdec = q["dK"]
        prodL = q["b"] * K * S
        lim = jnp.minimum(1.0, 0.5 * S / jnp.maximum(h * (auto + prodL), 1e-12))
        auto, prodL = auto * lim, prodL * lim
        S2 = jnp.maximum(S + h * (q["DS"] * lap(S) - auto - prodL + q["F"] * (1 - S) + f), 0)
        K2 = jnp.maximum(K + h * (mob_div(K, g, q["DK"]) + auto - kdec * K), 0)
        w = 4 * phi * (1 - phi)
        pre = q["DL"] * q["chi"] * g * 0.5
        vy = pre * (roll(w, -1, 0) - roll(w, 1, 0))
        vx = pre * (roll(w, -1, 1) - roll(w, 1, 1))
        adv = upwind_div(L, vy, vx)
        L2 = jnp.maximum(L + h * (mob_div(L, g, q["DL"]) - adv + prodL - q["dL"] * L), 0)
        phi2 = jnp.clip(phi + h * q["Dp"] * lap(phi) + h * q["r"] * phi * (1 - phi) * (phi - 0.5 + q["a"] * (L - q["th"])),
                        0, 1)
        return {"S": S2, "K": K2, "L": L2, "phi": phi2}

    return native_step


def make_init(cfg: Config):
    """init(theta, key): the source's IC 'noise' (smoothed normal phi, uniform K and L, S = 1) from JAX draws."""
    H, W = cfg.H, cfg.W

    def init(q, key):
        k1, k2, k3, k4 = jax.random.split(key, 4)
        n = gaussian_blur_wrap(jax.random.normal(k1, (H, W), jnp.float64), 3.0)
        phi = jnp.clip(q["noise_mean"] + n / n.std() * q["noise_amp"], 0, 1)
        K = q["noise_K"] * jax.random.uniform(k2, (H, W), jnp.float64)
        L = q["noise_KL"] * jax.random.uniform(k3, (H, W), jnp.float64)
        K = K + 0.01 * jax.random.uniform(k4, (H, W), jnp.float64) * phi
        return {"S": jnp.ones((H, W)), "K": K, "L": L, "phi": phi}

    return init


# ----------------------------------------------------------------------------- the channel
def bump_basis(cfg: Config) -> np.ndarray:
    """(m, H*W) periodic Gaussian bumps of std bump_w px and peak 1 on a G x G grid (row-major)."""
    H, W, G = cfg.H, cfg.W, cfg.G
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    out = []
    for i in range(G):
        for j in range(G):
            cy, cx = (i + 0.5) * H / G, (j + 0.5) * W / G
            dy = (yy - cy + H / 2) % H - H / 2
            dx = (xx - cx + W / 2) % W - W / 2
            out.append(np.exp(-(dy ** 2 + dx ** 2) / (2 * cfg.bump_w ** 2)).ravel())
    return np.stack(out)


def bump_centres(cfg: Config) -> np.ndarray:
    """(m, 2) bump centres (y, x) in px, row-major as bump_basis."""
    return np.array([((i + 0.5) * cfg.H / cfg.G, (j + 0.5) * cfg.W / cfg.G) for i in range(cfg.G) for j in range(cfg.G)])


def channel(cfg: Config, noise: vw.Noise, u):
    """The realised coefficients u~ = u + eta, eta ~ N(0, sigma_a^2 I) from noise stream 0."""
    return u + cfg.sigma_a * noise.stream(0).normal((cfg.m,))


def make_level(cfg: Config = Config(), theta: dict | None = None, name: str = "membrane") -> vw.Level:
    """One tick = n_sub native steps with the substrate channel held over the tick (module doc).
    Noise: stream 0 = channel noise (one m-vector per tick); the law has no other randomness."""
    q0 = {k: jnp.asarray(v, jnp.float64) for k, v in dict(THETA, **(theta or {})).items()}
    ns = make_native_step(cfg)
    B = jnp.asarray(bump_basis(cfg))
    n = cfg.n_sub

    def step(q, x, noise, u):
        f = (channel(cfg, noise, u) @ B).reshape(cfg.H, cfg.W) / cfg.tick_time
        return jax.lax.fori_loop(0, n, lambda i, xx: ns(q, xx, f), x)

    return vw.Level(init=make_init(cfg), step=step, input_dim=cfg.m, params=q0, differentiable=True,
                    name=f"{name}{cfg.H}x{cfg.W}/dt{cfg.dt:g}x{n}")
