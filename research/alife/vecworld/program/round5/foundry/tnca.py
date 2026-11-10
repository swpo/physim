"""tnca -- world foundry v0: the affinity transport NCA family (round 5, track 1, study foundry).

A level-0 family whose hidden weights are the law. One world = one draw theta from the declared prior
below; the code, the prior and every constant of `Family` are public, theta is hidden.

State      x in R_+^(C x H x W), periodic (default C = 2, H = W = 64); x[c, i, j] is the mass of matter
           kind c in cell (i, j).
Perception isotropic scales per kind, by an a-trous cascade of periodic binomial filters ([1 2 1]/4 per
           axis at dilations 1 | 1, 2 | 2, 4 | 4, 8): s1 (std 0.7 px, radius 1), s2 (std 1.7 px, radius 4),
           s3 (std 3.6 px, radius 10), s4 (std 7.3 px, radius 22). The net's features are
           f = (s2, s3, s4) x C; s1 enters the crowding term only. Finite range. The raw cell value is
           not used: every binomial pass has zero response at the Nyquist wavenumber of either axis, so
           the potential cannot feed a checkerboard (lattice-scale) instability (a first version with
           the raw cell as a feature and raw S in the crowding term did, in 7 of 16 draws), and the
           finest attractive scale (1.7 px) puts bodies at a few px across (with s1 as a feature the CPU
           pilot gave 2 px spots that filled every tracker slot).
Law net    hidden per-cell network, the same at every cell (so the law is translation- and
           D4-equivariant): h = tanh(W1^T f + b1) (HID units), o = W2^T h, split into
               a_c  affinity of kind c for a cell       (C numbers)
               m_c  log-mobility of kind c in a cell    (C numbers)
               r_cc' conversion logits kind c -> c'     (C*C numbers, diagonal unused)
Transport  for kind c the potential is U_c = beta * a_c - (alpha / 2) * S1^2 with S1 = sum_c s1_c
           (the 3 x 3 binomial mean of the total density): the second term is the crowding term (CRITIQUE
           section 5; the analogue of Flow-Lenia's -alpha grad A_sum), unbounded in S1 while the affinity
           is bounded, so matter cannot pile up into a point mass.
           Matter of kind c in cell i moves to its 4 neighbours j with
               z_c(i->j) = gam * m_c(i) + U_c(j) - U_c(i) + sigma * xi_c(i->j) + wq_c * wind(i).e_ij
               zt        = L * tanh(z / L)                         (bounded rates)
               q_c(i->j) = (mu/4) exp(zt) / [(1 - mu) + (mu/4) sum_j' exp(zt_c(i->j'))]
           (a softmax over the 5-point stencil with noise on the logits), xi iid N(0, 1) per kind, cell,
           direction and substep. x'_c(j) = stay_c(j) + sum_i x_c(i) q_c(i->j): a column-stochastic
           update, so mass is conserved to rounding and positivity holds exactly (sums and products of
           non-negative numbers).
Conversion in each cell a fraction p(c->c') = k / (1 + sum k), k = kappa * exp(L tanh(gr * r_cc' / L)), of
           kind c becomes kind c' (after transport, features of the substep's start). Total mass is
           conserved; with kappa = 0 (half the prior) each kind is conserved separately.
Tick       NSUB = 4 substeps; one call of the vw.Level is one tick.
Wind       a = u + sigma_w * eta, eta ~ N(0, I) (2 x GW x GW coefficients, GW = 8: one force per 8 x 8 px
           block and component), drawn once per tick from its own sub-stream and held for the tick;
           wind = E(a), E = block-constant upsampling followed by binomial smoothing (std 3.6 px, DC
           gain 1, linear, public). Charge c(u) = 0.5 |u|^2 / sigma_w^2 nats per tick, exact: given a
           the law of the level-0 path does not depend on the program, so KL(P_u || P_0) is the KL of
           the a sequence (the argument of track2/actuation/wind.py). wq_c (the wind coupling of kind c)
           is hidden.
Init       x_c = dens_c * exp(g_c) / mean(exp(g_c)), g_c smoothed white noise of unit rms (std 1 px: small
           scales only, so a world whose uniform state is stable is uniform after the burn-in instead
           of carrying the initial clouds for hundreds of ticks).

Prior (declared; `draw_theta`): W1 ~ N(0, G1^2 / F), b1 ~ N(0, 1), W2 ~ N(0, 1 / HID); beta ~ logU[2, 60],
gam ~ U[0, 2], alpha ~ logU[0.3, 30], mu ~ U[0.05, 0.25], kappa = 0 w.p. 1/2 else logU[0.002, 0.1],
gr ~ U[0, 3], dens_c ~ logU[0.03, 0.6] iid, wq_c ~ U[0, 2]. Draws use numpy's PCG64 seeded by
(prior_seed, index), so theta is the same on every platform.

Functions are pure and written for one world; batching is by jax.vmap (weights are per-world matmul
operands, no convolution).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # research/alife/vecworld
VW1 = os.path.join(VEC, "vw1")
if VW1 not in sys.path:
    sys.path.insert(0, VW1)

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import vw  # noqa: E402  (enables float64)
from vw.core import Noise  # noqa: E402

WIND_STREAM = 7


@dataclass(frozen=True)
class Family:
    """Public constants of the family."""
    C: int = 2
    H: int = 64
    W: int = 64
    HID: int = 16
    NSUB: int = 4
    sigma: float = 0.3          # logit noise per kind, cell, direction, substep
    L: float = 3.0              # logit bound
    GW: int = 8                 # wind blocks per axis
    sigma_w: float = 0.25       # wind noise per coefficient and tick
    G1: float = 2.0             # first-layer gain of the prior
    init_contrast: float = 1.0

    @property
    def F(self) -> int:
        return 3 * self.C

    @property
    def O(self) -> int:
        return 2 * self.C + self.C * self.C

    @property
    def NW(self) -> int:
        return 2 * self.GW * self.GW

    @property
    def n_weights(self) -> int:
        return self.F * self.HID + self.HID + self.HID * self.O


FAM = Family()
PRIOR = dict(beta=("logU", 2.0, 60.0), gam=("U", 0.0, 2.0), alpha=("logU", 0.3, 30.0), mu=("U", 0.05, 0.25),
             kappa=("0|logU", 0.5, 0.002, 0.1), gr=("U", 0.0, 3.0), dens=("logU", 0.03, 0.6), wq=("U", 0.0, 2.0))
SCALARS = ("beta", "gam", "alpha", "mu", "kappa", "gr")


# ----------------------------------------------------------------------------- prior
def draw_theta(prior_seed: int, index: int, fam: Family = FAM) -> dict:
    """One draw from the prior as numpy arrays (float64); platform independent."""
    g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([int(prior_seed), int(index)])))
    th = {}
    th["W1"] = g.normal(size=(fam.F, fam.HID)) * fam.G1 / np.sqrt(fam.F)
    th["b1"] = g.normal(size=(fam.HID,))
    th["W2"] = g.normal(size=(fam.HID, fam.O)) / np.sqrt(fam.HID)

    def lu(lo, hi, size=None):
        return np.exp(g.uniform(np.log(lo), np.log(hi), size))
    th["beta"] = lu(2.0, 60.0)
    th["gam"] = g.uniform(0.0, 2.0)
    th["alpha"] = lu(0.3, 30.0)
    th["mu"] = g.uniform(0.05, 0.25)
    on = g.uniform() < 0.5
    k = lu(0.002, 0.1)
    th["kappa"] = float(k) if on else 0.0
    th["gr"] = g.uniform(0.0, 3.0)
    th["dens"] = lu(0.03, 0.6, (fam.C,))
    th["wq"] = g.uniform(0.0, 2.0, (fam.C,))
    return {k: np.asarray(v, np.float64) for k, v in th.items()}


def draw_thetas(prior_seed: int, indices, fam: Family = FAM) -> dict:
    """Stacked draws (leading axis = draw)."""
    ths = [draw_theta(prior_seed, i, fam) for i in indices]
    return {k: np.stack([t[k] for t in ths]) for k in ths[0]}


def perturb_theta(th: dict, prior_seed: int, index: int, eps: float, fam: Family = FAM, hyper: bool = False) -> dict:
    """A neighbour of theta: weights W' = sqrt(1 - eps^2) W + eps W_fresh (keeps the Gaussian prior
    marginal; correlation sqrt(1 - eps^2)); the scalars are kept unless hyper=True (then the log-uniform
    and uniform scalars move by eps of their prior range, reflected at the ends; kappa = 0 stays 0)."""
    fresh = draw_theta(prior_seed + 7919, index, fam)
    out = dict(th)
    c = np.sqrt(1.0 - eps * eps)
    for k in ("W1", "b1", "W2"):
        out[k] = c * th[k] + eps * fresh[k]
    if hyper:
        g = np.random.Generator(np.random.PCG64(np.random.SeedSequence([int(prior_seed) + 104729, int(index)])))

        def refl(v, lo, hi):
            r = hi - lo
            v = (v - lo) % (2 * r)
            return lo + np.where(v > r, 2 * r - v, v)
        for k, spec in PRIOR.items():
            if spec[0] == "logU":
                lo, hi = np.log(spec[1]), np.log(spec[2])
                out[k] = np.exp(refl(np.log(th[k]) + eps * (hi - lo) * g.normal(size=np.shape(th[k])), lo, hi))
            elif spec[0] == "U":
                out[k] = refl(th[k] + eps * (spec[2] - spec[1]) * g.normal(size=np.shape(th[k])), spec[1], spec[2])
            elif k == "kappa" and float(th[k]) > 0:
                lo, hi = np.log(spec[2]), np.log(spec[3])
                out[k] = np.exp(refl(np.log(th[k]) + eps * (hi - lo) * g.normal(), lo, hi))
    return {k: np.asarray(v, np.float64) for k, v in out.items()}


# ----------------------------------------------------------------------------- the law
def _b1(x, d: int, axis: int):
    """Periodic binomial [1 2 1]/4 at dilation d along one axis."""
    return 0.5 * x + 0.25 * (jnp.roll(x, d, axis) + jnp.roll(x, -d, axis))


def blur(x, d: int):
    return _b1(_b1(x, d, -1), d, -2)


def perceive(x):
    """(C, H, W) -> s1 (C, H, W) and the net's features (3C, H, W): the kinds at scales s2, s3, s4."""
    s1 = blur(x, 1)
    s2 = blur(blur(s1, 1), 2)
    s3 = blur(blur(s2, 2), 4)
    s4 = blur(blur(s3, 4), 8)
    return s1, jnp.concatenate([s2, s3, s4], 0)


