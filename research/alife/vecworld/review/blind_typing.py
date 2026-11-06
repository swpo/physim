"""Does the hidden output permutation hide coordinate meaning? A blind typing of the 144 Phi_objects
observation coordinates from passive observations only (permuted by out_map, quantised to 1e-3).
  presence coord  = takes only the values {0, 1}
  slot membership = zero pattern over time equal to a presence coord's on >= 99% of ticks
  position pair   = two coords of one slot with a^2 + b^2 = const (= (L/2 pi)^2) whenever present
Scored against the true out_map (used for scoring only)."""
import glob
import json

import numpy as np

INT = "/home/user/evalwork/vecworld/integrate"
import sys
sys.path.insert(0, INT)
import lenia_world as LW   # noqa: E402
vw = LW.vw
specs, parts = LW.make_specs("A_gliders")
w = vw.VectorWorld(specs["objects"], world_seed=0)
om = w.out_map                                   # agent obs j <- level-1 index om[j]
true_slot = om // LW.NF
true_feat = np.array(LW.OBJ_FEATURES)[om % LW.NF]
files = sorted(glob.glob(f"{INT}/data/A_gliders/base_*.npz"))
res = {}
for label, fl in (("1 episode (301 obs)", files[:1]), ("4 episodes", files[:4]), ("24 episodes", files)):
    Y = np.concatenate([np.load(f)["Yo"] for f in fl])[:, om]
    Y = 1e-3 * np.round(Y / 1e-3)
    Z = Y == 0
    pres = [j for j in range(Y.shape[1]) if np.isin(Y[:, j], (0.0, 1.0)).all() and (Y[:, j] == 1).any()]
    slot_of = -np.ones(Y.shape[1], int)
    for p in pres:
        agree = (Z == Z[:, [p]]).mean(0)
        cand = np.flatnonzero(agree >= 0.99)
        for c in cand:
            if slot_of[c] < 0 or agree[c] > (Z[:, c] == Z[:, pres[slot_of[c]]]).mean():
                slot_of[c] = pres.index(p)
    ok_slot = [slot_of[j] >= 0 and true_slot[pres[slot_of[j]]] == true_slot[j] for j in range(Y.shape[1])]
    # position pairs within each recovered slot
    E2 = (128 / (2 * np.pi)) ** 2
    pairs_ok, pairs_found = 0, 0
    for s, p in enumerate(pres):
        on = Y[:, p] == 1
        mem = [j for j in np.flatnonzero(slot_of == s) if j != p]
        for a in range(len(mem)):
            for b in range(a + 1, len(mem)):
                r = Y[on, mem[a]] ** 2 + Y[on, mem[b]] ** 2
                if on.any() and np.abs(r - E2).max() < 0.5:
                    pairs_found += 1
                    fa, fb = true_feat[mem[a]], true_feat[mem[b]]
                    pairs_ok += {fa[0], fb[0]} <= {"x", "y"} and fa[0] == fb[0]
    res[label] = {"presence_coords_found": len(pres),
                  "presence_correct": int(sum(true_feat[p] == "present" for p in pres)),
                  "coords_assigned_to_correct_slot_frac": float(np.mean(ok_slot)),
                  "position_pairs_found": pairs_found, "position_pairs_correct": int(pairs_ok)}
    print(label, res[label])
json.dump(res, open("/home/user/evalwork/vecworld_integrate_review/blind_typing.json", "w"), indent=1)
