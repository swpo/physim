#!/usr/bin/env python3
"""Read-only seed-942 full-field reconnaissance. Never advances a simulator.
Run with ~/.venvs/bk3/bin/python from the repository root.
A stored NPY member is mapped in-place; no cache extraction or bulk NPZ load.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
from pathlib import Path
import sys, json, zipfile, struct, hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
CACHE = ROOT / "probes/blobs/agentenv/cache/p6g8_033_s942.npz"

def map_member(path, name):
    with zipfile.ZipFile(path) as z:
        item = z.getinfo(name + ".npy")
        if item.compress_type != zipfile.ZIP_STORED:
            raise ValueError("Expected uncompressed stored NPY; do not bulk-load")
        off = item.header_offset
    with open(path, "rb") as f:
        f.seek(off)
        hdr = f.read(30)
        sig, = struct.unpack("<I", hdr[:4])
        assert sig == 0x04034b50
        n, extra = struct.unpack("<HH", hdr[26:30])
        f.seek(n + extra, 1)
        version = np.lib.format.read_magic(f)
        shape, fort, dtype = np.lib.format._read_array_header(f, version)
        offset = f.tell()
    return np.memmap(path, mode="r", dtype=dtype, offset=offset,
                     shape=shape, order="F" if fort else "C")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def initial():
    with np.load(CACHE, allow_pickle=False) as z:
        meta = json.loads(str(z["meta"]))
    F = map_member(CACHE, "frames")
    times = [0, 250, 1000, 1700, 2500]
    ids = [int(t / meta["ctrl_tu"]) for t in times]
    labels = ["u0", "u1", "u2"] + [f"X{c}" for c in range(10)]
    selected = np.asarray(F[ids], dtype=np.float32)
    stats = []
    for j, t in enumerate(times):
        stats.append({"t": t, "field": [{"name": labels[k],
            "min": float(selected[j,k].min()), "max": float(selected[j,k].max()),
            "mean": float(selected[j,k].mean()), "std": float(selected[j,k].std())}
            for k in range(13)]})
    for name, fields in [("activators",range(3)), ("channels_0_4",range(3,8)),
                          ("channels_5_9",range(8,13))]:
        fig, axes = plt.subplots(len(fields),len(times),figsize=(12.5,2.35*len(fields)),
                                 layout="constrained", squeeze=False)
        for i,k in enumerate(fields):
            lo,hi=float(selected[:,k].min()),float(selected[:,k].max())
            for j,t in enumerate(times):
                ax=axes[i,j]
                im=ax.imshow(selected[j,k],origin="lower",extent=(0,128,0,128),
                             vmin=lo,vmax=hi,cmap="viridis", interpolation="nearest")
                if i==0: ax.set_title(f"t={t} tu")
                if j==0: ax.set_ylabel(labels[k]+"\ny (world units)")
                ax.set_xticks([0,64,128]); ax.set_yticks([0,64,128])
                ax.tick_params(labelsize=7)
            fig.colorbar(im,ax=axes[i,:],shrink=.75, pad=.01)
        fig.suptitle("p6g8_033 / seed 942: native cached 2D fields\n"
                     "Full torus; fixed per-row full range over displayed times; field indices, not ports",fontsize=12)
        fig.savefig(OUT/f"initial_{name}.png",dpi=130)
        plt.close(fig)
    (OUT/"initial_stats.json").write_text(json.dumps({"times":times,"stats":stats},indent=2)+"\n")
    print("Initial full-field figures and scalar stats written.", flush=True)

if __name__ == "__main__":
    initial()
