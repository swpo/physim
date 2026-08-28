
import os, json
os.environ["BLOBKIT_SKIP_LOCK"] = "1"
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def main():
    from blobkit._batteryproc import battery_worker
    from blobkit import worlds
    from blobkit.soup import sim_cpu as SC

    g = worlds.load("m0")
    S = SC.init_soup(g, L=128.0, seed=7, workers=1)
    SC.advance(S, 2500.0)
    rec = SC.snapshot_rec(S)

    pool = ProcessPoolExecutor(max_workers=2, mp_context=mp.get_context("spawn"))
    res = list(pool.map(battery_worker, [(dict(rec), g), (dict(rec), g)]))
    pool.shutdown(wait=True)
    outs = [(r[0]["interest"] if r[0] else None, r[2]) for r in res]
    print("spawn pool results:", outs)
    assert outs[0][0] == outs[1][0] and outs[0][0] is not None and outs[0][1] is None

    import blobkit.assay_batch as ABM
    pool2 = ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"))
    list(pool2.map(battery_worker, [(dict(rec), g)]))
    pool2._broken = "simulated broken"     # emulate BrokenExecutor state flag
    ABM._shutdown_pool(pool2)              # must return promptly
    print("broken-pool shutdown returned")
    print("SPAWN TEST PASS")

if __name__ == "__main__":
    main()
