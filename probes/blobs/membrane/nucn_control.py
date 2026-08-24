import sys, os, numpy as np, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
etaw = float(sys.argv[1]); T = float(sys.argv[2]); sd = int(sys.argv[3])
r = sim.run(tau1=5.8, tau2=2.5, Dv1=4/5.8, Dv2=1.6, etaw12=etaw,
            init_from="MEMBRANE_N10.npz", init_slot=2, noise=2e-3, seed=sd,
            T=T, rec_tu=25.0, stop_split=False, save_fields=False, n2_expect=10)
out = dict(kind="nucleation_control_noisy", name=f"NUCN_w{etaw}_s{sd}", etaw=etaw, T=T,
           status=r["status"], nc1_max=int(max(r["ncomp1"])) if len(r["ncomp1"]) else 0,
           ncomp2_final=int(r["ncomp2"][-1]),
           nucleated=bool((r["ncomp1"] > 0).any()))
sim.append_result(out)
print(json.dumps(out))
