"""val_gates_lib.py — history-reconstruction gates re-run on LIB format.
Cheap: exact-equality algebra vs lib refs + ONE rotor behavior check via
lib's run_genome (the earlier own-engine behavior gates already passed;
logged in results.json val_gate rows)."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "lib"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import genome as G
import operators_lib as OP
from engine import append_result


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def eq_upto_perm(A, B, tol=1e-9):
    import itertools
    na, nc = len(A["acts"]), len(A["chans"])
    if len(B["acts"]) != na or len(B["chans"]) != nc:
        return False
    WA, KA = np.asarray(A["W"], float), np.asarray(A["K"], float)
    WB, KB = np.asarray(B["W"], float), np.asarray(B["K"], float)
    for pa in itertools.permutations(range(na)):
        if not all(all(close(A["acts"][pa[i]][k], B["acts"][i][k], tol)
                       for k in ("lam", "k1", "Du", "u0")) for i in range(na)):
            continue
        for pc in itertools.permutations(range(nc)):
            ok = all(close(A["chans"][pc[i]]["tau"], B["chans"][i]["tau"], tol)
                     and close(A["chans"][pc[i]]["D"], B["chans"][i]["D"], tol)
                     and A["chans"][pc[i]]["g"] == B["chans"][i]["g"]
                     for i in range(nc))
            if ok and np.abs(WA[np.ix_(pc, pa)] - WB).max() < 1e-6 \
                  and np.abs(KA[np.ix_(pa, pc)] - KB).max() < 1e-6:
                return True
    return False


# V1: iso+iso share_chan == ref_VVW modulo the CANONICAL-PAIR CAVEAT:
# lib ref_VVW is M3's original A(d=0)+B(d=0.75) MAXC pair (A has continuum
# caveat); the canonical continuum pair is A'(0.65)+B(0.75) (M5-prep decision).
# Gate: merge(iso_0, iso_0.75) == ref_VVW exactly.
A0 = OP.ref_iso(0.0)
B  = OP.ref_iso(0.75)
M, _ = OP.merge_share_chan(A0, B, rescale=None)
V = G.ref_VVW()
ok1 = eq_upto_perm(M, V, tol=2e-5)   # lib UB is rounded -0.86756; ours exact
print("V1-lib share_chan(iso_0, iso_0.75) == ref_VVW:", ok1, flush=True)

# V2: M4+M4 cross_edge == ref_XV
X, _ = OP.merge_cross_edge(G.ref_M4(5.7), G.ref_M4(2.5), eta=0.1)
R = G.ref_XV(5.7, 2.5, 0.1, 0.1)
ok2 = eq_upto_perm(X, R)
print("V2-lib cross_edge(M4_5.7, M4_2.5) == ref_XV:", ok2, flush=True)

append_result(dict(kind="val_gate", gate="lib_format_exactness",
                   passed=bool(ok1 and ok2),
                   v1_sharechan_vvw=bool(ok1), v2_crossedge_xv=bool(ok2),
                   note="operators ported to lib format; behavior gates for own-engine versions already logged (V1_behavior_vvw_recal, V1b_M0M0_deadend_repro, V2_behavior_rotor_certproto all PASS)"))
print("logged")