def net(th, f):
    """(F, H, W) -> (O, H, W)."""
    h = jnp.tanh(jnp.einsum("fhw,fk->khw", f, th["W1"]) + th["b1"][:, None, None])
    return jnp.einsum("khw,ko->ohw", h, th["W2"])


def substep(th, x, xi, wind, fam: Family = FAM):
    """One substep. x (C, H, W) >= 0; xi (C, 4, H, W) standard normal; wind (2, H, W) [y, x].
    Directions: 0 = +y (to row i + 1), 1 = -y, 2 = +x (to column j + 1), 3 = -x."""
    C, L = fam.C, fam.L
    s1, f = perceive(x)
    o = net(th, f)
    S = s1.sum(0)                                                                    # S1
    U = th["beta"] * o[:C] - 0.5 * th["alpha"] * (S * S)[None]
    s = th["gam"] * o[C:2 * C]
    dU = jnp.stack([jnp.roll(U, -1, -2) - U, jnp.roll(U, 1, -2) - U,
                    jnp.roll(U, -1, -1) - U, jnp.roll(U, 1, -1) - U], 1)             # (C, 4, H, W)
    wdir = jnp.stack([wind[0], -wind[0], wind[1], -wind[1]], 0)[None]                # (1, 4, H, W)
    z = s[:, None] + dU + fam.sigma * xi + th["wq"][:, None, None, None] * wdir
    w = (0.25 * th["mu"]) * jnp.exp(L * jnp.tanh(z / L))
    Z = (1.0 - th["mu"]) + (w[:, 0] + w[:, 1] + w[:, 2] + w[:, 3])
    xz = x / Z
    out = xz[:, None] * w                                                            # mass leaving, per direction
    xn = ((1.0 - th["mu"]) * xz + jnp.roll(out[:, 0], 1, -2) + jnp.roll(out[:, 1], -1, -2)
          + jnp.roll(out[:, 2], 1, -1) + jnp.roll(out[:, 3], -1, -1))
    # conversion between kinds (total mass per cell kept)
    r = th["gr"] * o[2 * C:].reshape(C, C, fam.H, fam.W)
    k = th["kappa"] * jnp.exp(L * jnp.tanh(r / L)) * (1.0 - jnp.eye(C))[:, :, None, None]   # k[c, c']
    Zr = 1.0 + k.sum(1)
    xr = xn / Zr
    return xr + (xr[:, None] * k).sum(0)


