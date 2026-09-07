#!/usr/bin/env python3
"""Bounded offline follow-up to recon.py. No simulator state is created or advanced.
Native stored frames only; exact device sampling functions only.
"""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
from pathlib import Path
import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from recon import ROOT, OUT, CACHE, map_member, sha256
sys.path.insert(0,str(ROOT/"probes/blobs/blobkit"))
sys.path.insert(0,str(ROOT/"probes/blobs/agentenv"))
import device as D
from blobkit import genome as G

F=map_member(CACHE,"frames")
BR=CACHE.with_name("p6g8_033_s942_branches.npz")
with np.load(CACHE,allow_pickle=False) as z:
    meta=json.loads(str(z["meta"]))
    snap=z["snapF_1700"]
with np.load(BR,allow_pickle=False) as z:
    bmeta=json.loads(str(z["meta"]))
gpath=ROOT/"environments/physim/physim/blobdata/p6g8_033.json"
g=json.loads(gpath.read_text())["genome"]
labels=["u0","u1","u2"]+[f"X{c}" for c in range(10)]
roster=[dict(lattice="square",n_rings=3,base_ds=3.5),dict(lattice="hex",n_rings=3,base_ds=3.0)]
sec=D.world_secrets("p6g8_033|s942|A0",13,roster,128.0)
perm=np.asarray(sec["port_perm"],int)
devs=[]
for i,(cfg,ds) in enumerate(zip(roster,sec["devices"])):
    devs.append(D.ProbeDevice(i,L=128.0,**cfg,**ds))

# Small field-only sampled reductions: not any new trajectory.
late_ids=[50,200,340,500]
core_records=[]
for i in late_ids:
    u=F[i,2].astype(np.float32)
    mask=u<0
    lab,n=G.periodic_label(mask)
    components=[]
    for j in range(1,n+1):
        yy,xx=np.nonzero(lab==j)
        cy=(np.angle(np.exp(2j*np.pi*(yy+.5)/256).mean())%(2*np.pi))*128/(2*np.pi)
        cx=(np.angle(np.exp(2j*np.pi*(xx+.5)/256).mean())%(2*np.pi))*128/(2*np.pi)
        components.append(dict(y=float(cy),x=float(cx),area=float(len(yy)*.25)))
    components.sort(key=lambda c:(c["y"],c["x"]))
    core_records.append(dict(t=i*5,n_components=n,negative_area=float(mask.sum()*.25),
                             components=components))
ious=[]
ref=F[50,2]<0
for i in late_ids[1:]:
    mask=F[i,2]<0
    ious.append(dict(t=i*5,mask_iou_with_t250=float((mask&ref).sum()/(mask|ref).sum())))

x9_trace=[]
u2_max=[]
for i in range(len(F)):
    x=F[i,12].astype(np.float32)
    x9_trace.append([i*5,float(x.min()),float(x.max()),int(np.count_nonzero(x))])
    u2_max.append(float(F[i,2].max()))
nonzero=[a[0] for a in x9_trace if a[3]]

# Actual home-pose sensor observations from existing cached frames.
home=np.empty((len(F),2,13,19),np.float64); home.fill(np.nan)
for i in range(len(F)):
    a=F[i].astype(np.float32)[perm]
    for j,dev in enumerate(devs):
        home[i,j,:,:dev.k]=dev.sample(a,.5)
sensor_summary=[]
for j,dev in enumerate(devs):
    v=home[50:,j,:,:dev.k]
    sensor_summary.append(dict(device=j,center=dev.center.tolist(),n_slots=dev.k,
        fields=[dict(field=labels[int(fi)],port=p,min=float(v[:,p].min()),
            max=float(v[:,p].max()),std_across_time_and_slots=float(v[:,p].std()))
            for p,fi in enumerate(perm)]))

# Matched native branch checks and response observations.
ctrl=map_member(BR,"control")
parity_all=all(np.array_equal(ctrl[i],F[340+i]) for i in range(51))
lag_ids=[1,2,5,10,20,50]
branch_stats={}
for name,amp in [("calib1",1.),("calib2",2.),("announced",3.),("calib4",4.)]:
    fr=map_member(BR,name)
    lag_stats=[]
    for i in lag_ids:
        delta=fr[i].astype(np.float32)-ctrl[i].astype(np.float32)
        sensors=[]
        for j,dev in enumerate(devs):
            vals=dev.sample(delta[perm],.5)
            sensors.append(dict(device=j,field_mean=vals.mean(axis=1).tolist(),
                field_rms=np.sqrt(np.mean(vals**2,axis=1)).tolist(),
                field_min=vals.min(axis=1).tolist(),field_max=vals.max(axis=1).tolist()))
        lag_stats.append(dict(lag=i*5,field_mean=delta.mean(axis=(1,2)).tolist(),
           field_rms=np.sqrt(np.mean(delta**2,axis=(1,2))).tolist(),
           field_min=delta.min(axis=(1,2)).tolist(),field_max=delta.max(axis=(1,2)).tolist(),
           sensor_port_order=sensors))
    branch_stats[name]=dict(amp=amp,duration=10.,starts_equal_control=bool(np.array_equal(fr[0],ctrl[0])),
                            sampled=lag_stats)
    del fr
ann=map_member(BR,"announced")
fig,axes=plt.subplots(4,3,figsize=(10,11),layout="constrained")
rows=[("control u0",0,False), ("amp3 u0",0,False),("amp3 minus control: u0",0,True),
      ("amp3 minus control: u1",1,True)]
