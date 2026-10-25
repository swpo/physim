"""(c27) Death hazard per 1e5 cell-steps by cell AGE bin (steps since the id first appeared), founders vs split-born,
pooled over the genealogies given. Separates 'founders are old' from 'founders die more at the same age'."""
import sys, json, gzip
bins = [(10000, 30000), (30000, 50000), (50000, 100001)]
acc = {(b, k): [0, 0] for b in bins for k in ("founder", "born")}
for fn in sys.argv[1:]:
    d = json.load(gzip.open(fn)); S, E = d["series"], d["events"]; dt = S[1]["t"] - S[0]["t"]
    sb = set(c for t, ty, p, ch in E if ty == "split" for c in ch)
    t0 = {}
    for x in S:
        for c in x["id"]: t0.setdefault(c, x["t"])
    for x in S:
        for c in x["id"]:
            age = x["t"] - t0[c]
            for b in bins:
                if b[0] <= age < b[1]: acc[(b, "born" if c in sb else "founder")][1] += dt
    for t, ty, p, ch in E:
        if ty == "death":
            for c in p:
                if c not in t0: continue
                age = t - t0[c]
                for b in bins:
                    if b[0] <= age < b[1]: acc[(b, "born" if c in sb else "founder")][0] += 1
for b in bins:
    print(f"age {b[0]}-{b[1]}: " + "; ".join(f"{k}: {acc[(b,k)][0]} deaths / {acc[(b,k)][1]} cell-steps = {1e5*acc[(b,k)][0]/max(acc[(b,k)][1],1):.3f} per 1e5" for k in ("founder", "born")))
