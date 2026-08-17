
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
EWD = WD + "/ecoevo"
TC = json.load(open(WD + "/tcstar.json"))

def jsonable(m):
    def cv(v):
        if isinstance(v, (np.floating, np.integer)): return float(v)
        if isinstance(v, dict): return {k: cv(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)): return [cv(x) for x in v]
        return v
    return {k: cv(v) for k, v in m.items()}

def report(tag, evo, m, extra=""):
    eco = m.get("eco", {})
    print(f"[{tag}] c={evo['c']} m={evo['m']} G0={evo['G0']}: st={m.get('status')} "
          f"G*={m.get('Gstar') and round(m['Gstar'],3)} tau4={m.get('tau4') and round(m['tau4'],0)} "
          f"mode={m.get('mode')} fit4={m.get('fit4',{}).get('model')}/{m.get('fit4',{}).get('r2')} "
          f"sdG={m.get('sdG_med') and round(m['sdG_med'],3)} T3={eco.get('T3') and round(eco['T3'],1)} "
          f"ecoG1={eco.get('G1')} ecoG2={eco.get('G2')} s34={m.get('sep34') and round(m['sep34'],1)} "
          f"entr={m.get('entrained')} stat={m.get('stationary')} rt={m.get('runtime_s')}s {extra}", flush=True)

results = []
cid = 0
for c in (0.005, 0.0075, 0.01, 0.0125):
    for m_ in (0.1, 0.2):
        for G0 in (1.5, 0.6):
            evo = dict(c=c, m=m_, G0=G0)
            nt = 320000 if m_ <= 0.1 else 240000
            try:
                rec, m = run_and_measure_evo(TC, evo, L=64, nticks=nt, seed=0, snaps=False)
            except Exception as e:
                m = dict(status="error", error=str(e))
            row = dict(stage="E1", id=f"e1-{cid:02d}", evo=evo, seed=0, L=64, nticks=nt,
                       **jsonable({k: v for k, v in m.items() if k != "evo"}))
            results.append(row); cid += 1
            report(row["id"], evo, m)
            json.dump(results, open(EWD + "/results_e1.json", "w"), indent=1)
print("DONE E1")
