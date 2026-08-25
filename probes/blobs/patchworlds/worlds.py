"""worlds.py — shared world builders + helpers for patchworld tests.

UNITS: everything in lu (= dx1-px, the program's "px"): blob radius ~3, tail
wavelength ~11, d* = 15.4-15.7, w-halo decay sqrt(Dw*theta) = 3.74.
Grid: 96 x 96 lu (192x192 cells at dx=0.5). Patch B = x-band [24,72) lu;
seams at x=24 (seam-1) and x=72 (seam-2). Seam ladder w_tanh = {4,12,24} lu
(10-90%% transition = 2.197*w = {8.8, 26, 53} lu; parent's 8/24/48 ladder).

PAIRS:
  pair_M0_M4(tau_B): A = ref_M0 (tau=3, Dv=1, A=3 static) vs B = ref_M4(tau_B)
    (Dv=4/tau_B, A=4). Blends tau AND Dv (flux-form dD split, litreview-R1
    reference implementation). Aligned vacuum (identical activator params).
  pair_vac(k1B): A = M0 vs B = M0 with k1_orig=k1B — NON-aligned vacua
    (u0 -0.7035 vs -0.7514 at k1B=-0.8), wiring identical.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_lib as P
G = P.G

N, DX, LLU = 192, 0.5, 96.0
BAND = (24.0, 72.0)
SEAM1, SEAM2 = 24.0, 72.0     # lu
WLAD = (4.0, 12.0, 24.0)      # w_tanh lu


def build(gA, gB, w_lu):
    rho = P.rho_band(N, DX, BAND[0], BAND[1], w_lu)
    g, pm = P.blend_genomes(gA, gB, rho)
    return g, pm, rho


def pair_M0_M4(tau_B, w_lu):
    return build(G.ref_M0(), G.ref_M4(tau_B), w_lu)


def pair_vac(k1B, w_lu):
    return build(G.ref_M0(), P.ref_M0_k1(k1B), w_lu)


def rhoB_at(x_lu, w_lu):
    return 0.5 * (np.tanh((x_lu - BAND[0]) / w_lu) + np.tanh((BAND[1] - x_lu) / w_lu))


def seed_m0(F, g, x_lu, y_lu):
    return G.poke(F, g, 0, x_lu, y_lu, 2.0, 3.0, DX)


def seed_m4(F, x_lu, y_lu, kick=None, na=1):
    st = P.load_stamp()
    return P.seed_stamp(F, st, x_lu, y_lu, DX, kick=kick, na=na)


def pos_lu(res, i=0):
    """(nrec, nblob, 2) unwrapped (y,x) in lu; ragged-safe (nan pad)."""
    seq = res[f"pos{i}"]
    nb = max((p.shape[0] for p in seq), default=0)
    out = np.full((len(seq), nb, 2), np.nan)
    for k, p in enumerate(seq):
        if p.size:
            out[k, :p.shape[0]] = p
    return out
