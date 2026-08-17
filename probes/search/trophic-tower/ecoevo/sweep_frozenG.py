
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
EWD = WD + "/ecoevo"
TC = json.load(open(WD + "/tcstar.json"))

results = []
for G in (0.5, 0.6, 0.75, 0.9, 1.0, 1.2, 1.5, 2.0):
    evo = dict(c=0.0075, m=0.0, G0=G)   # frozen uniform genotype
    try:
        rec, m = run_and_measure_evo(TC, evo, L=64, nticks=56000, seed=0, snaps=False)
        eco = m["eco"]
    except Exception as e:
        m = dict(status="error", error=str(e)); eco = {}
    results.append(dict(stage="frozenG", G=G, evo=evo, seed=0, L=64, nticks=56000,
                        eco={k: (float(v) if isinstance(v, (int, float, np.floating)) else v)
                             for k, v in eco.items() if k != "top_fit"},
                        top=eco.get("top_fit", {}).get("model"),
                        r2=eco.get("top_fit", {}).get("r2")))
    print(f"G={G}: eco st={eco.get('status')} top={eco.get('top_fit',{}).get('model')}/{eco.get('top_fit',{}).get('r2')} "
          f"T3={eco.get('T3') and round(eco['T3'],1)} T2={eco.get('T2') and round(eco['T2'],1)} "
          f"s12={eco.get('sep12') and round(eco['sep12'],1)} s23={eco.get('sep23') and round(eco['sep23'],1)} "
          f"G1={eco.get('G1')} G2={eco.get('G2')}", flush=True)
    json.dump(results, open(EWD + "/results_frozenG.json", "w"), indent=1)
print("DONE frozenG")
