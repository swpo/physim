"""val_history.py — VALIDATION GATE: operators must reconstruct our own
hand-designed history before any evolution (mandate).

V1 vvw: merge(iso_A', iso_B) + share_chan == genome_vvw_cert EXACT up to
        channel permutation; assays: both species persist with DISTINCT
        sizes (~36 vs ~25 px^2), A-B pair REPELS, flavor conserved.
V1b   : merge(M0, M0) physics check — rescale=None (sum-drive): lone spot
        behaves EXACTLY like M0; rescale=0.5 (M3 avg-drive): lone M0-point
        spot must DIE (certified island-relocation subtlety, M3 SUMMARY).
V2 xv : merge(M4 tau=5.7, M4 tau=2.5) + cross_edge(eta=0.1) ==
        genome_xv_cert EXACT; assay: stamped heterodimer at d0=8 ROTATES
        (|omega| ~ 0.0111 certified; gate: 0.008-0.014 and >= 1.5 revs,
        sep 8.44 +- 0.3, both ncomp stay 1).
"""
import sys, time, itertools
import numpy as np
sys.path.insert(0, ".")
from engine import run, funnel_g0, append_result, load_stamp, min_image
from refs import genome_M0, genome_M4, genome_iso, genome_vvw_cert, genome_xv_cert
from operators import merge_share_chan, merge_cross_edge


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(x) for x in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


def genome_equal_upto_perm(A, B, tol=1e-10):
    """Equality up to permutation of channels AND acts."""
    na, nc = len(A["acts"]), len(A["chans"])
    if len(B["acts"]) != na or len(B["chans"]) != nc:
        return False, "shape"
    WA, KA = np.asarray(A["W"], float), np.asarray(A["K"], float)
    WB, KB = np.asarray(B["W"], float), np.asarray(B["K"], float)
    for pa in itertools.permutations(range(na)):
        oka = all(all(abs(A["acts"][pa[i]][k] - B["acts"][i][k]) < tol
                      for k in ("lam", "k1", "Du")) and
                  abs(A["u0"][pa[i]] - B["u0"][i]) < tol for i in range(na))
        if not oka:
            continue
        for pc in itertools.permutations(range(nc)):
            okc = True
            for i in range(nc):
                ca, cb = A["chans"][pc[i]], B["chans"][i]
                if abs(ca["tau"] - cb["tau"]) > tol or abs(ca["D"] - cb["D"]) > tol \
                        or ca["g"] != cb["g"]:
                    okc = False; break
            if not okc:
                continue
            if np.max(np.abs(WA[np.ix_(pc, pa)] - WB)) < tol and \
                    np.max(np.abs(KA[np.ix_(pa, pc)] - KB)) < tol:
                return True, (pa, pc)
    return False, "no_perm"


def omega_meas(r, L):
    """Angular velocity of the act0-act1 separation axis, late-2/3 fit."""
    p0s, p1s, ts = [], [], []
    for i, t in enumerate(r["t"]):
        if len(r["pos"][0][i]) == 1 and len(r["pos"][1][i]) == 1:
            p0s.append(r["pos"][0][i][0]); p1s.append(r["pos"][1][i][0]); ts.append(t)
    if len(ts) < 12:
        return None
    d = np.array([min_image(np.array(b) - np.array(a), L) for a, b in zip(p0s, p1s)])
    ang = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))
    sep = np.hypot(d[:, 0], d[:, 1])
    i0 = len(ts) // 3
    A = np.polyfit(ts[i0:], ang[i0:], 1)
    return dict(omega=float(A[0]), revs=float((ang[-1] - ang[0]) / (2 * np.pi)),
                sep_mean=float(sep[i0:].mean()), sep_std=float(sep[i0:].std()))


T0 = time.time()

# ---------------------------------------------------------------- V1 algebra
A = genome_iso(0.65, wweight=0.5)
B = genome_iso(0.75, wweight=0.5)
M, prov = merge_share_chan(A, B, rescale=None)
ok1, perm = genome_equal_upto_perm(M, genome_vvw_cert())
print("V1 EXACT (share_chan -> vvw_cert up to perm):", ok1, perm, flush=True)
append_result(dict(kind="val_gate", gate="V1_exact_sharechan", passed=bool(ok1),
                   perm=str(perm), merged_prov=clean(prov)))

# ---------------------------------------------------------------- V2 algebra
X, prov2 = merge_cross_edge(genome_M4(tau=5.7), genome_M4(tau=2.5), eta=0.1)
ok2, perm2 = genome_equal_upto_perm(X, genome_xv_cert(5.7, 2.5, 0.1))
print("V2 EXACT (cross_edge -> xv_cert):", ok2, perm2, flush=True)
append_result(dict(kind="val_gate", gate="V2_exact_crossedge", passed=bool(ok2),
                   perm=str(perm2), merged_prov=clean(prov2)))

