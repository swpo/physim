#!/usr/bin/env python3
"""Bounded, cache-only measurements for three per-world physics candidates.
No stepper, simulator, fork, or evaluator is called. Each full-field temporary
is one float32 frame (~3 MB). The large stored arrays remain read-only maps.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
import json
from pathlib import Path
import numpy as np
from cache_access import memmap_member, json_member, project_root, make_devices

OUT = Path(__file__).resolve().parent
ROOT = project_root()
BASE = ROOT / "probes/blobs/agentenv/cache/p4g2_044_s928.npz"
BR = BASE.with_name("p4g2_044_s928_branches.npz")
g = json.loads((ROOT / "environments/physim/physim/blobdata/p4g2_044.json").read_text())["genome"]
frames=memmap_member(BASE,"frames")
control=memmap_member(BR,"control")
meta=json_member(BASE)
bm=json_member(BR)
sec,devs=make_devices(ROOT)
from device import blob_list_fast
u0=np.array([a["u0"] for a in g["acts"]])
thr=np.array([a["u0"] + .45*(np.sqrt(a["lam"])-a["u0"]) for a in g["acts"]])

def corr(a,b):
    return float(np.corrcoef(a.ravel(),b.ravel())[0,1])

def stats(a):
    return dict(mean=float(a.mean()),std=float(a.std()),min=float(a.min()),max=float(a.max()))

selected=[]
for t in (0,250,750,1700,2500):
    F=np.array(frames[int(t/5)],dtype=np.float32)
    gate=F[:4]-u0[:,None,None] > g["chans"][7]["thr"]
    nonspot=F[0] < thr[0]
    selected.append(dict(t=t,negative_area=(F[:4]<0).mean(axis=(1,2)).tolist(),
                         gate_above_threshold_fraction=gate.mean(axis=(1,2)).tolist(),
                         u0_u1_correlation_off_u0_spots=corr(F[0][nonspot],F[1][nonspot]),
                         u2_u3_correlation=corr(F[2],F[3]),
                         u2_where_u3_negative=stats(F[2][F[3]<0]) if (F[3]<0).any() else None,
                         u2_where_u3_above_one=stats(F[2][F[3]>1]),
                         shared_drive_mean=float((F[2]+F[3]-u0[2]-u0[3]).mean()),
                         shared_channels_mean=F[[8,9,10]].mean(axis=(1,2)).tolist()))

c=(np.arange(256)+.5)*.5
cy,cx=bm["inj_yx"]
dy=(c-cy+64)%128-64;dx=(c-cx+64)%128-64
rad=np.hypot(dy[:,None],dx[None,:])
rings=[(0,8),(8,16),(16,32),(32,91)]
branches=[]
for name,amp in (("calib1",1),("calib2",2),("announced",3),("calib4",4)):
    arr=memmap_member(BR,name)
    records=[]
    for lag in (0,5,10,25,50,100,250):
        j=int(lag/5)
        C=np.array(control[j],dtype=np.float32)
        B=np.array(arr[j],dtype=np.float32)
        delta=B-C
        measurements=dict(lag=lag,mean_delta=delta.mean(axis=(1,2)).tolist(),
                          max_abs_delta=np.abs(delta).max(axis=(1,2)).tolist(),
                          rms_delta=np.sqrt((delta*delta).mean(axis=(1,2))).tolist(),
                          sensor_delta_raw_field_order=[(d.sample(B,.5)-d.sample(C,.5)).tolist() for d in devs],
                          u0_visibility_area_abs_delta_gt_005=float((np.abs(delta[0])>.05).mean()),
                          u0_delta_by_emitter_distance=[dict(inner=lo,outer=hi,**stats(delta[0][(rad>=lo)&(rad<hi)])) for lo,hi in rings])
        if lag in (10,50,250):
            measurements["u0_segments"]=blob_list_fast(B[0],thr[0],.5,128)
            measurements["u0_control_segments"]=blob_list_fast(C[0],thr[0],.5,128)
        records.append(measurements)
    branches.append(dict(name=name,amp=amp,dur=10,records=records))
    del arr

parity=[]
for lag in (0,5,10,25,50,100,250):
    C=np.array(control[int(lag/5)],dtype=np.float32)
    M=np.array(frames[int((1700+lag)/5)],dtype=np.float32)
    parity.append(dict(lag=lag,exact_f16_equal=bool(np.array_equal(C,M)),max_abs_diff=float(np.abs(C-M).max())))
with np.load(BASE,allow_pickle=False) as z:
    snap=np.array(z["snapF_1700"],dtype=np.float32)
F=np.array(frames[340],dtype=np.float32)
report=dict(selected=selected,branches=branches,control_main_parity=parity,
            f16_vs_f32_max_error_at_1700=np.abs(F-snap).max(axis=(1,2)).tolist(),
            notes=["Raw-field order u0,u1,u2,u3,x0,...,x7; map to ports using first_look.json.",
                   "Branches share restored state and RNG according to adequacy.py; one realization, not an ensemble.",
                   "Visibility threshold |delta u0|>0.05 is an explicit display summary, not a phenotype rank or calibrated detectability threshold."])
(OUT/"measurements.json").write_text(json.dumps(report,indent=2)+"\n")
print("Measurements saved to",OUT/"measurements.json",flush=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
A=memmap_member(BR,"announced")
C=np.array(control[50],dtype=np.float32)
B=np.array(A[50],dtype=np.float32)
D10=np.array(A[2],dtype=np.float32)-np.array(control[2],dtype=np.float32)
D250=B-C
fig,axs=plt.subplots(3,4,figsize=(14,10.5),layout="constrained")
for row,k in enumerate((0,1,11)):
    name=("u0","u1","x7")[row]
    lo=min(C[k].min(),B[k].min());hi=max(C[k].max(),B[k].max())
    dv=max(np.abs(D10[k]).max(),np.abs(D250[k]).max())
    for col,arr in enumerate((C[k],B[k],D10[k],D250[k])):
        ax=axs[row,col]
        im=ax.imshow(arr,origin="lower",extent=(0,128,0,128),interpolation="nearest",
                     cmap="viridis" if col<2 else "RdBu_r",
                     vmin=lo if col<2 else -dv,vmax=hi if col<2 else dv)
        for d,color in zip(devs,["white","black"]):
            p=d.node_positions()
            ax.scatter(p[:,1],p[:,0],s=10,facecolors="none",edgecolors=color,linewidths=.7)
        ax.set_title(f"{name}: " + ("control lag 250","source 3 lag 250","paired delta lag 10","paired delta lag 250")[col],fontsize=9)
        ax.set_xticks([0,64,128]);ax.set_yticks([0,64,128]);ax.tick_params(labelsize=7)
        fig.colorbar(im,ax=ax,shrink=.72)
fig.suptitle("Existing matched branches: source u0, amp=3, duration=10, anchor t=1700. No new simulation.")
fig.savefig(OUT/"paired_source_fields.png",dpi=135)
plt.close(fig)
print("Figure saved to",OUT/"paired_source_fields.png",flush=True)
