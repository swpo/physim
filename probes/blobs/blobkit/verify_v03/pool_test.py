"""pool-path check: SIGALRM guard must fire INSIDE spawn pool workers."""
import multiprocessing as mp
import os, time
from concurrent.futures import ProcessPoolExecutor


def main():
    os.environ["BLOBKIT_BATTERY_TIMEOUT"] = "20"
    import numpy as np
    from blobkit import _batteryproc as BP
    from blobkit import worlds as W
    import test_034 as T

    rec = T.dense_record(n_frames=400, n_blobs=260)   # T2-proven >20s full
    g = W.load("m0")
    recN, gN = T.battery_pair("m0")
    ex = ProcessPoolExecutor(2, mp_context=mp.get_context("spawn"))
    t0 = time.time()
    futs = [ex.submit(BP.battery_worker, (rec, g)),
            ex.submit(BP.battery_worker, (recN, gN))]
    dense = futs[0].result(timeout=300)
    normal = futs[1].result(timeout=300)
    wall = time.time() - t0
    ex.shutdown()
    out_d, crit_d, err_d = dense
    out_n, crit_n, err_n = normal
    ok = (err_d is None and out_d.get("battery_mode") == "subsampled"
          and err_n is None and "battery_mode" not in out_n
          and wall < 200)
    print(f"dense: mode={out_d.get('battery_mode') if out_d else None} "
          f"err={err_d}")
    print(f"normal: mode={'full' if out_n and 'battery_mode' not in out_n else '?'} "
          f"interest={out_n['interest'] if out_n else None}")
    print(f"POOL_PATH: {'PASS' if ok else 'FAIL'} (wall {wall:.0f}s)")


if __name__ == "__main__":
    main()
