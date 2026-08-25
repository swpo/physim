import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds_lib as DL
import ds2_lib as D2

a2 = json.load(open(D2.ARCHIVE2))
# rerun failed seed2s WITH the t0 floor (horizon-fair)
plan = []
for key, c in a2.items():
    if c.get("seed2_interest") is not None and not c.get("seed2_ok"):
        plan.append((key, c))
print("rerun plan:", [(k, c["cand"]) for k, c in plan], flush=True)
for key, c in plan:
    # find seed1 T_used from results
    rows = [r for r in json.load(open(D2.RESULTS2))
            if r.get("cand") == c["cand"] and r.get("phase") == "screen"]
    t0 = rows[-1].get("T_used") if rows else None
    job = dict(cand=c["cand"] + "_s2f", gen=10, op="seed2", kind="seed2f",
               seed=2, t0=t0, parents=[c["cand"]], genome=c["genome"])
    row = D2.evaluate_v2(job)
    i2 = row.get("interest", 0.0) or 0.0
    ok = bool(i2 >= 0.6 * c["interest"] and i2 > 0.0)
    with DL.locked_json(D2.ARCHIVE2, {}) as cc:
        cell = cc.data[key]
        cell["seed2_interest"] = i2
        cell["seed2_cell"] = row.get("cell")
        cell["seed2_ok"] = ok
        cell["seed2_t0floor"] = t0
        cc.write()
    print("RERUN", c["cand"], "t0=", t0, "I2=", round(i2, 1), "ok=", ok,
          "cell=", row.get("cell"), flush=True)
print("S2F_DONE")
