"""Fuel minima of the noise battery, from each labkit pack's rendered frames (frames.npz, channel 1 = fuel Y; 120 saved
frames over T=1200). usage: fuel_min.py PACKS_DIR. Prints, per pack: minimum over the run, over its second half,
pixels below 0.01 summed over frames, and the number of frames with any such pixel."""
import glob, os, sys
import numpy as np

for p in sorted(glob.glob(os.path.join(sys.argv[1], "*_s*"))):
    Y = np.load(p + "/frames.npz")["render"][:, 1].astype(np.float32)
    n = len(Y)
    below = Y < 0.01
    print(f"{os.path.basename(p):10s} min {Y.min():.4f}  min_second_half {Y[n // 2:].min():.4f}  "
          f"px<0.01 {int(below.sum())}  frames_with_px<0.01 {int(below.any(axis=(1, 2)).sum())} of {n}")