def wind_field(a, fam: Family = FAM):
    """E(a): coefficients (2*GW*GW,) -> field (2, H, W) [y-component, x-component]."""
    a = jnp.reshape(a, (2, fam.GW, fam.GW))
    b = fam.H // fam.GW
    up = jnp.repeat(jnp.repeat(a, b, axis=1), b, axis=2)
    return blur(blur(blur(blur(blur(up, 1), 1), 2), 2), 4)


def wind_coeff(nz: Noise, u, fam: Family = FAM):
    """The realised wind coefficients of a tick: a = u + sigma_w * eta (its own sub-stream of the tick)."""
    return u + fam.sigma_w * nz.stream(WIND_STREAM).normal((fam.NW,))


def tick(th, x, nz: Noise, u, fam: Family = FAM):
    """One tick: the wind of the tick, then NSUB substeps."""
    wind = wind_field(wind_coeff(nz, u, fam), fam)

    def body(x, i):
        xi = nz.substep(fam.NSUB, i).normal((fam.C, 4, fam.H, fam.W))
        return substep(th, x, xi, wind, fam), None
    x, _ = lax.scan(body, x, jnp.arange(fam.NSUB))
    return x


def tick_free(th, x, nz: Noise, fam: Family = FAM):
    """A tick with no command (u = 0)."""
    return tick(th, x, nz, jnp.zeros((fam.NW,)), fam)


