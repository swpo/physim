"""Small numerics toolbox shared by world files (all periodic, spectral where possible).

Nothing here is required; copy what you need into a world file if you want it frozen.
"""
from __future__ import annotations

import numpy as np
import scipy.fft as sfft

WORKERS = 2  # FFT threads per process; the containers have 4 cores shared by everyone


def wavenumbers(H, W, dx=1.0):
    """Angular wavenumber grids (ky, kx) matching rfft2 output, shape (H, W//2+1)."""
    ky = 2 * np.pi * sfft.fftfreq(H, d=dx)[:, None]
    kx = 2 * np.pi * sfft.rfftfreq(W, d=dx)[None, :]
    return ky, kx


def rfft2(x):
    return sfft.rfft2(x, axes=(-2, -1), workers=WORKERS)


def irfft2(X, shape):
    return sfft.irfft2(X, s=shape, axes=(-2, -1), workers=WORKERS)


def lap_symbol(H, W, dx=1.0):
    """Spectral Laplacian symbol -k^2."""
    ky, kx = wavenumbers(H, W, dx)
    return -(kx ** 2 + ky ** 2)


def laplacian(u, dx=1.0):
    """5-point periodic Laplacian (works on (..., H, W))."""
    return (np.roll(u, 1, -1) + np.roll(u, -1, -1) + np.roll(u, 1, -2) + np.roll(u, -1, -2) - 4 * u) / dx ** 2


def grad(u, dx=1.0):
    """Central-difference periodic gradient, returns (d/dy, d/dx)."""
    gy = (np.roll(u, -1, -2) - np.roll(u, 1, -2)) / (2 * dx)
    gx = (np.roll(u, -1, -1) - np.roll(u, 1, -1)) / (2 * dx)
    return gy, gx


def div(fy, fx, dx=1.0):
    """Central-difference periodic divergence of a vector field."""
    return (np.roll(fy, -1, -2) - np.roll(fy, 1, -2) + np.roll(fx, -1, -1) - np.roll(fx, 1, -1)) / (2 * dx)


def upwind_flux_div(rho, vy, vx, dx=1.0):
    """Divergence of rho*v with first-order upwinding (conservative, positivity friendly).

    v components are taken at cell centres and averaged to faces.
    """
    def face(v, axis):
        return 0.5 * (v + np.roll(v, -1, axis))

    out = np.zeros_like(rho)
    for v, axis in ((vy, -2), (vx, -1)):
        vf = face(v, axis)                       # velocity on face i+1/2
        up = np.where(vf > 0, rho, np.roll(rho, -1, axis))
        flux = vf * up                           # flux through face i+1/2
        out += (flux - np.roll(flux, 1, axis)) / dx
    return out


def radial_grid(H, W):
    """Periodic distance-from-origin grid (origin at [0, 0]), for building FFT kernels."""
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    return np.sqrt(x ** 2 + y ** 2)


def bell(x, m, s):
    return np.exp(-((x - m) / s) ** 2 / 2)


def ring_kernel(H, W, R, peaks=(1.0,), width=0.15, kind="gauss"):
    """Lenia shell kernel of radius R with len(peaks) concentric rings, normalized to sum 1.

    kind="gauss": bell(frac, 0.5, width) per ring (Lenia tutorial convention).
    kind="exp":   exp(4 - 1/(frac*(1-frac))) per ring (Chan 2019 exponential core).
    Returns the rfft2 of the kernel, ready for fft_conv.
    """
    D = radial_grid(H, W) / R
    B = len(peaks)
    Kr = np.zeros_like(D)
    inside = D < 1
    idx = np.minimum((D * B).astype(int), B - 1)
    frac = (D * B) % 1.0
    if kind == "gauss":
        shell = bell(frac, 0.5, width)
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            shell = np.where((frac > 0) & (frac < 1), np.exp(4 - 1 / (frac * (1 - frac))), 0.0)
    Kr[inside] = (np.asarray(peaks)[idx] * shell)[inside]
    Kr /= Kr.sum()
    return rfft2(Kr)


def gauss_kernel(H, W, sigma):
    """Normalized periodic Gaussian blur kernel (rfft2)."""
    r = radial_grid(H, W)
    K = np.exp(-r ** 2 / (2 * sigma ** 2))
    return rfft2(K / K.sum())


def fft_conv(x, Kf):
    """Periodic convolution of x (..., H, W) with a precomputed rfft2 kernel."""
    shape = x.shape[-2:]
    return irfft2(rfft2(x) * Kf, shape)


def growth_gauss(u, m, s):
    """Lenia growth mapping in [-1, 1]."""
    return 2 * bell(u, m, s) - 1


def disk(H, W, cy, cx, r):
    """Boolean periodic disk mask."""
    y = np.arange(H)[:, None]
    x = np.arange(W)[None, :]
    dy = np.minimum(np.abs(y - cy), H - np.abs(y - cy))
    dx = np.minimum(np.abs(x - cx), W - np.abs(x - cx))
    return dy ** 2 + dx ** 2 <= r ** 2
