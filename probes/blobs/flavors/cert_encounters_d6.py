"""cert_encounters_d6.py — encounter table extension: d0=6 (strongly overlapping seeds)."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors")
import importlib
import cert_encounters as CE

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(k, s, 6) for k in ("AA", "AB", "BB") for s in (0, 1, 2)]
    t0 = time.time(); out = []
    with ProcessPoolExecutor(max_workers=9) as ex:
        for rec in ex.map(CE.one, jobs):
            out.append(rec)
            print({k: rec[k] for k in rec if k != "census_hist"}, flush=True)
    print("total %.0fs" % (time.time()-t0))
    json.dump(out, open("/Users/spoho/Documents/prime/test/physim/probes/blobs/flavors/cert_encounters_d6.json","w"), indent=1)
