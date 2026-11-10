"""cinterp -- the hand-written reading of the `bias2` GPU jobs as claims, every number pulled from the result files.

usage: python -B cinterp.py RESULTS_DIR world=JOB_ID [world=JOB_ID ...]   -> RESULTS_DIR/interpretation.json
(csummary.py then folds it into summary.json under `claims`.)
Each claim is a text template whose {placeholders} are filled from the result files, so a number in the text cannot
differ from its source: `values` holds the numbers, `sources` where each comes from. Source forms:
  <job>:out/<world>/combined.json:<key path>     a file of the job's output on the gpu-jobs branch
  analysis:<world>.<key path>                    results/analysis.json, derived from combined.json by canalyze.py
  pairs:<world>.<A>__minus__<B>.<key>            results/pairs_<world>.json, the paired trajectory bootstrap of
                                                 cpair.py on <job>:out/<world>/items/*.npz
  extra:<world>.<key path>                       results/extra.json, local follow-up readings by cextra.py of
                                                 <job>:out/<world>/latsub/*.npz and <job>:out/<world>/windows/*.npz
Horizon index i of a 5-vector is h = (1, 2, 4, 8, 16)[i] study ticks. Ceiling = the closure ceiling of
learned_phi2's fixed family G, (V_mean - V_best) / (V_mean - V_oracle). `loc1` = cross-validated R^2 of a per-block
linear readout with weights shared over blocks; "sym" = the smaller of the two directions.
The claims themselves are in cclaims.py (written after the jobs returned; plain calls of claim()).
"""
import json
import os
import sys

R = sys.argv[1]
JOBS = dict(a.split("=") for a in sys.argv[2:])
HZ = [1, 2, 4, 8, 16]
HI = {h: i for i, h in enumerate(HZ)}
def _combined(w):
    import gzip
    p = os.path.join(R, w, "combined.json")
    return json.load(open(p)) if os.path.exists(p) else json.load(gzip.open(p + ".gz", "rt"))


C = {w: _combined(w) for w in JOBS}
A = json.load(open(os.path.join(R, "analysis.json")))
X = json.load(open(os.path.join(R, "extra.json"))) if os.path.exists(os.path.join(R, "extra.json")) else {}
PAIRS = {w: (json.load(open(os.path.join(R, f"pairs_{w}.json"))) if os.path.exists(os.path.join(R, f"pairs_{w}.json")) else {})
         for w in JOBS}
claims = []


def _walk(v, path):
    for p in path:
        v = v[p] if not isinstance(v, list) else v[int(p)]
    return v


def cfg(w, nm, *path):
    """A key of combined.json:configs.<nm> (seed means)."""
    return _walk(C[w]["configs"][nm], path), f"{JOBS[w]}:out/{w}/combined.json:configs.{nm}." + ".".join(str(p) for p in path)


def hand(w, k, *path):
    return _walk(C[w]["hand"][k], path), f"{JOBS[w]}:out/{w}/combined.json:hand.{k}." + ".".join(str(p) for p in path)


def ana(w, *path):
    return _walk(A[w], path), f"analysis:{w}." + ".".join(str(p) for p in path)


def ext(w, *path):
    return _walk(X[w], path), f"extra:{w}." + ".".join(str(p) for p in path)


def ceil(w, nm, h):
    """Closure ceiling (family G) at horizon h of a config (seed mean) or `hand_<design>`."""
    if nm.startswith("hand_"):
        return hand(w, nm[5:], "G", "ceiling", HI[h])
    return cfg(w, nm, "ceiling_G", HI[h])


def agree(w, nm, target, mode="loc1", direction=None):
    """Agreement of a config (or hand_<design>) with a hand design: one direction, or the smaller of the two."""
    get = (lambda *p: hand(w, nm[5:], *p)) if nm.startswith("hand_") else (lambda *p: cfg(w, nm, *p))
    if direction:
        return get("agreement", target, mode, direction)
    a, sa = get("agreement", target, mode, "H_from_Z")
    b, sb = get("agreement", target, mode, "Z_from_H")
    return min(a, b), sa.rsplit(".", 1)[0] + ".min(H_from_Z, Z_from_H)"


def pair(w, a, b, h, key="diff"):
    r = PAIRS[w][f"{a}__minus__{b}"]
    return r[key][HI[h]], f"pairs:{w}.{a}__minus__{b}.{key}[{HI[h]}]"


def rd(v, n=3):
    if v is None or isinstance(v, str):
        return v
    return [rd(x, n) for x in v] if isinstance(v, (list, tuple)) else round(float(v), n)


def claim(text, items, digits=None):
    """text with {name} placeholders; items {name: (value, source)}; digits {name: n} overrides 3 decimals (2 for
    names not listed when the value's magnitude is >= 10)."""
    digits = digits or {}
    vals = {}
    for k, (v, _) in items.items():
        n = digits.get(k, 3 if (not isinstance(v, (int, float)) or abs(v) < 10) else 1)
        vals[k] = rd(v, n)
    claims.append({"claim": text.format(**vals), "values": vals, "sources": {k: s for k, (_, s) in items.items()}})


# ----------------------------------------------------------------------------- claims
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cclaims.py")).read())   # noqa: S102  (same folder; plain data + calls of claim())

json.dump(claims, open(os.path.join(R, "interpretation.json"), "w"), indent=1)
print(len(claims), "claims")
for c in claims:
    print("-", c["claim"], "\n")
