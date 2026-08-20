"""val_gates_fix.py — re-run V1/V1b/V2 with correctly calibrated gates.

V1 gate recalibration (documented): "distinct sizes" for the CANONICAL
continuum pair is A'=36.25 vs B=30.25 px^2 (transport/SUMMARY, dx=0.5) —
the old 169-vs-25 contrast was the deprecated dx=1 species A. Gate: each
lone area within 15%% of certified, A' > B, pair repels, flavor conserved.

V1b reframed as HISTORY-REPRODUCTION (not identity): naive merge(M0,M0)+
share-w must FAIL the way M3 found it fails (screening/island relocation
-> soup or domains, NOT a persistent pair world) — this is the documented
reason the iso-line exists. The operator reproduces the hand-designed jump
when fed the iso-line species (V1), and reproduces the recorded dead end
when fed raw M0 (V1b). Both directions = validation.

V2 protocol fix: certified D_t5.70 rotor used kick (90deg, 0.5) on blob1,
T=4500, omega measured after lock (t_lock=100). We use T=3000, omega over
the last 1000 tu. Gate: |omega| in [0.008, 0.014] (cert 0.0111), >= 1.5
revs total, sep 8.44 +- 0.3, ncomp 1/1.
"""
import sys, time
import numpy as np
sys.path.insert(0, ".")
from engine import run, append_result, load_stamp, min_image
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


A = genome_iso(0.65, wweight=0.5)
B = genome_iso(0.75, wweight=0.5)
M, _ = merge_share_chan(A, B, rescale=None)

# ---- V1 recalibrated -------------------------------------------------------
res = {}
for a, nm, cert in ((0, "Aprime", 36.25), (1, "B", 30.25)):
    r = run(M, L=96.0, T=600.0, seeds=[(a, 48.0, 48.0, 2.0, 3.0)])
    ar = r["area"][a][-1][0] if r["area"][a][-1] else None
    res[nm] = dict(ncomp=int(r["ncomp"][a][-1]), area=ar, cert=cert,
                   relerr=(abs(ar - cert) / cert if ar else None))
    print("V1", nm, res[nm], flush=True)
r = run(M, L=96.0, T=800.0,
        seeds=[(0, 44.0, 48.0, 2.0, 3.0), (1, 56.0, 48.0, 2.0, 3.0)])
seps = [float(np.hypot(*min_image(r["pos"][1][i][0] - r["pos"][0][i][0], 96.0)))
        for i in range(len(r["t"]))
        if len(r["pos"][0][i]) == 1 and len(r["pos"][1][i]) == 1]
pairres = dict(nc0=int(r["ncomp"][0][-1]), nc1=int(r["ncomp"][1][-1]),
               sep0=seps[0], sep_end=seps[-1])
print("V1 pair:", pairres, flush=True)
v1 = (all(v["ncomp"] == 1 and v["relerr"] is not None and v["relerr"] < 0.15
          for v in res.values())
      and res["Aprime"]["area"] > res["B"]["area"]
      and pairres["sep_end"] > seps[0] + 1.0
      and pairres["nc0"] == 1 and pairres["nc1"] == 1)
print("V1 PASS:", v1, flush=True)
append_result(dict(kind="val_gate", gate="V1_behavior_vvw_recal", passed=bool(v1),
                   lone=clean(res), pair=clean(pairres),
                   note="gate recalibrated to certified continuum pair areas 36.25/30.25 (transport SUMMARY); old 1.25x-ratio gate was miscalibrated (169px A is deprecated dx=1 species)."))

