"""Blind grouping of the 192 Phi_coarse observation coords into per-block triples (c0 mean, c1 mean,
mean A_sum^2) from one episode: coords whose quantised zero patterns agree best."""
import glob, json, sys
import numpy as np
INT = "/home/user/evalwork/vecworld/integrate"
sys.path.insert(0, INT)
import lenia_world as LW
vw = LW.vw
specs, parts = LW.make_specs("A_gliders")
w = vw.VectorWorld(specs["coarse"], world_seed=0)
om = w.out_map
blk = np.where(om < 128, om % 64, om - 128)          # true block of each agent coord
f = sorted(glob.glob(f"{INT}/data/A_gliders/base_*.npz"))[0]
Y = np.load(f)["Yc"][:, om]
Y = 1e-3 * np.round(Y / 1e-3)
Z = (Y == 0).astype(float)
# for each coord, its best partner by co-occurrence of (near-)empty ticks
agree = 1 - np.abs(Z[:, :, None] - Z[:, None, :]).mean(0)
np.fill_diagonal(agree, -1)
part = agree.argmax(1)
ok = float((blk[part] == blk).mean())
frac_zero = float(Z.mean())
# m2 vs mean: m2 >= (c0+c1)^2/... separate by scale: coords whose max exceeds ~1.5x the 98th pct of others
print(json.dumps({"best_partner_in_same_block_frac": ok, "frac_zero_entries": frac_zero}))
json.dump({"best_partner_in_same_block_frac": ok, "frac_zero_entries": frac_zero},
          open("/home/user/evalwork/vecworld_integrate_review/blind_coarse.json", "w"))
