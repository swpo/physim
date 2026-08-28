"""verify_v03/smoke4.py — W1 smoke: 4-lane batched ladder, CPU-JAX f64.
Lanes: m0 s7, m4 s1, m4 s2, coex s2. Expect m0 exits rung1 "static"; others
per their singles. Writes smoke4.txt (transcript) + smoke4.json (summary)."""
import json, os, sys, time
os.environ.setdefault("BLOBKIT_RESULTS", "")
from blobkit import worlds
from blobkit.assay_batch import run_assay_batch

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    specs = [("m0", 7), ("m4", 1), ("m4", 2), ("coex", 2)]
    jobs, kicks_map = [], {}
    for w, s in specs:
        g = worlds.WORLDS[w]()
        jobs.append((g, s))
        k = worlds.KICKS.get(g["id"])
        if k:
            kicks_map[g["id"]] = k
    t0 = time.time()
    outs = run_assay_batch(jobs, dtype="f64", kicks_map=kicks_map,
                           cap=5000.0, verbose=True)   # bounded wall (local)
    wall = time.time() - t0
    summary = []
    for (w, s), o in zip(specs, outs):
        summary.append(dict(world=w, seed=s, interest=o["interest"],
                            T_used=o["horizon"]["T_used"],
                            why=o["horizon"]["why_stopped"],
                            n_ext=o["horizon"]["n_extensions"]))
        print(f"[smoke4] {w} s{s}: interest={o['interest']:.2f} "
              f"T={o['horizon']['T_used']:.0f} why={o['horizon']['why_stopped']}")
    res = dict(gate="W1-smoke", dtype="f64", cap=5000.0,
               wall=round(wall, 1), lanes=summary)
    json.dump(res, open(os.path.join(HERE, "smoke4.json"), "w"), indent=1)
    print(json.dumps(res))

if __name__ == "__main__":
    main()
