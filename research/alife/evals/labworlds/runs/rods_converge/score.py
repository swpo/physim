"""Refinement nulls from saved ensembles.

A test has two native ensembles A, B (8 members each, independent seeds) at the candidate resolution and one refined
ensemble R (8 members, its own seed) at the refined resolution, all from the same prepared state and program.
Per program, window w (readouts 1..w tu) and score group (device0, device1, global):
  ratio8   ES(R, A) / ES(B, A)  (A as truth, the evaluation's ratio with an 8-member control)
  null     permutation band from the 16 natives: split A u B into X(5), Y(5), T(6); ES(X, T) / ES(Y, T) (2000 splits)
  refined  ES(R5, T) / ES(Y, T) on the same splits, R5 a random 5 of R's 8
  pass     median(refined) inside the null's 5-95% band
ES is PhySim's energy score (blobround6_eval._energy_score: rms distance, self-pairs included) on readouts divided
by frozen scales: per field for the probes (sd over members, times and nodes) and per field and slot for the global
sensor (mean om is identically 0: scale 1), from the calibration ensemble CAL (sham, dt 0.05, 128^2, seed 101: native B of the first test).
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rc
from ens import path
from physim.blobround6_eval import _energy_score

CAL = ("sham", 0.05, 128, 101)
WINDOWS = (10, 25, 50)
TESTS = [  # label, program, native A, native B, refined R   (dt, n, seed); every ensemble has its own seed
    ("time dt0.05", "sham", (0.05, 128, 202), (0.05, 128, 101), (0.025, 128, 303)),
    ("time dt0.05", "surf", (0.05, 128, 202), (0.05, 128, 101), (0.025, 128, 303)),
    ("time dt0.025", "sham", (0.025, 128, 303), (0.025, 128, 404), (0.0125, 128, 505)),
    ("time dt0.025", "surf", (0.025, 128, 303), (0.025, 128, 404), (0.0125, 128, 505)),
    # sensitivity control: a sham ensemble (ignore actions) as the "refined" arm against the surf natives
    ("control ignore-actions", "surf", (0.05, 128, 202), (0.05, 128, 101), (0.025, 128, 303, "sham")),  # own seed; dt shown not to matter
    ("space n128 dt0.05", "sham", (0.05, 128, 202), (0.05, 128, 101), (0.05, 192, 606)),
    ("space n128 dt0.05", "surf", (0.05, 128, 202), (0.05, 128, 101), (0.05, 192, 606)),
    ("space n192 dt0.05", "sham", (0.05, 192, 606), (0.05, 192, 707), (0.05, 256, 808)),
    ("space n128 dt0.025", "sham", (0.025, 128, 303), (0.025, 128, 404), (0.025, 192, 606)),
    ("space n128 dt0.025", "surf", (0.025, 128, 303), (0.025, 128, 404), (0.025, 192, 606)),
]


def load(program, key):
    if len(key) == 4:              # (dt, n, seed, program): an arm from another program (sensitivity control)
        program, key = key[3], key[:3]
    z = np.load(path(program, *key))
    return {k: z[k] for k in z.files}


def scales():
    z = load(CAL[0], CAL[1:])
    sc = {g: z[g].std(axis=(0, 1, 3))[:, None] + 1e-12 for g in ("device0", "device1")}
    sc["global"] = z["global"].std(axis=(0, 1)) + 1e-12
    sc["global"][5, 0] = 1.0
    return sc


def flat(a, g, w, sc):
    return (a[:, :w] / sc[g][None, None]).reshape(len(a), -1)


def dist(X):
    """Pairwise rms distances between rows."""
    sq = (X * X).sum(1)
    d2 = np.maximum(sq[:, None] + sq[None, :] - 2 * X @ X.T, 0)
    np.fill_diagonal(d2, 0)
    return np.sqrt(d2 / X.shape[1])


def es_sub(D, P, T):
    return D[np.ix_(P, T)].mean() - 0.5 * D[np.ix_(P, P)].mean()


def test(program, A, B, R, sc, nperm=2000, seed=0):
    a, b, r = load(program, A), load(program, B), load(program, R)
    rng = np.random.default_rng(seed)
    out = {}
    for w in WINDOWS:
        for g in rc.GROUPS:
            Xa, Xb, Xr = (flat(z[g], g, w, sc) for z in (a, b, r))
            full = _energy_score(Xr, Xa) / _energy_score(Xb, Xa)
            D = dist(np.concatenate([Xa, Xb, Xr]))
            # exact check of the fast ES against PhySim's on the full sets
            assert abs(es_sub(D, np.arange(16, 24), np.arange(8)) - _energy_score(Xr, Xa)) < 1e-6 * max(1, _energy_score(Xr, Xa))
            nul, ref = [], []
            for _ in range(nperm):
                idx = rng.permutation(16)
                X, Y, T = idx[:5], idx[5:10], idx[10:]
                R5 = 16 + rng.choice(8, 5, replace=False)
                base = es_sub(D, Y, T)
                nul.append(es_sub(D, X, T) / base)
                ref.append(es_sub(D, R5, T) / base)
            nul, ref = np.array(nul), np.array(ref)
            lo, hi = np.percentile(nul, [5, 95])
            med = float(np.median(ref))
            out[f"{w}tu/{g}"] = dict(ratio8=round(float(full), 3), null_5_95=[round(float(lo), 3), round(float(hi), 3)],
                                     refined_median=round(med, 3),
                                     refined_5_95=[round(float(x), 3) for x in np.percentile(ref, [5, 95])],
                                     frac_refined_above_null95=round(float((ref > hi).mean()), 3),
                                     es_native=round(float(_energy_score(Xb, Xa)), 4),
                                     passed=bool(lo <= med <= hi))
    return out


if __name__ == "__main__":
    sc = scales()
    res = dict(scales={g: v.round(6).tolist() for g, v in sc.items()}, tests={})
    for label, program, A, B, R in TESTS:
        if not all(path(k[3] if len(k) == 4 else program, *k[:3]).exists() for k in (A, B, R)):
            continue
        r = test(program, A, B, R, sc)
        res["tests"][f"{label} {program}"] = dict(A=A, B=B, R=R, cells=r, all_passed=all(c["passed"] for c in r.values()))
        print(f"\n{label} {program}: A={A} B={B} R={R}")
        for k, c in r.items():
            print(f"  {k:14s} ratio8 {c['ratio8']:.3f}  refined median {c['refined_median']:.3f}  null {c['null_5_95']}  "
                  f"above95 {c['frac_refined_above_null95']:.2f}  {'pass' if c['passed'] else 'FAIL'}")
    (rc.OUT / "scores.json").write_text(json.dumps(res, indent=1))
