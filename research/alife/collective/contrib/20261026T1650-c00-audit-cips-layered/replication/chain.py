"""Same-individual check: follow founder -> gen1 -> gen2 chains in labkit tracks (lineage_audit.json) and look up
each track's s-layer samples (wrapworld log) by centroid at the same time.
usage: python chain.py PACKDIR LOG.json"""
import sys, json
import numpy as np
pk, lg = sys.argv[1], sys.argv[2]
L = json.load(open(pk + "/lineage_audit.json")); D = json.load(open(lg))
dtf = L["dt_frame"]; H = W = 192
tr = {t["id"]: t for t in L["tracks"]}
rows = {round(r["t"]): r for r in D["rows"]}


def pd(a, b):
    dy = abs(a[0] - b[0]); dy = min(dy, H - dy); dx = abs(a[1] - b[1]); dx = min(dx, W - dx); return (dy * dy + dx * dx) ** 0.5


def samples(t):
    out = []
    for k, (cy, cx) in enumerate(zip(t["cy"], t["cx"])):
        tm = round(t["start"] + k * dtf)
        if tm % 100 or tm not in rows:
            continue
        bb = rows[tm]["bodies"]
        if not bb:
            continue
        j = int(np.argmin([pd((cy, cx), (b["cy"], b["cx"])) for b in bb]))
        b = bb[j]
        if pd((cy, cx), (b["cy"], b["cx"])) > 6:
            continue
        out.append((tm, b))
    return out


gen = {}
for t in sorted(L["tracks"], key=lambda t: t["start"]):
    gen[t["id"]] = 0 if not t["parents"] else gen[t["parents"][0]] + 1
leaves = [i for i in tr if gen[i] == max(gen.values())]
for leaf in leaves:
    chain = [leaf]
    while tr[chain[-1]]["parents"]:
        chain.append(tr[chain[-1]]["parents"][0])
    chain = chain[::-1]
    tot = ok = 0; rcmin = romin = 1e9; bm = []
    for i in chain:
        for tm, b in samples(tr[i]):
            if "rim_core" not in b:
                continue
            tot += 1; ok += b["rim_core"] >= 1.5 and b["rim_out"] >= 1.5
            rcmin = min(rcmin, b["rim_core"]); romin = min(romin, b["rim_out"])
            if "s_rim_from" in b:
                bm.append((tm, round(b["s_rim_from"][0], 3)))
    span = (tr[chain[0]]["start"], tr[chain[-1]]["end"])
    conv = [x for x in bm if not (x[0] < 1200 and x[0] < tr[chain[0]]["start"] + 300) and not (3500 <= x[0] < 3800) and not (8300 <= x[0] < 8600)]
    print(f"chain {chain} (gen 0..{gen[leaf]}) t {span[0]:.0f}-{span[1]:.0f}: s layer passes {ok}/{tot} samples, rim/core min {rcmin:.2f}, rim/out min {romin:.2f};"
          f" body-made share of rim s (converged tracer samples) min {min(x[1] for x in conv) if conv else None} over {len(conv)}; earliest {bm[:3]}")
