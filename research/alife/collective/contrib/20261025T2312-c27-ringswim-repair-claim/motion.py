"""(c27) Swimming after repair: for each cut cell and its twin (twinrepair.py result.json with tracks), the
path of the followed cell from +REP (repair done) to the first split/merge/loss (area jump > 30% between samples)
and the net displacement over that stretch in body lengths (2 R_eq of the pre-cut cell); also the ring score and
closure along it. usage: motion.py result.json [...]"""
import sys, json, numpy as np
REP = 340
H = W = 256
for fn in sys.argv[1:]:
    r = json.load(open(fn))
    for c in r["cells"]:
        BL = 2 * np.sqrt(c["area"] / np.pi); row = {"file": fn.split("/")[-2], "cell": c["cell"]}
        for a in ("twin", "cut"):
            T = [x for x in c["tracks"][a] if x[0] >= REP]
            disp = np.zeros(2); n = 0; ring = []; clo = []; end = None
            for p, q in zip(T, T[1:]):
                if p[1] == 0 or q[1] == 0 or abs(q[1] - p[1]) > 0.3 * p[1]: end = q[0]; break
                d = (np.array(q[4:6]) - np.array(p[4:6]) + np.array([H, W]) / 2) % np.array([H, W]) - np.array([H, W]) / 2
                disp += d; n += 1
                if q[3] is not None: ring.append(q[3])
                if q[6] is not None: clo.append(q[6])
            row[a] = {"stretch": [REP, end if end is not None else (T[-1][0] if T else None)], "net_BL": round(float(np.hypot(*disp) / BL), 2),
                      "ring_ge_1p5": round(float(np.mean([x >= 1.5 for x in ring])), 2) if ring else None, "closure_median": round(float(np.median(clo)), 2) if clo else None}
        print(json.dumps(row))
