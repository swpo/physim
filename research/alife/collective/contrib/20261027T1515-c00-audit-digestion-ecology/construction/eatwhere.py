"""Where does digestion happen? eat = k2 c_a^2 c_b^2 (world.py l.118-119) split by distance to the nearest prey body.
usage: eatwhere.py STATE.npz SEED"""
import sys, os, json
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import ndimage
from arms import load, label_p
import world_dump as WD
w = WD.w
s = load(sys.argv[1], int(sys.argv[2])); P = s["par"]; H, W = s["shape"]
ca, cb = w._c(s["pa"]), w._c(s["pb"])
eat = np.minimum(P["k2"] * ca ** 2 * cb ** 2, 0.5 * ca / P["dt"])
La, na = label_p(ca)
d = ndimage.distance_transform_edt(np.tile(La == 0, (3, 3)))[H:2 * H, W:2 * W]
far = d > 6
out = dict(t=float(s["t"]), eat_total=float(eat.sum()), share_inside_prey=float(eat[d == 0].sum() / eat.sum()),
           share_0_3px=float(eat[(d > 0) & (d <= 3)].sum() / eat.sum()), share_3_6px=float(eat[(d > 3) & (d <= 6)].sum() / eat.sum()),
           share_gt6px=float(eat[far].sum() / eat.sum()), ca_bath_median_gt6px=float(np.median(ca[far])), ca_mean=float(ca.mean()),
           prey_body_area_frac=float((La > 0).mean()), cb_bath_median=float(np.median(cb[cb < 0.3])),
           prey_material_in_bodies_frac=float(ca[La > 0].sum() / ca.sum()))
print(json.dumps(out))
