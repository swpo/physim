import sys, time
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy")
from hier_metrics import *
from guild_econ import *
import numpy as np

WD = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"

def quick(tc, T=25000, seed=0, tag=""):
    p = theory_to_raw(tc)
    rng = np.random.default_rng(seed)
    state = init_state(p, rng)
    step = make_stepper(p, rng)
    t0 = time.time()
    fr_hist = []
    blocks = []
    for t in range(T):
        step(state)
        if t % 25 == 0:
            m = macro(state)
            fr_hist.append((t, m["fr_e"]))
        if t >= T - 10000 and t % 20 == 0:
            blocks.append(block_series(state, p["L"]))
        if state[0].sum() < 1e-9:
            break
    m = macro(state)
    V, E, R, W, A = state
    bm = bimodality(A, V)
    ce = contact_enrichment(A, V)
    bt = block_tau(blocks, 20)
    rt = time.time() - t0
    # marginal equalization check: rho * Wm / Rm should ~ 1 at coexistence
    marg = p["rho"] * m["Wm"] / max(m["Rm"], 1e-9)
    print(f"{tag:28s} rt={rt:4.0f}s ncell={m['ncell']:5d} fr_e={m['fr_e']:.3f} "
          f"purity={m['purity']:.3f} bimod={bm['bimod']:.2f} shares=({bm['share_lo']:.2f},{bm['share_hi']:.2f}) "
          f"CE={ce if ce is None else round(ce,2)} Rm={m['Rm']:.3f} Wm={m['Wm']:.3f} marg={marg:.2f} btau={bt}")
    return state, m, bm

base = dict(rho=2.0, yW=0.8, leak=0.5, margin=3.0, sig_mut=0.05)
for over in (0.0, 0.3, 0.6, 1.0, 1.5):
    tc = dict(base, over=over)
    state, m, bm = quick(tc, tag=f"over={over}")
    save_strip([state[2], state[3], state[0], np.where(state[0]>0.05, state[4], np.nan)],
               WD + f"/strips/phaseA_over{over}.png",
               titles=[f"R over={over}", "W", "V", "alloc a"], cmap="viridis")
