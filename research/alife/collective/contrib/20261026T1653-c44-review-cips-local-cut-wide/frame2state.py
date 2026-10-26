"""Build a cutmany.py CUT_CACHE state from a labkit frames.npz (fields e, p, F, s stored as float16 at recorded frames).
usage: python frame2state.py frames.npz FRAME OUT.npz   (t = FRAME * steps_per_frame * dt = FRAME * 100)"""
import sys, numpy as np
z = np.load(sys.argv[1]); f = int(sys.argv[2]); rf = list(z["render_f"])
k = rf.index(f); e, p, F, s = z["render"][k].astype(np.float64)
np.savez(sys.argv[3], e=e, p=p, F=F, s=s, t=float(f * 100))
print("frame", f, "t", f * 100, "e max", e.max())