def init(th, key, fam: Family = FAM):
    g = jax.random.normal(key, (fam.C, fam.H, fam.W))
    g = blur(blur(g, 1), 1)
    g = g / jnp.sqrt(jnp.mean(g * g, axis=(-2, -1), keepdims=True))
    x = jnp.exp(fam.init_contrast * g)
    return x / x.mean((-2, -1), keepdims=True) * th["dens"][:, None, None]


def nats(u, fam: Family = FAM) -> float:
    """Charge of a wind command or a stack of commands."""
    u = np.asarray(u, float)
    return 0.5 * float((u ** 2).sum()) / fam.sigma_w ** 2


def make_level(theta: dict, fam: Family = FAM, name: str = "tnca") -> vw.Level:
    """The world of one theta as a vw.Level (one tick per step; u = wind command, length 2*GW*GW)."""
    th = {k: jnp.asarray(v) for k, v in theta.items()}
    cons = {"mass_total": lambda x: x.sum()}
    if float(np.asarray(theta["kappa"])) == 0.0:
        for c in range(fam.C):
            cons[f"mass_c{c}"] = (lambda c: (lambda x: x[c].sum()))(c)
    return vw.Level(init=lambda p, key: init(p, key, fam), step=lambda p, x, nz, u: tick(p, x, nz, u, fam),
                    input_dim=fam.NW, params=th, conserved=cons,
                    name=f"{name}[C={fam.C},{fam.H}x{fam.W},NSUB={fam.NSUB},sigma={fam.sigma},sigma_w={fam.sigma_w}]")


# ----------------------------------------------------------------------------- coarse views
def block_view(x, G: int = 8):
    """Phi_coarse (the gliders port's definition): block means of every kind and of S^2, (C + 1, G, G)."""
    C, H, W = x.shape
    b = H // G
    m = x.reshape(C, G, b, G, b).mean((2, 4))
    S = x.sum(0).reshape(G, b, G, b)
    return jnp.concatenate([m, (S * S).mean((1, 3))[None]], 0)


