
import sys, time, json
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility")
from sim import run
from metrics import certify_point

OUT = "/Users/spoho/Documents/prime/test/physim/probes/blobs/motility"
res = {}
# parameter window at the M1 traveling point (tau=5.0, Dv=0.65): vary k1 and Dv
for k1 in (-0.6, -0.65, -0.7, -0.75, -0.8):
    r = run(p=dict(k1=k1, Dv=0.65, tau=5.0), T=400.0, dx=0.5, stepper="imexfft", kick_angle=30.0)
    m = certify_point(r, 400.0)
    res[f"k1_{k1}"] = m
    print(f"k1={k1}: {m.get('cls')} c={m.get('c_med')}", flush=True)
for Dv in (0.55, 0.6, 0.7, 0.75):
    r = run(p=dict(k1=-0.7, Dv=Dv, tau=5.0), T=400.0, dx=0.5, stepper="imexfft", kick_angle=30.0)
    m = certify_point(r, 400.0)
    res[f"Dv_{Dv}"] = m
    print(f"Dv={Dv}: {m.get('cls')} c={m.get('c_med')}", flush=True)
# tau split edge
for tau in (5.5, 5.6):
    r = run(p=dict(k1=-0.7, Dv=0.65, tau=tau), T=400.0, dx=0.5, stepper="imexfft", kick_angle=30.0)
    m = certify_point(r, 400.0)
    res[f"tau_{tau}"] = m
    print(f"tau={tau}: {m.get('cls')} c={m.get('c_med')}", flush=True)
json.dump(res, open(OUT + "/cert7_window.json", "w"), indent=1)