# ------------------------------------------------------------- V1 behavior
# lone pokes per species then pair encounter, merged genome M (L=96 cert box)
res = {}
for a, nm in ((0, "Aprime"), (1, "B")):
    r = run(M, L=96.0, T=600.0, seeds=[(a, 48.0, 48.0, 2.0, 3.0)])
    ar = r["area"][a][-1][0] if r["area"][a][-1] else None
    res[nm] = dict(status=r["status"], ncomp=int(r["ncomp"][a][-1]), area=ar,
                   other_ncomp=int(r["ncomp"][1 - a][-1]))
    print(f"V1 lone {nm}: {res[nm]}", flush=True)
r = run(M, L=96.0, T=800.0,
        seeds=[(0, 44.0, 48.0, 2.0, 3.0), (1, 56.0, 48.0, 2.0, 3.0)])
seps = []
for i in range(len(r["t"])):
    if len(r["pos"][0][i]) == 1 and len(r["pos"][1][i]) == 1:
        seps.append(float(np.hypot(*min_image(
            r["pos"][1][i][0] - r["pos"][0][i][0], 96.0))))
pairres = dict(status=r["status"], nc0=int(r["ncomp"][0][-1]),
               nc1=int(r["ncomp"][1][-1]), sep0=seps[0] if seps else None,
               sep_end=seps[-1] if seps else None)
print("V1 pair A-B d0=12:", pairres, flush=True)
sizes_ok = (res["Aprime"]["area"] and res["B"]["area"]
            and res["Aprime"]["area"] > 1.25 * res["B"]["area"])
repel_ok = pairres["sep_end"] and pairres["sep_end"] > seps[0] + 1.0
flavor_ok = pairres["nc0"] == 1 and pairres["nc1"] == 1
v1b_pass = bool(res["Aprime"]["ncomp"] == 1 and res["B"]["ncomp"] == 1
                and sizes_ok and repel_ok and flavor_ok)
print("V1 BEHAVIOR PASS:", v1b_pass, flush=True)
append_result(dict(kind="val_gate", gate="V1_behavior_vvw", passed=v1b_pass,
                   lone=clean(res), pair=clean(pairres),
                   note="distinct sizes + repulsion + flavor conserved"))

# ------------------------------------------------- V1b M0+M0 physics checks
MM_sum, _ = merge_share_chan(genome_M0(), genome_M0(), rescale=None)
MM_avg, _ = merge_share_chan(genome_M0(), genome_M0(), rescale=0.5)
r_sum = run(MM_sum, L=64.0, T=400.0, seeds=[(0, 32.0, 32.0, 2.0, 3.0)])
r_avg = run(MM_avg, L=64.0, T=400.0, seeds=[(0, 32.0, 32.0, 2.0, 3.0)])
a_sum = r_sum["area"][0][-1][0] if r_sum["area"][0][-1] else None
a_avg = r_avg["area"][0][-1][0] if r_avg["area"][0][-1] else None
print(f"V1b M0+M0 sum-drive lone: ncomp={int(r_sum['ncomp'][0][-1])} area={a_sum}"
      f" (expect EXACT M0: 1, 24.0)", flush=True)
print(f"V1b M0+M0 avg-drive lone: ncomp={int(r_avg['ncomp'][0][-1])} area={a_avg}"
      f" (expect DIE/relocate per M3 subtlety)", flush=True)
v1c_pass = (int(r_sum["ncomp"][0][-1]) == 1 and a_sum and abs(a_sum - 24.0) < 3.0
            and int(r_avg["ncomp"][0][-1]) == 0)
append_result(dict(kind="val_gate", gate="V1b_M0M0_drive_convention",
                   passed=bool(v1c_pass),
                   sum_drive=dict(ncomp=int(r_sum["ncomp"][0][-1]), area=a_sum),
                   avg_drive=dict(ncomp=int(r_avg["ncomp"][0][-1]), area=a_avg),
                   note="sum-drive lone spot == exact M0; avg-drive M0 point dies (island relocation, M3 SUMMARY)"))

# ------------------------------------------------------------- V2 behavior
st = load_stamp()
c0 = 48.0
stamps = [(0, c0 - 4.0, c0, st, {"dv": 0, "dw": 1}),
          (1, c0 + 4.0, c0, st, {"dv": 2, "dw": 3})]
r = run(X, L=96.0, T=1500.0, stamps=stamps)
om = omega_meas(r, 96.0)
print("V2 rotor run:", r["status"], "nc:", int(r["ncomp"][0][-1]),
      int(r["ncomp"][1][-1]), "omega:", om, f"wall={r['wall_s']:.0f}s", flush=True)
v2b_pass = bool(om and 0.008 <= abs(om["omega"]) <= 0.014 and abs(om["revs"]) >= 1.5
                and abs(om["sep_mean"] - 8.44) <= 0.3
                and int(r["ncomp"][0][-1]) == 1 and int(r["ncomp"][1][-1]) == 1)
print("V2 BEHAVIOR PASS (certified omega=0.0111 sep=8.44):", v2b_pass, flush=True)
append_result(dict(kind="val_gate", gate="V2_behavior_rotor", passed=v2b_pass,
                   omega=clean(om), status=r["status"],
                   cert=dict(omega=0.0111, sep=8.44),
                   wall_s=r["wall_s"]))

print(f"ALL GATES done in {time.time()-T0:.0f}s")
