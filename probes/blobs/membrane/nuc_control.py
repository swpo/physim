import sys, os, numpy as np, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
etaw = float(sys.argv[1]); T = float(sys.argv[2])
r = sim.run(tau1=5.8, tau2=2.5, Dv1=4/5.8, Dv2=1.6, etaw12=etaw,
            init_from="MEMBRANE_N10.npz", init_slot=2,
            T=T, rec_tu=25.0, stop_split=False, save_fields=False,
            n2_expect=10)
out = dict(kind="nucleation_control", name=f"NUC_w{etaw}", etaw=etaw, T=T,
           status=r["status"], ncomp1=[int(x) for x in r["ncomp1"]],
           ncomp2_final=int(r["ncomp2"][-1]),
           nucleated=bool((r["ncomp1"] > 0).any()))
sim.append_result(out)
print(json.dumps(dict(etaw=etaw, nucleated=out["nucleated"], nc1_max=int(max(out["ncomp1"])))))
