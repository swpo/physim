"""worlds_v3.py — v3 validation-gate bank worlds (b: hand-built positives,
c: anti-gaming probes). NEW module; reconstructs minimal versions from the
certified parameter tables (membrane SUMMARY R3, M4/M5 program certs) —
no locked file edited.

Each builder returns dict(genome, ic (or None), kw (assay_v3 kwargs), note).
ICs are built with the EXISTING dressing machinery (soup_sim.dressed_poke)
on a vacuum state — same convention as the locked soup protocol.

Documented deviations from the certs (all forced by the locked soup assay):
 * L=128 (soup protocol) instead of the membrane/transport L=96.
 * burn-in 500tu doubles as the prerelax (cert used cargo-free prerelax;
   at etaw=0.9 instant-paste was measured clean, membrane R2b).
 * m2_dimer uses the LITERAL M2 point (tau=2.5, Dv=2.0, A=5) — which the
   membrane campaign PROVED dt-artifacted under IMEX dt=0.02 (pairs slide
   through d* and replicate ~2600tu). Kept as specified; the A4s (Dv=1.6)
   variant m2_dimer_a4 is the integrator-honest dimer gas.
"""
import copy, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import genome as G
import soup_sim as SS
import worlds as W1

L_ASSAY = 128.0
DX = 0.5


def _vacuum_ic(g, L=L_ASSAY):
    N = int(round(L / DX))
    return G.state_vacuum(g, N)


def _poke(F, g, act, x, y, kick_px=0.0, ang=0.0):
    return SS.dressed_poke(F, g, act, x, y, DX, kick_px=kick_px,
                           kdir=(np.cos(ang), np.sin(ang)))


# ---------------------------------------------------------------- bank b
def cargo_cell():
    """Membrane R3 'cargo in cell': N10 A4s ring (R=24.91) + motile cargo
    (tau1=5.8) inside, one-way cross-w etaw12=0.9 (ring writes cargo's w).
    Params verbatim from membrane SUMMARY (R1 A4s tau=2.5 Dv=1.6; R3 config
    etaw12=0.9, cargo tau 5.8, kicked at a gap). Expect HIGH s9 (interaction
    at the wall), nonzero t9 (cargo bounces in the cage through void)."""
    g = G.ref_XV(tau1=5.8, tau2=2.5, eta12=0.0, eta21=0.0)
    # ring material A4s: tau2=2.5 -> Dv2=4/tau2=1.6 (ref_XV already A=4)
    Wm = np.asarray(g["W"], float)
    Wm[2] = [1.0, 0.9]          # w1 drive: u1 + etaw12 * u2 (one-way)
    g["W"] = Wm.tolist()
    g["id"] = "b_cargo_cell"
    g["provenance"]["source"] = "membrane R3 reconstruction (etaw12=0.9)"
    F = _vacuum_ic(g)
    cy = cx = L_ASSAY / 2
    R = 24.91
    N_RING = 10
    for j in range(N_RING):
        th = 2 * np.pi * j / N_RING
        F = _poke(F, g, 1, cx + R * np.cos(th), cy + R * np.sin(th))
    # cargo at center, kicked toward the midpoint gap between blobs 0 and 1
    gap_ang = np.pi / N_RING
    F = _poke(F, g, 0, cx, cy, kick_px=0.5, ang=gap_ang)
    return dict(genome=g, ic=F, kw=dict(cap=2500.0),
                note="N10 A4s ring + tau5.8 cargo, etaw12=0.9 one-way")


def m5_trains():
    """M4/M5 'trains through void': ref_M4 at tau=5.7 (pair-only drift zone
    tau in (5.636, 5.748): molecules move, singles park). IC: one 3-blob
    train (spacing 14.78, the certified moving-bond sep) kicked +x, plus 3
    parked single cargoes on its path (relay-tug pickup reconstruction,
    no environment saw — pure pair physics). Expect HIGH t9 (traversal),
    bond events on every pickup (e9), speed/bond phenotype split (r9)."""
    g = G.ref_M4(tau=5.7)
    g["id"] = "b_m5_trains"
    F = _vacuum_ic(g)
    y0 = 64.0
    sep = 14.78
    for j in range(3):
        F = _poke(F, g, 0, 20.0 + j * sep, y0, kick_px=0.5, ang=0.0)
    for xc in (70.0, 92.0, 114.0):
        F = _poke(F, g, 0, xc, y0)
    # a second, y-offset train going the other way (richer encounters)
    for j in range(2):
        F = _poke(F, g, 0, 100.0 - j * sep, 24.0, kick_px=0.5, ang=np.pi)
    return dict(genome=g, ic=F, kw=dict(cap=5000.0),
                note="tau=5.7 pair-only zone: 3-train + parked cargoes")


