import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

for hz, sig in [(5e-4, 0.05), (1e-3, 0.05), (5e-4, 0.10)]:
    tc = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=sig, hazard=hz)
    t0 = time.time()
    out = simulate(tc, T=30000, seed=0, snap_ticks=(29999,),
                   block_win=(15000, 30000), dwell_win=(15000, 30000))
    rt = time.time() - t0
    h = out["hist"]
    bm = bimodality(out["final"][4], out["final"][2])
    bt = block_tau(out["blocks"])
    dw = out["dwells"]
    print(f"hz={hz} sig={sig} rt={rt:.0f}s | ncell={h['ncell'][-1]} Vtot={h['Vtot'][-1]:.0f} "
          f"fr_e={h['fr_e'][-1]:.3f} purity={h['purity'][-1]:.3f} bimod={bm['bimod']:.2f} "
          f"share_lo={bm['share_lo']:.2f} Rm={h['Rm'][-1]:.3f} Wm={h['Wm'][-1]:.3f} "
          f"blocktau={bt} dwell_med={np.median(dw) if len(dw) else None}")
    s = out["snaps"][29999]
    save_strip([s[0], s[1], s[2], s[3]],
               f"/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy/strips/sanity2_hz{hz}_sig{sig}.png",
               titles=[f"R", "W", "V", "alloc a"], cmap="viridis")
