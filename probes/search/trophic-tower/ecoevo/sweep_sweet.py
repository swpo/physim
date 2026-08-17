
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
print("=== sweet-spot attempt: G*~1 via m=0.22, c=0.005, rho=0.030 ===")
TC30 = dict(TC); TC30["rho"] = 0.030
for sd in (0, 1):
    evo = dict(c=0.005, m=0.22, G0=1.2)
    try:
        rec, m = run_and_measure_evo(TC30, evo, L=64, nticks=280000, seed=sd, snaps=(sd == 0))
        eco = m.get("eco", {})
        tf = eco.get("top_fit", {})
        extra = f"ecoTop={tf.get('model')}/{tf.get('r2')} T2={eco.get('T2') and round(eco['T2'],1)}"
        if sd == 0:
            np.save(EWD + "/sweet_sd0.npy", np.vstack([rec["Gbar"], rec["sdG"], rec["meanP"], rec["meanH"]]))
            from hier_metrics import save_strip
            R, H, P = rec["snaps"][-1]; G = rec["snapsG"][-1]
            save_strip([R, H, P, G], EWD + "/strips/sweet_RHPG.png",
                       titles=["R", "H", "P", "G"])
    except Exception as e:
        m = dict(status="error", error=str(e)); extra = ""
    row = dict(stage="sweet", id="sweet", tc_eco=TC30, evo=evo, seed=sd, L=64, nticks=280000,
               **jsonable({k: v for k, v in m.items() if k != "evo"}))
    results.append(row)
    report("sweet" + f" sd={sd}", evo, m, extra)
    json.dump(results, open(EWD + "/results_sweet.json", "w"), indent=1)
print("DONE sweet")
