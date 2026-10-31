"""c40 CIPS layered-divide world with isotropic 9-point drift stencils (wrapper; the world file is untouched).

Diffusion in the original is already spectral (-k^2, isotropic). The direction-dependent numerics are the two
explicit drift terms, written as axis-split face fluxes:
  enzyme:      div( chi e(1-e) grad p )   conservative MUSCL (harmonic limiter), volume-filling upwind mobility
  amphiphile:  div( c s grad w )          first-order upwind
Here each is replaced by the isotropic 9-point combination of the SAME face-flux scheme:
  D_iso = 2/3 * (D_(1,0) + D_(0,1)) + 1/6 * (D_(1,1) + D_(1,-1))
where D_d is the original one-direction flux divergence along neighbour offset d (MUSCL slopes along d, face
velocity chi (p_{i+d} - p_i)). For constant mobility this is the isotropic 9-point Laplacian
[1/6 2/3 1/6; 2/3 -10/3 2/3; 1/6 2/3 1/6] (leading truncation error isotropic); it stays conservative
(each D_d telescopes). Everything else (reactions, spectral diffusion, init, parameters, dt) is the original.
"""
import importlib.util
import os

import numpy as np

ORIG = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
_spec = importlib.util.spec_from_file_location("c40_cips_orig_for_iso", ORIG)
_w = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_w)          # reads WORLD_P from the environment, as the original does


def _sh(u, d):
    """u at i + d (periodic)."""
    return np.roll(u, (-d[0], -d[1]), axis=(-2, -1))


def _faces_d(u, d):
    up, um = _sh(u, d), _sh(u, (-d[0], -d[1]))
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, _sh(u - 0.5 * slope, d)


def _vf_dir(e, p, chi, d):
    vf = chi * (_sh(p, d) - p)
    L, R = _faces_d(e, d)
    flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
    return flux - _sh(flux, (-d[0], -d[1]))


def _up_dir(u, w, c, d):
    vf = c * (_sh(w, d) - w)
    flux = np.where(vf > 0, vf * u, vf * _sh(u, d))
    return flux - _sh(flux, (-d[0], -d[1]))


AX, DG = ((1, 0), (0, 1)), ((1, 1), (1, -1))


def vf_flux_div_iso(e, p, chi):
    return (2 / 3) * sum(_vf_dir(e, p, chi, d) for d in AX) + (1 / 6) * sum(_vf_dir(e, p, chi, d) for d in DG)


def up_flux_div_iso(u, w, c):
    return (2 / 3) * sum(_up_dir(u, w, c, d) for d in AX) + (1 / 6) * sum(_up_dir(u, w, c, d) for d in DG)


_w.vf_flux_div = vf_flux_div_iso       # step() looks these names up in the original module's globals
_w.up_flux_div = up_flux_div_iso

META = dict(_w.META, name=_w.META["name"] + "-iso9")
P = _w.P                               # same dict object, so LabWorld.load's P.update reaches the stepper
ops = _w.ops
init, step, fields, damage, _ss_p = _w.init, _w.step, _w.fields, _w.damage, _w._ss_p
