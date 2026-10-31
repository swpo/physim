import os, sys, json, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import numpy as np
from physim import labbundle as LB
from physim import blobround6_eval as scoring
B = "/home/user/evalwork/vortex_eval/suite/bundle"
W = "/home/user/evalwork/vortex_eval/suite/work"
bundle = LB.open_bundle(B, profile="evaluation")
bundle.check_runtime()
rep = json.load(open(W + "/report.json"))
cases = bundle.suite["cases"]
out = {}
# 1. re-simulate one truth (follow_vortex, c014) bit for bit
i = [c["family"] for c in cases].index(sys.argv[1] if len(sys.argv) > 1 else "follow_vortex")
rec = cases[i]
o = bundle.make_oracle()
t0 = time.process_time()
tr = o.sample_truth(rec["request"]["actions"], rec["request"]["queries"], n_samples=2, truth_seed=bundle.suite["truth_seeds"][i])
truth = bundle.truth(rec)
out["truth_resim"] = dict(case=rec["request"]["id"], family=rec["family"], cpu_s=time.process_time() - t0,
    bitwise=[bool(np.array_equal(a, b)) for a, b in zip(tr["samples"], truth)] if isinstance(truth, list) else str(type(truth)))
# 2. rescore reference, slices, controls on two cases independently of fedvortex_report
def score(record, samples, n, truth):
    r = scoring.score_case(record["request"], {"samples": samples}, truth, groups=record["groups"], n_samples=n,
                           n_truth=2, roster=bundle.roster, limits=bundle.limits)
    return r["joint_energy_equal_group_mean"]
def load(p):
    with np.load(p, allow_pickle=False) as z:
        m = json.loads(str(z["meta"])); return [z[f"query{k}"].copy() for k in range(len(m["queries"]))], m
for fam in ("feed_neck", "sham", "stir_cut"):
    j = [c["family"] for c in cases].index(fam); rc = cases[j]; cid = rc["request"]["id"]; tj = bundle.truth(rc)
    ref, meta = load(f"{W}/controls/reference_{cid}.npz")
    s64 = score(rc, ref, 64, tj)
    sl = [score(rc, [a[4*k:4*k+4] for a in ref], 4, tj) for k in range(16)]
    m4 = float(np.mean(sl))
    row = dict(native64=s64, native64_report=rep["per_case"][cid]["native64"], band=[min(sl)/m4, max(sl)/m4],
               band_report=rep["per_case"][cid]["band"], ref_seed=meta["seed"], ref_members=meta["members"])
    for name in ("ablate_body_gain", "numerical_null", "wrong_probe_geometry"):
        p = f"{W}/controls/{name}_{cid}.npz"
        if os.path.exists(p):
            arr, m = load(p)
            row[name] = dict(ratio=score(rc, arr, 4, tj)/m4, report=rep["per_case"][cid]["ratio"][name], seed=m["seed"])
    out[fam] = row
print(json.dumps(out, indent=1))
