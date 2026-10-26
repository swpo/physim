"""Are the bodies identical between two labkit runs? Compares the recorded matter (phi) of every frame and the rendered
channels 0-2 (phi, |Q|, s). usage: compare_bodies.py a/frames.npz b/frames.npz"""
import sys, numpy as np
A, B = np.load(sys.argv[1]), np.load(sys.argv[2])
ma, mb = A["matter"].astype(np.float32), B["matter"].astype(np.float32)
print("matter frames", ma.shape, mb.shape, "max |diff|", float(np.abs(ma - mb).max()), "identical", bool(np.array_equal(ma, mb)))
ra, rb = A["render"].astype(np.float32), B["render"].astype(np.float32)
for c, nm in enumerate(["phi", "|Q|", "s"]):
    print(f"render ch{c} {nm}: max |diff| {float(np.abs(ra[:, c] - rb[:, c]).max())}, identical {bool(np.array_equal(ra[:, c], rb[:, c]))}")
print("cargo ch3 differs (expected):", float(np.abs(ra[:, 3] - rb[:, 3]).max()))
