import json, glob, re
rows = []
for f in sorted(glob.glob("packs/b128_*/claim_measures.json")):
    d = json.load(open(f)); m = re.match(r"packs/b128_(\w+?)_([\d.]+)_s(\d)", f)
    rows.append((m.group(1), float(m.group(2)), int(m.group(3)), d))
rows.sort(key=lambda r: (r[0] != "base", r[0], r[1], r[2]))
K = ["persistent_splits", "max_generation", "merge_split_ratio", "swim_divide_3bl", "best_bl", "ring_frac", "ring_rimout",
     "cargo_inout", "cargo_frac2", "daughters_frac2", "speed_px_per_frame", "components_final", "wall"]
print("form  sd    seed " + " ".join(k[:10] for k in K))
for form, sd, seed, d in rows:
    print(f"{form:5} {sd:<5g} {seed}    " + " ".join(f"{str(d.get(k)):>10}" for k in K))
json.dump([dict(form=f, sd=s, seed=e, **{k: d.get(k) for k in ["status"] + K}) for f, s, e, d in rows], open("noise_table.json", "w"), indent=1)
