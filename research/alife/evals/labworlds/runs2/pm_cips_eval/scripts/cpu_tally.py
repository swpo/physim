import numpy as np, glob, json, os
OUT = "/home/user/evalwork/pm_cips_eval"
tot = {}
for p in glob.glob(f"{OUT}/**/*.npz", recursive=True):
    try:
        with np.load(p) as z:
            if "cpu_s" in z.files:
                k = os.path.relpath(p, OUT).split("/")[0]
                tot[k] = tot.get(k, 0.0) + float(z["cpu_s"])
    except Exception:
        pass
extra = {"timing": 77 + 19, "cips_prep": 190, "cips_parity": 65, "aborted_runs": 120, "analysis": 60}
for k, v in json.load(open(f"{OUT}/cips_prep/prep_s5_t3100.json")).items():
    pass
tot.update({k: tot.get(k, 0) + v for k, v in extra.items()})
print({k: round(v) for k, v in sorted(tot.items())}, "total h", round(sum(tot.values()) / 3600, 2))