def tracker(fam: Family = FAM, K: int = 24, m_min: float = 20.0, sigma: float = 1.0, threshold: float = 2.0,
            max_raw: int = 64, max_kept: int = 32):
    """The declared object view: vw.objects.BlobTracker on the field divided by its mean total density
    (a function of the state alone), bodies = components of blurred S / mean(S) > threshold with at least
    m_min cells' worth of mean density."""
    return vw.objects.BlobTracker(shape=(fam.C, fam.H, fam.W), K=K, m_min=m_min, sigma=sigma, threshold=threshold,
                                  max_raw=max_raw, max_kept=max_kept)


def tracker_field(x):
    return x / jnp.mean(x.sum(0))


# ----------------------------------------------------------------------------- statistics of the weights
def uniform_fixed_point(th, fam: Family = FAM, n: int = 400):
    """The uniform state reached from dens under the noise-free law (conversion can change the mix)."""
    f1 = Family(C=fam.C, H=1, W=1, HID=fam.HID, NSUB=fam.NSUB, sigma=0.0, L=fam.L, GW=1, sigma_w=0.0,
                G1=fam.G1, init_contrast=fam.init_contrast)
    x0 = jnp.asarray(th["dens"])[:, None, None]
    zx, zw = jnp.zeros((fam.C, 4, 1, 1)), jnp.zeros((2, 1, 1))

    def body(x, _):
        xn = substep(th, x, zx, zw, f1)
        return xn, jnp.abs(xn - x).max()
    x, d = lax.scan(body, x0, None, length=n)
    return x[:, 0, 0], d[-1]


def linear_symbol(th, fam: Family = FAM):
    """Linear stability of the uniform state under the noise-free substep: the C x C symbol M(k) of the
    Jacobian (a convolution, by translation invariance) on the full (H, W) wavevector grid.
    Returns dict(xbar (C,), resid, lam (H, W, C) complex eigenvalues)."""
    xbar, resid = uniform_fixed_point(th, fam)
    x0 = jnp.broadcast_to(xbar[:, None, None], (fam.C, fam.H, fam.W))
    zx, zw = jnp.zeros((fam.C, 4, fam.H, fam.W)), jnp.zeros((2, fam.H, fam.W))
    f = lambda x: substep(th, x, zx, zw, fam)

    def col(c):
        d = jnp.zeros((fam.C, fam.H, fam.W)).at[c, 0, 0].set(1.0)
        return jax.jvp(f, (x0,), (d,))[1]                         # (C, H, W): response of every kind
    J = jnp.stack([col(c) for c in range(fam.C)], 1)              # (C_out, C_in, H, W)
    M = jnp.moveaxis(jnp.fft.fft2(J, axes=(-2, -1)), (0, 1), (-2, -1))   # symbol (H, W, C, C)
    if fam.C == 2:                                                # closed form (eigvals has no GPU kernel)
        tr, det = M[..., 0, 0] + M[..., 1, 1], M[..., 0, 0] * M[..., 1, 1] - M[..., 0, 1] * M[..., 1, 0]
        disc = jnp.sqrt(tr * tr - 4.0 * det + 0j)
        lam = jnp.stack([(tr + disc) / 2.0, (tr - disc) / 2.0], -1)
    elif fam.C == 1:
        lam = M[..., 0, :]
    else:
        lam = jnp.linalg.eigvals(M)                               # CPU only
    return dict(xbar=xbar, resid=resid, lam=lam)


