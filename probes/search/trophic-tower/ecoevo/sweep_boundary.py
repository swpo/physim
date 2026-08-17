
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
print("=== dissolution boundary: c=0.0075, G0=1.0, 120k ticks, 3 seeds ===")
for m_ in (0.02, 0.04, 0.06, 0.09, 0.12, 0.15):
    ok = 0
    for sd in (0, 1, 2):
        evo = dict(c=0.0075, m=m_, G0=1.0)
        try:
            rec, m = run_and_measure_evo(TC, evo, L=64, nticks=120000, seed=sd, snaps=False)
            eco = m.get("eco", {})
            coher = bool(eco.get("G1") and eco.get("G2"))
            ok += int(coher)
            tf = eco.get("top_fit", {})
            row = dict(stage="boundary", id=f"bnd_m={m_}", evo=evo, seed=sd, L=64,
                       nticks=120000, coherent=coher,
                       **jsonable({k: v for k, v in m.items() if k != "evo"}))
        except Exception as e:
            row = dict(stage="boundary", id=f"bnd_m={m_}", evo=evo, seed=sd, L=64,
                       nticks=120000, status="error", error=str(e), coherent=False)
            m = dict(status="error"); eco = {}; tf = {}
        results.append(row)
        print(f"m={m_} sd={sd}: st={m.get('status')} top={tf.get('model')}/{tf.get('r2')} "
              f"T3={eco.get('T3') and round(eco['T3'],1)} T2={eco.get('T2') and round(eco['T2'],1)} "
              f"s12={eco.get('sep12') and round(eco['sep12'],1)} s23={eco.get('sep23') and round(eco['sep23'],1)} "
              f"ecoG1={eco.get('G1')} ecoG2={eco.get('G2')} COHER={row.get('coherent')} "
              f"sdG={m.get('sdG_med') and round(m['sdG_med'],3)} <G>end={m.get('Gstar') and round(m['Gstar'],3)} "
              f"rt={m.get('runtime_s')}s", flush=True)
        json.dump(results, open(EWD + "/results_boundary.json", "w"), indent=1)
    print(f"  ==> m={m_}: coherent {ok}/3", flush=True)
print("DONE boundary")
