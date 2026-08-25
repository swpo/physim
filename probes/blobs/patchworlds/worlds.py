"""worlds.py — shared world builders + analysis helpers for patchworld tests.

Geometry (locked): N=192 px, dx=0.5 (L=96 lu). Patch B = x-band [24,72) lu
(px [48,144)); patch A = complement. Seam-1 at 48 px, seam-2 at 144 px.
w quoted in PX; w_len = w_px*dx. All logged distances in px (pos_lu * 2).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_lib as P
G = P.G

N, DX, LLU = 192, 0.5, 96.0
BAND = (24.0, 72.0)           # lu
SEAM1_PX, SEAM2_PX = 48.0, 144.0


def build_patch(gA, gB, w_px):
    rho = P.rho_band(N, DX, BAND[0], BAND[1], w_px * DX)
    g, pm = P.blend_genomes(gA, gB, rho)
    return g, pm, rho


def gM0():
    return G.ref_M0()


def gM4(tau):
    return G.ref_M4(tau)


def gM0k1(k1_orig):
    return P.ref_M0_k1(k1_orig)


def px(lu):
    return np.asarray(lu) * 2.0


def lu(px_):
    return np.asarray(px_) * DX


def seed_m0(F, g, x_lu, y_lu):
    return G.poke(F, g, 0, x_lu, y_lu, 2.0, 3.0, DX)


def seed_m4(F, x_lu, y_lu, kick=None, na=1):
    st = P.load_stamp()
    return P.seed_stamp(F, st, x_lu, y_lu, DX, kick=kick, na=na)


def pos_px(res, i=0):
    """(nrec, nblob, 2) unwrapped (y,x) in px; ragged-safe (pads nan)."""
    seq = res[f"pos{i}"]
    nb = max((p.shape[0] for p in seq), default=0)
    out = np.full((len(seq), nb, 2), np.nan)
    for k, p in enumerate(seq):
        if p.size:
            out[k, :p.shape[0]] = p
    return out * 2.0


def speed_series(xy_px, t, half_win=3):
    """central-difference speed (px/tu) of one blob track (nrec,2)."""
    v = np.gradient(xy_px, t, axis=0)
    return np.hypot(v[:, 0], v[:, 1])