for r,(label,field,is_delta) in enumerate(rows):
    for c,i in enumerate([2,10,50]):
        a=(ann[i,field].astype(np.float32)-ctrl[i,field].astype(np.float32)) if is_delta else (
            ann[i,field] if r==1 else ctrl[i,field])
        ax=axes[r,c]
        if is_delta:
            im=ax.imshow(a,origin="lower",extent=(0,128,0,128),cmap="RdBu_r",vmin=-2.5,vmax=2.5)
        else:
            im=ax.imshow(a,origin="lower",extent=(0,128,0,128),cmap="viridis",vmin=-1.2,vmax=1.8)
        for j,dev in enumerate(devs):
            ax.plot(dev.center[1],dev.center[0],"x" if j==0 else "+",color="black",ms=7,mew=1.3)
            ax.text(dev.center[1]+2,dev.center[0]+2,"A" if j==0 else "B",fontsize=8,color="black")
        ax.set_xticks([0,64,128]); ax.set_yticks([0,64,128])
        if r==0: ax.set_title(f"lag={i*5} tu")
        if c==0: ax.set_ylabel(label+"\ny (world units)")
    fig.colorbar(im,ax=axes[r,:],shrink=.7,pad=.01)
fig.suptitle("Native matched pulse: port7 = u0; anchor1700, amp3 for10tu\n"
             "Same snapshot/noise path; f16 stored fields. A emitter, B witness. Not an ensemble effect.")
fig.savefig(OUT/"matched_branch_fields.png",dpi=130); plt.close(fig)

fig,axes=plt.subplots(3,4,figsize=(12,8.2),layout="constrained")
for r,(field,lo,hi) in enumerate([(2,-1.7,1.7),(7,-.1,0),(12,-1e-7,1e-7)]):
    for c,i in enumerate(late_ids):
        ax=axes[r,c]
        im=ax.imshow(F[i,field],origin="lower",extent=(0,128,0,128),vmin=lo,vmax=hi,cmap="viridis")
        if c==0:ax.set_ylabel(labels[field]+"\ny (world units)")
        if r==0:ax.set_title(f"t={i*5}")
        ax.set_xticks([0,64,128]); ax.set_yticks([0,64,128])
        for j,dev in enumerate(devs):
            ax.plot(dev.center[1],dev.center[0],"x" if j==0 else "+",color="red",ms=6)
    fig.colorbar(im,ax=axes[r,:],shrink=.8,pad=.01)
fig.suptitle("Persistent negative u2 cores, broad X4 halo, quiet X9\n"
             "Late-only explicit scales; X9 is exactly zero in stored f16 frames at displayed times.")
fig.savefig(OUT/"late_polarity_and_quiet_control.png",dpi=130);plt.close(fig)

source_paths=[gpath,CACHE,BR,Path(D.__file__),ROOT/"probes/blobs/agentenv/adequacy.py",
    ROOT/"probes/blobs/blobkit/blobkit/genome.py",ROOT/"probes/blobs/blobkit/blobkit/soup/sim_cpu.py",
    ROOT/"probes/blobs/blobkit/blobkit/soup/sim_v1.py",ROOT/"environments/physim/physim/blobcore.py",
    ROOT/"environments/physim/physim/blobround5.py",
    ROOT/"probes/blobs/agentenv/cache/round5/r5_p6g8_033_s942_truth.npz"]
for n in ("REPORT.md","SCIENTIFIC_PROCESS.md","CONCURRENCY.md"):
    source_paths.append(ROOT/"probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit"/n)
provenance=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha256(p)) for p in source_paths]
out=dict(scope="read-only native cached seed942; no simulation and no fitted predictor",
    field_order=labels,port_to_field=perm.tolist(),port_to_label=[labels[i] for i in perm],
    geometry_key="p6g8_033|s942|A0",sensor_summary_t250_to2500=sensor_summary,
    negative_u2_components=core_records,negative_u2_iou=ious,
    x9=dict(last_nonzero_f16_sample_t=max(nonzero) if nonzero else None,
        sampled_late_nonzero_count=sum(a[3] for a in x9_trace[50:]),
        sampled_max_u2_t250_to2500=max(u2_max[50:]),
        x9_positive_drive_threshold_u2=g["acts"][2]["u0"]+g["chans"][9]["thr"],
        f32_snapshot1700_min=float(snap[12].min()),f32_snapshot1700_max=float(snap[12].max()),
        warning="f16 zeros do not prove exact continuum zeros; only saved 5tu times checked"),
    snapshot_rounding=dict(f32_to_f16_matches_frame340=bool(np.array_equal(snap.astype(np.float16),F[340])),
                          max_absolute_error=float(np.abs(snap-F[340].astype(np.float32)).max())),
    branch=dict(metadata=bmeta,control_equal_base_all_51_frames=parity_all,
       common_rng_evidence="adequacy.py:142 snapshot_state per branch; device.py:511-520 restores saved RNG; source leaves RNG draws unchanged",
       uncertainty="single shared noise path, same anchor and emitter; no repeated noise/path uncertainty estimate",
       data=branch_stats),provenance=provenance)
(OUT/"offline_checks.json").write_text(json.dumps(out,indent=2)+"\n")
np.savez_compressed(OUT/"offline_sensor_observations.npz",home=home,
                    t=np.arange(len(F))*5,port_to_field=perm,
                    x9_sampled_trace=np.array(x9_trace),u2_sampled_max=np.array(u2_max))
print(json.dumps(dict(done=True,control_parity=parity_all,port_to_label=out["port_to_label"],
    x9=out["x9"],negative_core_iou=ious),indent=2),flush=True)