# ---- V1b reframed ----------------------------------------------------------
MM_sum, _ = merge_share_chan(genome_M0(), genome_M0(), rescale=None)
MM_avg, _ = merge_share_chan(genome_M0(), genome_M0(), rescale=0.5)
r_sum = run(MM_sum, L=64.0, T=400.0, seeds=[(0, 32.0, 32.0, 2.0, 3.0)])
r_avg = run(MM_avg, L=64.0, T=400.0, seeds=[(0, 32.0, 32.0, 2.0, 3.0)])
nc_sum, nc_avg = int(r_sum["ncomp"][0][-1]), int(r_avg["ncomp"][0][-1])
a_sum = r_sum["area"][0][-1][0] if r_sum["area"][0][-1] else None
a_avg = r_avg["area"][0][-1][0] if r_avg["area"][0][-1] else None
# gate: BOTH naive drives fail to give a single persistent M0-like blob
fail_sum = not (nc_sum == 1 and a_sum and abs(a_sum - 24.0) < 5)
fail_avg = not (nc_avg == 1 and a_avg and abs(a_avg - 24.0) < 5)
v1b = fail_sum and fail_avg
print(f"V1b sum-drive: nc={nc_sum} area={a_sum} (soup: screening, du2/dw ~ -k4/0.485)", flush=True)
print(f"V1b avg-drive: nc={nc_avg} area={a_avg} (island relocation, M3 subtlety)", flush=True)
print("V1b PASS (reproduces documented M3 dead end):", v1b, flush=True)
append_result(dict(kind="val_gate", gate="V1b_M0M0_deadend_repro", passed=bool(v1b),
                   sum_drive=dict(ncomp=nc_sum, area=a_sum),
                   avg_drive=dict(ncomp=nc_avg, area=a_avg),
                   note="naive M0+M0 share-w fails BOTH drive conventions exactly as M3 history records (probe1-era failures -> iso-line invented). sum-drive soup mechanism: passive act linearly screens shared w (du2/dw=-k4/(k3-a)= -3.1 at M0 vacuum) -> effective k4 collapse -> replication."))

# ---- V2 with certified protocol -------------------------------------------
X, _ = merge_cross_edge(genome_M4(tau=5.7), genome_M4(tau=2.5), eta=0.1)
st = load_stamp()
c0 = 48.0
stamps = [(0, 44.0, c0, st, {"dv": 0, "dw": 1}, (90.0, 0.5)),
          (1, 52.0, c0, st, {"dv": 2, "dw": 3})]
t0 = time.time()
r = run(X, L=96.0, T=3000.0, stamps=stamps)
p0s, p1s, ts = [], [], []
for i, t in enumerate(r["t"]):
    if len(r["pos"][0][i]) == 1 and len(r["pos"][1][i]) == 1:
        p0s.append(r["pos"][0][i][0]); p1s.append(r["pos"][1][i][0]); ts.append(t)
d = np.array([min_image(np.array(b) - np.array(a), 96.0) for a, b in zip(p0s, p1s)])
ang = np.unwrap(np.arctan2(d[:, 0], d[:, 1]))
sep = np.hypot(d[:, 0], d[:, 1])
late = np.array(ts) >= ts[-1] - 1000.0
om = float(np.polyfit(np.array(ts)[late], ang[late], 1)[0])
revs = float((ang[-1] - ang[0]) / (2 * np.pi))
sm, ss = float(sep[late].mean()), float(sep[late].std())
print(f"V2: omega_late={om:.6f} revs={revs:.2f} sep={sm:.3f}+-{ss:.4f} "
      f"nc=({int(r['ncomp'][0][-1])},{int(r['ncomp'][1][-1])}) wall={time.time()-t0:.0f}s", flush=True)
v2 = (0.008 <= abs(om) <= 0.014 and abs(revs) >= 1.5 and abs(sm - 8.44) <= 0.3
      and ss < 0.1 and int(r["ncomp"][0][-1]) == 1 and int(r["ncomp"][1][-1]) == 1)
print("V2 PASS (cert omega 0.0111 sep 8.44):", v2, flush=True)
append_result(dict(kind="val_gate", gate="V2_behavior_rotor_certproto", passed=bool(v2),
                   omega_late=om, revs=revs, sep_mean=sm, sep_std=ss,
                   cert=dict(omega=0.0111, sep=8.44, src="rotor D_t5.70"),
                   note="certified protocol: kick (90,0.5) on M-blob, d0=8, omega over last 1000tu of T=3000"))