def m2_dimer():
    """LITERAL M2 dimer gas (M0 + Dv=2.0, tau=2.5 = A=5 binding point):
    5 dimers at d0=16 + 2 singles. KNOWN dt=0.02 artifact (A5 pairs slide
    through d* and replicate ~2600tu) — kept per spec; see m2_dimer_a4."""
    g = G.ref_M0()
    g["chans"][0]["tau"] = 2.5
    g["chans"][0]["D"] = 2.0
    g["id"] = "b_m2_dimer"
    g["provenance"]["source"] = "M2 P7s binding point (A=5)"
    F = _vacuum_ic(g)
    rng = np.random.default_rng(7)
    centers = [(24, 24), (24, 88), (64, 56), (100, 24), (96, 96)]
    for (cx, cy) in centers:
        ang = rng.uniform(0, 2 * np.pi)
        dx2, dy2 = 8.0 * np.cos(ang), 8.0 * np.sin(ang)
        F = _poke(F, g, 0, cx - dx2, cy - dy2)
        F = _poke(F, g, 0, cx + dx2, cy + dy2)
    F = _poke(F, g, 0, 48.0, 108.0)
    F = _poke(F, g, 0, 120.0, 64.0)
    return dict(genome=g, ic=F, kw=dict(cap=2500.0),
                note="A=5 dimer gas (5 pairs d0=16 + 2 singles)")


def m2_dimer_a4():
    """Integrator-honest dimer gas: A4s statics (tau=2.5, Dv=1.6), the
    certified dt=0.02 bond material (membrane rings = N of these bonds)."""
    d = m2_dimer()
    g = d["genome"]
    g["chans"][0]["D"] = 1.6
    g["id"] = "b_m2_dimer_a4"
    g["provenance"]["source"] = "A4s bond material (membrane R1)"
    # rebuild IC with the corrected genome (dressing uses W only; same W)
    return dict(genome=g, ic=d["ic"], kw=dict(cap=2500.0),
                note="A4s dimer gas (dt=0.02-certified bonds)")


# ---------------------------------------------------------------- bank c
def dead_world():
    """Anti-gaming: subcritical chemistry (every lam scaled 0.2x, vacuum
    re-polished). Blobs cannot persist -> C1 gate -> C9 = 0."""
    import json
    fc = os.path.join(os.path.dirname(HERE), "deepsearch", "v2_analysis",
                      "film_candidates", "p6g8_033.json")
    g = json.load(open(fc))["genome"]
    for a in g["acts"]:
        a["lam"] = 0.2 * a["lam"]
        roots = G.cubic_roots(a["lam"], a["k1"])
        a["u0"] = G.polish_root(a["lam"], a["k1"],
                                min(roots, key=lambda r: abs(r - a["u0"])))
    g["id"] = "c_dead"
    return dict(genome=g, ic=None, kw=dict(cap=2500.0),
                note="champion chemistry, lam x0.2 (subcritical)")


def frozen_lattice():
    """Anti-gaming: permanent bond lattice. A4s bond material, 8x8 grid at
    the bond length d*=15.4 -> every pair bonded forever: e9 must be ~0
    (frozen_frac ~ 1), t9 disp ~ 0."""
    g = G.ref_M0()
    g["chans"][0]["tau"] = 2.5
    g["chans"][0]["D"] = 1.6
    g["id"] = "c_frozen"
    g["provenance"]["source"] = "A4s lattice (bond-basin grid, wrap-exact)"
    F = _vacuum_ic(g)
    sp = 16.0                    # 128/8: wrap-exact; inside bond basin
    for iy in range(8):
        for ix in range(8):
            F = _poke(F, g, 0, 8.0 + ix * sp, 8.0 + iy * sp)
    return dict(genome=g, ic=F, kw=dict(cap=2500.0),
                note="8x8 A4s grid at 16px (permanent bonds, wrap-exact)")


def noise_soup():
    """Anti-gaming: churning speckle with no persistent identity. m0
    chemistry pushed into the replication corner (K w-coupling 1.5 -> 2.5,
    vacuum-exact change) + 3x working noise: blobs keep nucleating/dying,
    tracks shred -> d7b clusters cannot persist -> r9 ~ 0 (and e9 flicker).
    Deliberately ALIVE (the C1 gate must not be the thing that kills it)."""
    g = G.ref_M0()
    K = np.asarray(g["K"], float)
    K[0, 1] = 2.5                # M0 neighbor note: k4=2.5 -> spot soup
    g["K"] = K.tolist()
    g["id"] = "c_noise"
    # v1 of this probe used noise=6e-3: world died <405tu (all_dead) — that
    # degenerates into the dead-world case (C1 gate), not the r9 test.
    # WORKING noise keeps the replication churn alive: r9 must do the kill.
    return dict(genome=g, ic=None, kw=dict(cap=2500.0),
                note="m0 K_w=2.5 spot soup, working noise (alive churn)")


BANK_B = dict(cargo_cell=cargo_cell, m5_trains=m5_trains,
              m2_dimer=m2_dimer, m2_dimer_a4=m2_dimer_a4)
BANK_C = dict(dead=dead_world, frozen=frozen_lattice, noise=noise_soup)
