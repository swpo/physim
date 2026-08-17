
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

TC30 = dict(TC); TC30["rho"] = 0.030
results = []
cases = [
    ("R1 rho.030 m.2",  TC30, dict(c=0.0075, m=0.2,  G0=1.5), 280000),
    ("R2 rho.030 m.25", TC30, dict(c=0.0075, m=0.25, G0=1.5), 280000),
    ("R3 logmut m.15",  TC,   dict(c=0.0075, m=0.15, G0=1.5, logmut=1), 280000),
    ("R4 logmut m.25",  TC,   dict(c=0.0075, m=0.25, G0=1.5, logmut=1), 280000),
    ("R5 rho.030 m.2 up", TC30, dict(c=0.0075, m=0.2, G0=0.6), 280000),
    ("R6 rho.030 frozen1", TC30, dict(c=0.0075, m=0.0, G0=1.0), 56000),
]
for tag, tce, evo, nt in cases:
    try:
        rec, m = run_and_measure_evo(tce, evo, L=64, nticks=nt, seed=0, snaps=False)
        eco = m.get("eco", {})
        tf = eco.get("top_fit", {})
        extra = f"ecoTop={tf.get('model')}/{tf.get('r2')} T2={eco.get('T2') and round(eco['T2'],1)} s12={eco.get('sep12') and round(eco['sep12'],1)}"
    except Exception as e:
        m = dict(status="error", error=str(e)); extra = ""
    results.append(dict(stage="rescue", id=tag, tc_eco=tce, evo=evo, seed=0, L=64,
                        nticks=nt, **jsonable({k: v for k, v in m.items() if k != "evo"})))
    report(tag, evo, m, extra)
    json.dump(results, open(EWD + "/results_rescue.json", "w"), indent=1)
print("DONE rescue")