def weight_stats(th, fam: Family = FAM):
    """Statistics of theta alone (no simulation), as a flat dict of jnp scalars; vmap over draws.
    lin_*: from the symbol of the uniform state (growth per substep, the fastest mode's wavelength in px
    and its rotation angle per substep); aff_*: the affinity Jacobian d(beta a_c)/d(x_c') at the uniform
    state summed over scales (the response to a uniform change), mob_*: d(gam m_c)/d ln x_c."""
    C, H, W = fam.C, fam.H, fam.W
    sym = linear_symbol(th, fam)
    lam = sym["lam"]
    mod = jnp.abs(lam)
    ky = jnp.fft.fftfreq(H)[:, None] * jnp.ones((1, W))
    kx = jnp.fft.fftfreq(W)[None, :] * jnp.ones((H, 1))
    kk = jnp.sqrt(ky ** 2 + kx ** 2)                              # cycles per px
    modk = jnp.where((kk > 0)[..., None], mod, 0.0)
    best = modk.max(-1)
    idx = jnp.argmax(best)
    kbest = kk.reshape(-1)[idx]
    lbest = lam.reshape(-1, C)[idx]
    j = jnp.argmax(jnp.abs(lbest))
    out = {"lin_growth": jnp.log(jnp.maximum(best.max(), 1e-300)),
           "lin_wavelength": 1.0 / jnp.maximum(kbest, 1e-9),
           "lin_omega": jnp.abs(jnp.angle(lbest[j])),
           "lin_n_unstable": (best > 1.0 + 1e-9).sum().astype(jnp.float64),
           "lin_resid": sym["resid"]}
    # the largest growth among long waves (wavelength >= 8 px), the scale the block view can see
    long = jnp.where((kk > 0) & (kk <= 1.0 / 8.0), best, 0.0)
    out["lin_growth_long"] = jnp.log(jnp.maximum(long.max(), 1e-300))
    xbar = sym["xbar"]
    out["xbar_frac0"] = xbar[0] / xbar.sum()
    fbar = jnp.tile(xbar, 3)

    def outs(f):
        h = jnp.tanh(f @ th["W1"] + th["b1"])
        return h @ th["W2"]
    Jf = jax.jacfwd(outs)(fbar)                                   # (O, F)
    Jx = Jf.reshape(fam.O, 3, C).sum(1)                           # response to a uniform change of each kind
    Jloc = Jf.reshape(fam.O, 3, C)[:, 0]                          # the finest feature scale only
    A = th["beta"] * Jx[:C]                                       # (C, C): d U_aff_c / d x_c'
    for c in range(C):
        for d in range(C):
            out[f"aff_{c}{d}"] = A[c, d]
            out[f"affx_{c}{d}"] = A[c, d] * xbar[d]               # per relative change of kind d
    out["aff_self_max"] = jnp.max(jnp.diag(A) * xbar)
    out["aff_cross_prod"] = A[0, 1] * A[1, 0] * xbar[0] * xbar[1] if C > 1 else jnp.zeros(())
    out["aff_antisym"] = (jnp.abs(A[0, 1] * xbar[1] - A[1, 0] * xbar[0]) if C > 1 else jnp.zeros(()))
    out["aff_loc_self_max"] = jnp.max(jnp.diag(th["beta"] * Jloc[:C]) * xbar)
    Mb = th["gam"] * Jx[C:2 * C]
    out["mob_self_min"] = jnp.min(jnp.diag(Mb) * xbar)
    out["crowd"] = th["alpha"] * xbar.sum() ** 2                  # alpha S^2: crowding potential scale
    out["drive"] = 2.0 * jnp.max(jnp.diag(A) * xbar) - 2.0 * th["alpha"] * xbar.sum() * jnp.max(xbar)
    out["w1_norm"] = jnp.sqrt((th["W1"] ** 2).sum())
    out["w2_aff_norm"] = jnp.sqrt((th["W2"][:, :C] ** 2).sum())
    out["w2_mob_norm"] = jnp.sqrt((th["W2"][:, C:2 * C] ** 2).sum())
    out["hid_sat"] = jnp.mean(jnp.abs(jnp.tanh(fbar @ th["W1"] + th["b1"])))
    for k in SCALARS:
        out[k] = jnp.asarray(th[k], jnp.float64)
    out["log_beta"], out["log_alpha"] = jnp.log(th["beta"]), jnp.log(th["alpha"])
    out["kappa_on"] = (th["kappa"] > 0).astype(jnp.float64)
    for c in range(C):
        out[f"log_dens{c}"] = jnp.log(th["dens"][c])
        out[f"wq{c}"] = th["wq"][c]
    out["log_dens_tot"] = jnp.log(th["dens"].sum())
    return out
