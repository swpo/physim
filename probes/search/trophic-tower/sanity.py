
import sys, time, json
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from trophic_core import *
from hier_metrics import save_strip
import numpy as np

# Hastings-Powell 1991 classic (chaotic teacup): a1=5,b1=3,a2=0.1,b2=2,d1=0.4,d2=0.01
tc = dict(sigma1=3.0, g1=5/3, xi1=(5/3)/0.4, sigma2=2.0, xi2=(0.1/2)/0.01,
          rho=0.01/0.4, DH=0.05, Delta=2.0, nu=0.02)
t0 = time.time()
rec, m = run_and_measure(tc, L=64, nticks=40000, seed=0)
print("runtime", round(time.time()-t0,1), "s")
for k in ("status","meanH_end","meanP_end","meanR_end","top_var","fits_all","T_units",
          "tau1_units","tau2_units","sep12_t","sep23_t","ell1","ell2","npatch_med",
          "spatial_cv","wave_speed","G1","G2","cap_hits"):
    print(k, "=", m.get(k))
if rec.get("snaps"):
    R,H,P = rec["snaps"][-1]
    save_strip([R,H,P], "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/strips/sanity_RHP.png",
               titles=["R","H","P"])
import numpy as np
np.save("/tmp/tt_sanity_mh.npy", np.vstack([rec["meanR"],rec["meanH"],rec["meanP"]]))
