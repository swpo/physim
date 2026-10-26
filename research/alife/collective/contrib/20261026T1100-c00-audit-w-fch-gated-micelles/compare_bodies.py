"""Are the bodies (channel 0, u + 1.6) identical between an arm and the unchanged run on the same seed?
Usage: compare_bodies.py <unchanged_pack> <arm_pack> [...]"""
import sys, json
import numpy as np

ref = np.load(sys.argv[1] + "/frames.npz")["render"][:, 0].astype(np.float32)
mref = json.load(open(sys.argv[1] + "/metrics.json"))["summary"]
for p in sys.argv[2:]:
    a = np.load(p + "/frames.npz")["render"][:, 0].astype(np.float32)
    m = json.load(open(p + "/metrics.json"))["summary"]
    d = float(np.abs(a - ref).max()) if a.shape == ref.shape else float("nan")
    same = all(m[k] == mref[k] for k in ("splits", "persistent_splits", "merges", "max_generation", "tracks"))
    print(f"{p}: max|du| over all frames {d:.3g}; lineage summary identical: {same} "
          f"(splits {m['splits']}/{mref['splits']}, persistent {m['persistent_splits']}/{mref['persistent_splits']}, "
          f"tracks {m['tracks']}/{mref['tracks']})")
