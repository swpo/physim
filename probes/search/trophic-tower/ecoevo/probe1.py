
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *
import json
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
TC = json.load(open(WD + "/tcstar.json"))

for (c, m_, G0) in [(0.01, 0.02, 1.3), (0.01, 0.02, 0.7), (0.0, 0.02, 1.0)]:
    t0 = time.time()
    rec, m = run_and_measure_evo(TC, dict(c=c, m=m_, G0=G0), L=64, nticks=120000, seed=0)
    print(f"c={c} m={m_} G0={G0}: st={m.get('status')} eco_st={m.get('eco',{}).get('status')} "
          f"T3={m.get('eco',{}).get('T3')} G_end={m.get('G_end') and round(m['G_end'],3)} "
          f"sdG={m.get('sdG_med') and round(m['sdG_med'],3)} mode={m.get('mode')} "
          f"tau4={m.get('tau4') and round(m['tau4'],0)} fit4={m.get('fit4',{}).get('model')}/{m.get('fit4',{}).get('r2')} "
          f"entr={m.get('entrain_ratio') and round(m['entrain_ratio'],2)} sep34={m.get('sep34') and round(m['sep34'],1)} "
          f"rt={round(time.time()-t0,1)}s", flush=True)
    np.save(f"/tmp/ee_gbar_c{c}_G{G0}.npy",
            np.vstack([rec["Gbar"], rec["sdG"], rec["meanP"], rec["meanH"]]))
print("DONE probe1")
