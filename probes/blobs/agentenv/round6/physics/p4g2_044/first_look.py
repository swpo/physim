#!/usr/bin/env python3
"""First full-field look at p4g2_044/s928. Reads cache only; never integrates."""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cache_access import memmap_member, json_member, project_root, make_devices, raw_stats

OUT = Path(__file__).resolve().parent
ROOT = project_root()
CACHE = ROOT / "probes/blobs/agentenv/cache/p4g2_044_s928.npz"
BRANCH = CACHE.with_name("p4g2_044_s928_branches.npz")
meta = json_member(CACHE)
branch_meta = json_member(BRANCH)
g = json.loads((ROOT / "environments/physim/physim/blobdata/p4g2_044.json").read_text())["genome"]
frames = memmap_member(CACHE, "frames")
sec, devs = make_devices(ROOT, meta["na"] + meta["nc"], meta["L"])
labels = [f"u{i}" for i in range(4)] + [f"x{c}" for c in range(8)]
port_of_field = np.argsort(sec["port_perm"])
ts = [0, 250, 750, 1700, 2500]
selected = [np.array(frames[int(t / meta["ctrl_tu"] )], dtype=np.float32) for t in ts]
thr = np.array([a["u0"] + 0.45 * (np.sqrt(a["lam"]) - a["u0"]) for a in g["acts"]])

fig, axs = plt.subplots(4, len(ts), figsize=(15.5, 12.2), layout="constrained")
for a in range(4):
    lo = min(F[a].min() for F in selected)
    hi = max(F[a].max() for F in selected)
    for col, (t,F) in enumerate(zip(ts,selected)):
        ax = axs[a,col]
        im = ax.imshow(F[a], origin="lower", extent=(0,128,0,128),
                       cmap="viridis", vmin=lo, vmax=hi, interpolation="nearest")
        ax.set_title(f"{labels[a]} (port {port_of_field[a]}), t={t}", fontsize=10)
        ax.set_xticks([0,64,128]); ax.set_yticks([0,64,128]); ax.tick_params(labelsize=7)
        if col == 0: ax.set_ylabel("y")
        if a == 3: ax.set_xlabel("x")
    fig.colorbar(im, ax=axs[a,:].tolist(), shrink=0.8, label="raw field")
fig.suptitle("p4g2_044 / s928: all four activators, fixed raw color scale per row; periodic 128 x 128 box")
fig.savefig(OUT / "activators_time.png", dpi=135)
plt.close(fig)

F = selected[ts.index(1700)]
fig, axs = plt.subplots(3, 4, figsize=(15.5, 12), layout="constrained")
for a, ax in enumerate(axs.flat):
    lo,hi = np.quantile(F[a], [0.0,1.0])
    im=ax.imshow(F[a], origin="lower", extent=(0,128,0,128), cmap="viridis",
                 vmin=lo, vmax=hi, interpolation="nearest")
    for d,c in zip(devs,["white","red"]):
        pos=d.node_positions()
        ax.scatter(pos[:,1],pos[:,0],s=13,facecolors="none",edgecolors=c,linewidths=0.7)
    ax.set_title(f"{labels[a]} (port {port_of_field[a]})", fontsize=10)
    ax.set_xticks([0,64,128]);ax.set_yticks([0,64,128]);ax.tick_params(labelsize=8)
    fig.colorbar(im,ax=ax,shrink=.72)
fig.suptitle("p4g2_044 / s928 at t=1700: all 12 fields; own color range per panel. A white / B red sensor rings")
fig.savefig(OUT / "all_fields_t1700.png", dpi=135)
plt.close(fig)

blobs = json_member(CACHE, "blobs")
counts = np.array([[len(x) for x in row] for row in blobs])
areas = np.array([[sum(v[2] for v in x) for x in row] for row in blobs])
fig, axs=plt.subplots(2,1,figsize=(12,6),sharex=True,layout="constrained")
for a in range(4):
    axs[0].plot(meta["t"], counts[:,a], label=f"u{a}")
    axs[1].plot(meta["t"], areas[:,a]/128**2,label=f"u{a}")
axs[0].set_ylabel("recorded segment count");axs[0].legend(ncol=4)
axs[1].set_ylabel("above-threshold area / box");axs[1].set_xlabel("time (tu)")
fig.suptitle("Native cached blob records (thresholds from sim_v1; topology descriptors, not validated organism identities)")
fig.savefig(OUT / "native_segments.png",dpi=135)
plt.close(fig)

report = dict(meta=meta, branch_meta=branch_meta, secrets=sec,
              field_to_port=port_of_field.tolist(), threshold=thr.tolist(),
              snapshots=[dict(t=t,raw=raw_stats(F),
                              cover=(F[:4]>thr[:,None,None]).mean(axis=(1,2)).tolist(),
                              sensor_raw_field_order=[d.sample(F,meta["dx"]).tolist() for d in devs])
                         for t,F in zip(ts,selected)],
              blob_counts_at_selected={str(t):counts[int(t/5)].tolist() for t in ts},
              blob_count_range=[counts.min(axis=0).tolist(),counts.max(axis=0).tolist()])
(OUT / "first_look.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(dict(meta={k:v for k,v in meta.items() if k!="t"},branch_meta=branch_meta,
                     field_to_port=port_of_field.tolist(),counts=report["blob_counts_at_selected"],
                     figures=["activators_time.png","all_fields_t1700.png","native_segments.png"]),indent=2),flush=True)
