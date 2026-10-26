"""Are the bodies identical between two arms? Compares the recorded matter stack (phi, every frame) and the
rendered phi and |Q| channels. usage: compare_bodies.py a/frames.npz b/frames.npz"""
import sys, numpy as np
A, B = np.load(sys.argv[1]), np.load(sys.argv[2])
ma, mb = A["matter"].astype(np.float64), B["matter"].astype(np.float64)
ra, rb = A["render"].astype(np.float64), B["render"].astype(np.float64)
print(f"matter shapes {ma.shape} {mb.shape}; bitwise identical: {np.array_equal(A['matter'], B['matter'])}; "
      f"max |dphi| {np.abs(ma - mb).max():.3g}")
for c, n in ((0, "phi"), (1, "|Q|"), (2, "s"), (3, "c")):
    print(f"render ch{c} {n}: identical {np.array_equal(A['render'][:, c], B['render'][:, c])}, max |diff| {np.abs(ra[:, c] - rb[:, c]).max():.3g}")
