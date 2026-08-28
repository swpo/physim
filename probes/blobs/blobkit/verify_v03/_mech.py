"""dev mechanical test: 2 m0 lanes f32 -> pads to B=4 (2 ballast), both
exit rung 1 static. Validates: init, pad, ladder, pool battery, finalize."""
import json, os, time
os.environ.setdefault("BLOBKIT_RESULTS", "")
from blobkit import worlds
from blobkit.assay_batch import run_assay_batch

def main():
    g = worlds.WORLDS["m0"]()
    t0 = time.time()
    outs = run_assay_batch([(g, 7), (g, 3)], dtype="f32", verbose=True,
                           battery_procs=2)
    for o in outs:
        print("OUT", o["interest"], o["horizon"]["T_used"],
              o["horizon"]["why_stopped"], o["horizon"]["n_extensions"])
    print("wall", round(time.time() - t0, 1))

if __name__ == "__main__":
    main()
