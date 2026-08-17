
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
TC = json.load(open(WD + "/tcstar.json"))

for m_ in (0.05, 0.1, 0.2):
    t0 = time.time()
    rec, m = run_and_measure_evo(TC, dict(c=0.01, m=m_, G0=1.5), L=64,
                                 nticks=240000, seed=0, snaps=False)
    gb = rec["Gbar"]; sd = rec["sdG"]
    qtr = len(gb)//4
    print(f"m={m_}: st={m['status']} G(t): start={gb[0]:.3f} 1/4={gb[qtr]:.3f} "
          f"1/2={gb[2*qtr]:.3f} 3/4={gb[3*qtr]:.3f} end={gb[-1]:.3f} "
          f"sdG_med={np.median(sd[qtr:]):.3f} eco_T3={m['eco'].get('T3') and round(m['eco']['T3'],1)} "
          f"ecoG1={m['eco'].get('G1')} fit4={m.get('fit4',{}).get('model')}/{m.get('fit4',{}).get('r2')} "
          f"tau4={m.get('tau4') and round(m['tau4'],0)} rt={round(time.time()-t0,1)}s", flush=True)
    np.save(f"/tmp/ee_cal_m{m_}.npy", np.vstack([gb, sd, rec["meanP"]]))
print("DONE calib")
