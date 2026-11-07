"""Checker: further claims (rods formation 70-subset band, off-page specificity rows, suite-wide ranking claims)."""
import itertools, json, os, sys
from pathlib import Path
os.environ["OMP_NUM_THREADS"] = "1"
sys.path[:0] = ["/home/user/swpo/residency-environments/environments/physim"]
import numpy as np
from physim import blobround6_eval as sc
GC = Path("/home/user/evalwork/gc_suites")
O = GC / "rescore_fair" / "checker" / "out"
SC = {f.stem: json.loads(f.read_text()) for f in O.glob("*__*.json")}
E = ("plugin", "fair")
out = {}


def npz(p, nt=None):
    with np.load(p) as z:
        return [z[f"query{j}"][:, :nt] if nt else z[f"query{j}"] for j in range(3)]


# 1. rods formation band (fband.py) under both estimators, and the null on the S_steer case
R = GC / "rods/formation/suite"
s = json.loads((R / "suite.json").read_text())
entry = next(c for c in s["cases"] if c["family"] == "sham")
case, groups = entry["request"], s["groups_by_horizon"][str(entry["horizon"])]
truth = npz(R / entry["truth"])
nt = truth[0].shape[1]
rost = sc.PublicRoster(n_ports=int(truth[0].shape[2]), device_slots=tuple(int(d["k"]) for d in s["devices"]))
ind = npz(R / "controls" / case["id"] / "independent_native.npz")
pool = [np.concatenate([a, b]) for a, b in zip(ind, npz(R / "ignore_actions.npz", nt))]
band = {}
for e in E:
    f = lambda p: sc.score_case(case, {"samples": p}, {"samples": truth}, groups=groups, n_samples=4, n_truth=2,
                                roster=rost, estimator=e)["joint_energy_equal_group_mean"]
    ref = f(ind)
    rat = [f([p[list(sub)] for p in pool]) / ref for sub in itertools.combinations(range(8), 4)]
    band[e] = [float(np.quantile(rat, q)) for q in (0.05, 0.5, 0.95)]
key = "rods__formation"
nul = {e: {c: SC[key][c]["numerical_null"][e]["agg"] / SC[key][c]["independent_native"][e]["agg"]
           for c in SC[key] if "numerical_null" in SC[key][c]} for e in E}
out["rods_formation_band"] = dict(band_q05_q50_q95=band, null_ratio_by_case=nul)


# 2. off-page specificity rows
def r(key, e, c, k, ref="independent_native"):
    return SC[key][c][k][e]["agg"] / SC[key][c][ref][e]["agg"]


def fam(path):
    s = json.loads((path / "suite.json").read_text())
    return {c["family"]: c["request"]["id"] for c in s["cases"]}


rows = {}
for lab, p in (("main_iter1", GC / "phase_membrane/suite"), ("main_iter2", GC / "phase_membrane/iter2/suite")):
    f = fam(p)
    rows[f"phase_membrane/{lab}:feed_B D:DS2"] = {e: r(f"phase_membrane__{lab}", e, f["feed_B"], "ablate_DS2") /
                                                  r(f"phase_membrane__{lab}", e, f["sham"], "ablate_DS2") for e in E}
f = fam(GC / "cips/iter2/suite")
rows["cips/main_iter2:hold_neck D:d0"] = {e: r("cips__main_iter2", e, f["hold_neck"], "ablate_d0") /
                                          r("cips__main_iter2", e, f["sham"], "ablate_d0") for e in E}
vs = json.loads((GC / "vortex/suite/suite.json").read_text())
vid = {c["program"]: c["id"] for c in vs["cases"]}
key = "vortex__main"
pooled = lambda e, c: 0.5 * (SC[key][c]["independent_native"][e]["agg"] + SC[key][c]["native_b"][e]["agg"])
rows["vortex/main:E_feed E:k0 first native"] = {e: r(key, e, vid["E_feed"], "k0") / r(key, e, vid["sham"], "k0") for e in E}
rows["vortex/main:E_feed E:k0 pooled"] = {e: (SC[key][vid["E_feed"]]["k0"][e]["agg"] / pooled(e, vid["E_feed"])) /
                                          (SC[key][vid["sham"]]["k0"][e]["agg"] / pooled(e, vid["sham"])) for e in E}
out["offpage_specificity"] = rows

# 3. suite-wide claims
MECH = ("adv0", "eps0", "k0", "kl0", "mu0")
NATLIKE = ("band_native", "native_b", "numerical_null")
pers, mech, orders, rise, drop = {e: [] for e in E}, {e: [] for e in E}, {}, [], {}
for key, S in SC.items():
    ids = list(S)
    ctls = sorted({k for c in ids for k in S[c]} - {"independent_native"})
    for c in ids:
        if "initial_persistence" in S[c]:
            for e in E:
                pers[e].append((r(key, e, c, "initial_persistence"), key, c))
    aggr = {}
    for k in ctls:
        cs = [c for c in ids if k in S[c]]
        aggr[k] = {e: np.mean([S[c][k][e]["agg"] for c in cs]) / np.mean([S[c]["independent_native"][e]["agg"] for c in cs]) for e in E}
        if k.startswith("ablate_") or k in MECH:
            for e in E:
                mech[e].append((aggr[k][e], key, k))
        rise.append((aggr[k]["fair"] / aggr[k]["plugin"], key, k))
    o = {e: sorted(aggr, key=lambda k: aggr[k][e]) for e in E}
    orders[key] = dict(changed=o["plugin"] != o["fair"], plugin=o["plugin"], fair=o["fair"])
    nat = {e: np.array([S[c]["independent_native"][e]["agg"] for c in ids]) for e in E}
    drop[key] = dict(rel=float(1 - nat["fair"].mean() / nat["plugin"].mean()), abs=float(nat["plugin"].mean() - nat["fair"].mean()),
                     case_rel=[float((1 - nat["fair"] / nat["plugin"]).min()), float((1 - nat["fair"] / nat["plugin"]).max())])
out["persistence_min_case"] = {e: min(pers[e]) for e in E}
out["weakest_mechanism_aggregate"] = {e: min(mech[e]) for e in E}
out["aggregate_order_changes"] = {k: v for k, v in orders.items() if v["changed"]}
nonnat = [x for x in rise if x[2] not in NATLIKE]
out["ratio_rise_factor_non_native_controls"] = [min(nonnat), max(nonnat)]
out["ratio_rise_factor_native_like"] = sorted([x for x in rise if x[2] in NATLIKE])
out["native_drop"] = drop
(O / "derived2.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: v for k, v in out.items() if k != "native_drop"}, indent=0, default=str)[:6000])
for k, v in drop.items():
    print(k, {a: (round(b, 4) if isinstance(b, float) else [round(x, 3) for x in b]) for a, b in v.items()})
