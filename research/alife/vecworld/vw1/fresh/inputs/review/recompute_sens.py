"""Checker: (c) numbers from results/sensitivity.json, and shares recomputed from sensitivity_maps.npz."""
import json

import numpy as np
import scipy.ndimage as ndi

R0 = "/home/user/evalwork/vecworld/vw1/fresh/inputs/results"
S = json.load(open(f"{R0}/sensitivity.json"))
M = np.load(f"{R0}/sensitivity_maps.npz")
print("states", S["states"], "n_eff", S["n_eff_outputs"], "eps", S["eps"], "total s", S.get("seconds_total"))


def n90(v):
    o = np.sort(v.ravel())[::-1]
    c = np.cumsum(o) / o.sum()
    return int(np.searchsorted(c, 0.9) + 1)


for s in S["states"]:
    r = S["per_state"][str(s)]
    Sm = M[f"s{s}_matter"].astype(float)
    foot = Sm > 1e-3
    dil = ndi.binary_dilation(np.tile(foot.reshape(128, 128), (3, 3)), iterations=4)[128:256, 128:256].ravel()
    print(f"--- state {s}: footprint {foot.mean():.4f} (json {r['footprint_frac_A_sum_gt_1e-3']:.4f}); null {r['fd_null_check_max_abs']};"
          f" primal vs rollout {[r[f'N{N}']['primal_vs_rollout_max_abs'] for N in (1, 2, 4)]}; jvp/vjp N4 {r['jvp_vs_vjp_N4_max_rel']:.2g};"
          f" move admissible {r['move_inputs_admissible']}")
    for N in (1, 2, 4):
        dep = M[f"s{s}_dep_N{N}"].astype(float)
        fl = r[f"N{N}"]["deposit"]["direct_block_mean_floor"]
        ex = np.maximum(dep - fl, 0)
        o = np.argsort(-ex)
        nex = n90(ex)
        print(f"N{N}: s2 n90 {n90(dep**2)} ({n90(dep**2)/dep.size:.4%}) json {r[f'N{N}']['deposit']['shares']['s2']['n_cells_for_90pct']};"
              f" s share {n90(dep)/dep.size:.4f} json {r[f'N{N}']['deposit']['shares']['s']['share_cells_for_90pct']:.4f};"
              f" floor {fl:.3g}; excess share {nex/dep.size:.4f} within4px {dil[o[:nex]].mean():.4f};"
              f" max {dep.max():.3g}; ad_norm_median dep {r['ad_norm_median'][f'N{N}_deposit']:.3g} move {r['ad_norm_median'][f'N{N}_move']:.3g}")
    print("ad_norm_median N8", r["ad_norm_median"]["N8_deposit"], r["ad_norm_median"]["N8_move"])
    for N in (1, 2, 4, 8):
        print(f"  N{N} FD rel err median:",
              {f"{k}_{e:g}": round(r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median"], 6) for k in ("deposit", "move") for e in S["eps"]},
              "top:", {f"{k}_{e:g}": round(r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median_by_group"]["top"], 6)
                       for k in ("deposit", "move") for e in S["eps"]})
    for N in (1, 2, 4, 8):
        a = r["amplitude_0.5"]
        print(f"  amp0.5 N{N}:", {k: (round(a[f"N{N}_{k}"]["actual_snr_median"], 4), round(a[f"N{N}_{k}"]["linear_snr_median"], 4),
                                     round(a[f"N{N}_{k}"]["actual_over_linear_norm_median"], 4),
                                     {g: round(v["actual_over_linear_norm_median"], 4) for g, v in a[f"N{N}_{k}"]["by_group"].items()})
                                 for k in ("deposit", "move")})
    print("  oracle Vu", r["oracle_Vu"])
