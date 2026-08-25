
import sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/gpu")
from blobgpu.anchors import run_pair
r = run_pair(2.5, 1.6, "stamp_A4_dx05.npz", dt=0.02, T=300.0, dtype="f32")
print("A4s dt=0.02 T=300 f32:", r["status"], "sep:", [None if s is None else round(s,3) for s in r["sep"]])
