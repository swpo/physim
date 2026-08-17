
import sys, json, time
import numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower/ecoevo")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from ecoevo_core import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
WD = "/Users/spoho/Documents/prime/test/physim/probes/search/trophic-tower"
EWD = WD + "/ecoevo"
TC = json.load(open(WD + "/tcstar.json"))

# start AT the attractor, moderate mutation
for m_ in (0.1, 0.15):
    rec, m = run_and_measure_evo(TC, dict(c=0.0075, m=m_, G0=0.8), L=64,
                                 nticks=160000, seed=0, snaps=True)
    eco = m["eco"]
    print(f"m={m_}: Gstar={m['Gstar']:.3f} sdG={m['sdG_med']:.3f}")
    print("  eco:", {k: eco.get(k) for k in ("T3","T2","tau1","sep12","sep23","spatial_cv","npatch_med","G1","G2","fast_amp_frac")})
    print("  top:", eco.get("top_fit"), flush=True)
    if m_ == 0.15:
        dt_mac = 0.5
        t = np.arange(len(rec["meanH"])) * dt_mac
        fig, ax = plt.subplots(4, 1, figsize=(11, 8))
        ax[0].plot(t, rec["meanP"], "r", lw=0.8); ax[0].set_ylabel("mean P")
        ax[1].plot(t, rec["meanH"], "b", lw=0.6); ax[1].set_ylabel("mean H")
        ax[2].plot(t, rec["Gbar"], "purple", lw=0.8); ax[2].set_ylabel("<G> biomass-wt")
        ax[2].plot(t, rec["Gq10"], "k:", lw=0.5); ax[2].plot(t, rec["Gq90"], "k:", lw=0.5)
        ax[3].plot(t, rec["blocksH"][:, 40], "k", lw=0.5); ax[3].set_ylabel("block H")
        ax[3].set_xlim(2000, 3000); ax[3].set_xlabel("time units")
        fig.tight_layout(); fig.savefig(EWD + "/strips/diag_evolved_state.png", dpi=110)
        plt.close(fig)
        from hier_metrics import save_strip
        R, H, P = rec["snaps"][-1]; G = rec["snapsG"][-1]
        save_strip([R, H, P, G], EWD + "/strips/diag_RHPG.png",
                   titles=["R", "H", "P", "G (genotype)"])
print("DONE diag")
