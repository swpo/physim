"""vortex_jax -- c53's fed vortices with heredity (the selection variant) as a pure JAX vw.Level.

Source law: physim/research/alife/collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py
(the base world 20261027T0712-c53-fed-vortex-claim plus labels a, b). Vorticity-streamfunction form on
a periodic box, semi-implicit pseudo-spectral Euler step of dt = 0.02 with 2/3 dealiasing:

    d om = -u.grad om + nu lap om - hyper lap^2 om + (k (1 + eps b) Y s - mu) om + f     s = om^2/(om^2+wi^2)
    d Y  = -u.grad Y  + kY lap Y - hyper lap^2 Y - min(e Y s om^2, Y/dt) + kF (1 - Y)
    d a  = -u.grad a  + Dl lap a - dl a - hyper lap^2 a + kl (eat/Y) a (1 - a - b)     (b likewise)
    u = adv (dpsi/dy, -dpsi/dx),  lap psi = -om;   Y, a, b clipped at 0 after each step.
At t = lab_t every eating pixel (eat > 1e-3) gets a = 1, b = 0. Every mut_dt after lab_t one uniform
draw picks an eating pixel in raster order and a, b are swapped in a disk of radius mut_r there.

Differences from the numpy source (declared, not hidden):
  * the mutation draw comes from the explicit noise key (one uniform per native step, used only at
    mutation steps) instead of numpy's default_rng(mut_seed); `native_step` takes the uniform as an
    argument so the reproduction check can feed numpy's draws;
  * the switches fork_t (fuel emptied) and the bookkeeping list s['mutations'] are dropped;
  * f is new: the declared stirring channel (below). With f = 0 the step is the source step.

Stirring channel (the agent's input, EXAM section 3.3 option 1, a matched actuation channel).
u in R^m (m = G*G), one coefficient per bump of a public basis phi_j: zero-mean periodic Gaussians of
std `stir_w` px centred on a G x G grid. Every tick the world applies u~ = u + eta, eta ~ N(0, sigma_a^2 I)
(also when u = 0), and adds the vorticity field f = sum_j u~_j phi_j / T_tick at every native step of
the tick (held input), so the tick delivers sum_j u~_j phi_j of vorticity (peak ~ u~_j at bump j).
Since everything downstream is a function of u~ and independent randomness,
KL(P_u || P_0) <= sum_t |u_t|^2 / (2 sigma_a^2) for any program, at every level and port (data
processing), with equality on the channel itself. Zero-mean bumps make f the curl of a periodic force.

One vw tick = n_sub native steps (default 250 = 5 time units). State x = {'om','Y','a','b' (H, W),
't' (float64 time, accumulated as in the source)}. Parameters (the candidate hidden theta) are a flat
dict of float64 scalars; grid, dt, n_sub, schedule and channel geometry are static configuration.
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

THETA = dict(nu=0.1, mu=0.1, k=0.5, wi=0.1, kY=1.0, e=10.0, kF=0.02, hyper=0.005, Dl=0.02, kl=2.0, dl=0.05,
             eps=0.2, adv=1.0, Y0=0.6, noise=0.06, L=4.0)
FIELDS = ("om", "Y", "a", "b")


@dataclass(frozen=True)
class Config:
    H: int = 128
    W: int = 128
    dt: float = 0.02
    n_sub: int = 250            # native steps per vw tick (5 time units)
    lab_t: float = 300.0
    mut_dt: float = 50.0        # <= 0: no mutation
    mut_r: float = 6.0
    G: int = 8                  # stirring grid G x G (bump spacing H / G px)
    stir_w: float = 8.0         # bump std (px); the source noise smoothing was 2 px
    sigma_a: float = 0.005      # channel noise std per coefficient per tick (vorticity units)

    @property
    def m(self) -> int:
        return self.G * self.G

    @property
    def tick_time(self) -> float:
        return self.n_sub * self.dt


# ----------------------------------------------------------------------------- static operators
def wavenumbers(H, W):
    ky = 2 * np.pi * np.fft.fftfreq(H)[:, None]
    kx = 2 * np.pi * np.fft.rfftfreq(W)[None, :]
    return ky, kx


def spectral_tables(cfg: Config):
    """kx, ky, 1/k^2 (0 at k = 0), 2/3 dealias mask, k^2 -- as the numpy source builds them."""
    ky, kx = wavenumbers(cfg.H, cfg.W)
    ky = np.broadcast_to(ky, (cfg.H, cfg.W // 2 + 1)).copy()
    kx = np.broadcast_to(kx, (cfg.H, cfg.W // 2 + 1)).copy()
    k2 = kx ** 2 + ky ** 2
    kmax, kxm = np.abs(ky).max(), np.abs(kx).max()
    da = ((np.abs(ky) < (2 / 3) * kmax) & (np.abs(kx) < (2 / 3) * kxm)).astype(float)
    inv = np.where(k2 > 0, 1.0 / np.where(k2 > 0, k2, 1), 0.0)
    return dict(kx=kx, ky=ky, k2=k2, da=da, inv=inv)


def stir_basis(cfg: Config) -> np.ndarray:
    """(m, H*W) zero-mean periodic Gaussian bumps of std stir_w on a G x G grid (row-major)."""
    H, W, G = cfg.H, cfg.W, cfg.G
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    out = []
    for i in range(G):
        for j in range(G):
            cy, cx = (i + 0.5) * H / G, (j + 0.5) * W / G
            dy = (yy - cy + H / 2) % H - H / 2
            dx = (xx - cx + W / 2) % W - W / 2
            g = np.exp(-(dy ** 2 + dx ** 2) / (2 * cfg.stir_w ** 2))
            out.append((g - g.mean()).ravel())
    return np.stack(out)


def bump_centres(cfg: Config) -> np.ndarray:
    """(m, 2) bump centres (y, x) in px, row-major as stir_basis."""
    return np.array([((i + 0.5) * cfg.H / cfg.G, (j + 0.5) * cfg.W / cfg.G) for i in range(cfg.G) for j in range(cfg.G)])


# ----------------------------------------------------------------------------- the native step
def make_native_step(cfg: Config):
    """native_step(theta, x, mut_u, f) -> x': one dt step of the source law with mutation uniform mut_u
    and vorticity source field f (H, W). Pure; f = 0 is the source step."""
    T = spectral_tables(cfg)
    H, W, dt = cfg.H, cfg.W, cfg.dt
    sh = (H, W)
    kx, ky, k2, da, inv = (jnp.asarray(T[n]) for n in ("kx", "ky", "k2", "da", "inv"))
    per = int(round(cfg.mut_dt / dt)) if cfg.mut_dt > 0 else 0
    yy = jnp.arange(H, dtype=jnp.float64)[:, None]
    xx = jnp.arange(W, dtype=jnp.float64)[None, :]
    rfft2 = lambda z: jnp.fft.rfft2(z, axes=(-2, -1))                  # noqa: E731
    irfft2 = lambda Z: jnp.fft.irfft2(Z, s=sh, axes=(-2, -1))          # noqa: E731

    def native_step(q, x, mut_u, f):
        om, Y, a, b, t = x["om"], x["Y"], x["a"], x["b"], x["t"]
        Lom = 1 / (1 + dt * (q["nu"] * k2 + q["hyper"] * k2 ** 2))
        LY = 1 / (1 + dt * (q["kY"] * k2 + q["hyper"] * k2 ** 2))
        LL = 1 / (1 + dt * (q["Dl"] * k2 + q["dl"] + q["hyper"] * k2 ** 2))
        w2 = om ** 2
        sat = w2 / (w2 + q["wi"] ** 2)
        eat = jnp.minimum(q["e"] * Y * sat * w2, Y / dt)
        # labelling event: every eating pixel becomes kind a
        lab = (cfg.lab_t >= 0) & (jnp.abs(t - cfg.lab_t) < dt / 2)
        a = jnp.where(lab, jnp.where(eat > 1e-3, 1.0, 0.0), a)
        b = jnp.where(lab, 0.0, b)
        # trait-blind mutation: one uniform picks an eating pixel (raster order); swap a, b in a disk
        if per > 0:
            def mutate(ab):
                a_, b_ = ab
                mask = (eat > 1e-3).ravel()
                cnt = mask.sum()
                r = jnp.floor(mut_u * cnt).astype(jnp.int64)
                kk = jnp.argmax(mask & (jnp.cumsum(mask) == r + 1))
                cy, cx = (kk // W).astype(jnp.float64), (kk % W).astype(jnp.float64)
                d2 = ((yy - cy + H / 2) % H - H / 2) ** 2 + ((xx - cx + W / 2) % W - W / 2) ** 2
                m = (d2 <= cfg.mut_r ** 2) & (cnt > 0)
                return jnp.where(m, b_, a_), jnp.where(m, a_, b_)
            when = (t > cfg.lab_t) & (jnp.round(t / dt).astype(jnp.int64) % per == 0)
            a, b = jax.lax.cond(when, mutate, lambda ab: ab, (a, b))
        # spectral derivatives (the source computes rfft2(f) * da once per field; om's is shared with psi)
        Fh = rfft2(jnp.stack([om, a, b, Y])) * da
        ph = Fh[0] * inv
        D = irfft2(jnp.concatenate([jnp.stack([-1j * kx * ph, 1j * ky * ph]), 1j * ky * Fh, 1j * kx * Fh]))
        uy, ux = q["adv"] * D[0], q["adv"] * D[1]
        FA = rfft2(uy * D[2:6] + ux * D[6:10]) * da                     # u.grad of om, a, b, Y (dealiased)
        gain = q["k"] * (1 + q["eps"] * b)
        rate = eat / jnp.maximum(Y, 1e-6)
        R = jnp.stack([om + dt * ((gain * Y * sat - q["mu"]) * om + f),
                       a + dt * (q["kl"] * rate * a * (1 - a - b)),
                       b + dt * (q["kl"] * rate * b * (1 - a - b)),
                       Y + dt * (-eat + q["kF"] * (1 - Y))])
        # = the source's irfft2(rfft2(field + dt (-adv + R)) L) with rfft2(irfft2(FA)) = FA (round-off level)
        out = irfft2((rfft2(R) - dt * FA) * jnp.stack([Lom, LL, LL, LY]))
        return {"om": out[0], "Y": jnp.maximum(out[3], 0.0), "a": jnp.maximum(out[1], 0.0),
                "b": jnp.maximum(out[2], 0.0), "t": t + dt}

    return native_step


def make_init(cfg: Config):
    """init(theta, key): band-passed Gaussian noise vorticity (std `noise`, scale L), uniform fuel Y0, no
    labels, t = 0 -- the source's init with JAX normals instead of numpy's generator."""
    H, W = cfg.H, cfg.W
    yy = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    xx = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    r2 = jnp.asarray((xx ** 2 + yy ** 2).astype(float))

    def gk(sig):
        K = jnp.exp(-r2 / (2 * sig ** 2))
        return jnp.fft.rfft2(K / K.sum())

    def init(q, key):
        z = jax.random.normal(key, (H, W), jnp.float64)
        n = jnp.fft.irfft2(jnp.fft.rfft2(z) * gk(q["L"]), s=(H, W))
        n = n - jnp.fft.irfft2(jnp.fft.rfft2(n) * gk(4 * q["L"]), s=(H, W))
        om = q["noise"] * n / n.std()
        Z = jnp.zeros((H, W))
        return {"om": om, "Y": q["Y0"] * jnp.ones((H, W)), "a": Z, "b": Z, "t": jnp.zeros(())}

    return init


# ----------------------------------------------------------------------------- the vw Level
def channel(cfg: Config, noise: vw.Noise, u):
    """The realised stirring coefficients u~ = u + eta, eta ~ N(0, sigma_a^2 I) from stream 0."""
    return u + cfg.sigma_a * noise.stream(0).normal((cfg.m,))


def make_level(cfg: Config = Config(), theta: dict | None = None, name: str = "fedvortex") -> vw.Level:
    """One tick = n_sub native steps with the stirring input held over the tick (see module doc).
    Noise: stream 0 = channel noise (one m-vector per tick); stream 1, substep(n_sub, i) = the
    mutation uniform of native step i."""
    q0 = {k: jnp.asarray(v, jnp.float64) for k, v in dict(THETA, **(theta or {})).items()}
    ns = make_native_step(cfg)
    B = jnp.asarray(stir_basis(cfg))
    n = cfg.n_sub

    def step(q, x, noise, u):
        f = (channel(cfg, noise, u) @ B).reshape(cfg.H, cfg.W) / cfg.tick_time
        mut = noise.stream(1)

        def body(i, xx):
            return ns(q, xx, mut.substep(n, i).uniform(), f)
        return jax.lax.fori_loop(0, n, body, x)

    return vw.Level(init=make_init(cfg), step=step, input_dim=cfg.m, params=q0, differentiable=True,
                    name=f"{name}{cfg.H}x{cfg.W}/tick{n}")


def replace(cfg: Config, **kw) -> Config:
    return dataclasses.replace(cfg, **kw)
