"""Anonymisation: the checker's blind structure-recovery rules (physim .../vecworld/review/blind_typing.py and
blind_coarse.py, same rules and thresholds) on the observations of ONE fresh VW-1 agent episode per view
(hero_run.py: World.reset(0), then World.step(None) x 300; what the agent received). The hidden
out_map is used for scoring only.

usage: python -B blind.py SEED   -> results/blind.json
"""
import json
import sys

import numpy as np

BASE = "/home/user/evalwork/vecworld/vw1/fresh/media"
seed = int(sys.argv[1])
FEAT = np.array(["present", "mass", "frac_c1", "x_cos", "x_sin", "y_cos", "y_sin", "rg", "q1", "q2", "vx", "vy"])
NF, K, NC = 12, 12, 192
E2 = (128 / (2 * np.pi)) ** 2


def typing_rule(Y):
    """blind_typing.py: presence = values only {0, 1}; slot = zero pattern agreeing with a presence
    coord on >= 99% of ticks (best agreement wins); position pair = a^2 + b^2 = (L / 2 pi)^2 when present."""
    Z = Y == 0
    pres = [j for j in range(Y.shape[1]) if np.isin(Y[:, j], (0.0, 1.0)).all() and (Y[:, j] == 1).any()]
    slot_of = -np.ones(Y.shape[1], int)
    for p in pres:
        agree = (Z == Z[:, [p]]).mean(0)
        for c in np.flatnonzero(agree >= 0.99):
            if slot_of[c] < 0 or agree[c] > (Z[:, c] == Z[:, pres[slot_of[c]]]).mean():
                slot_of[c] = pres.index(p)
    pairs = []
    for s, p in enumerate(pres):
        on = Y[:, p] == 1
        mem = [j for j in np.flatnonzero(slot_of == s) if j != p]
        for a in range(len(mem)):
            for b in range(a + 1, len(mem)):
                r = Y[on, mem[a]] ** 2 + Y[on, mem[b]] ** 2
                if on.any() and np.abs(r - E2).max() < 0.5:
                    pairs.append((mem[a], mem[b]))
    return pres, slot_of, pairs


def partner_rule(Y):
    """blind_coarse.py: each coordinate's best partner by agreement of exact-zero patterns."""
    Z = (Y == 0).astype(float)
    agree = 1 - np.abs(Z[:, :, None] - Z[:, None, :]).mean(0)
    np.fill_diagonal(agree, -1)
    return agree.argmax(1), float(Z.mean())


def obj_truth(om, off=0):
    k = om - off
    return k // NF, FEAT[k % NF]


def score_typing(Y, slot_true, feat_true, is_obj):
    pres, slot_of, pairs = typing_rule(Y)
    ok = np.array([slot_of[j] >= 0 and is_obj[pres[slot_of[j]]] and slot_true[pres[slot_of[j]]] == slot_true[j]
                   for j in range(Y.shape[1])])
    # checker's criterion: both coords are x_* or both are y_*; strict: also same slot and one cos, one sin
    pc0 = sum(1 for a, b in pairs if is_obj[a] and is_obj[b] and {feat_true[a][0], feat_true[b][0]} <= {"x", "y"}
              and feat_true[a][0] == feat_true[b][0])
    pc = sum(1 for a, b in pairs if is_obj[a] and is_obj[b] and feat_true[a][0] in "xy" and feat_true[a][0] == feat_true[b][0]
             and slot_true[a] == slot_true[b] and {feat_true[a][2:], feat_true[b][2:]} == {"cos", "sin"})
    # slots ever occupied in this episode (truth side): a never-occupied slot's coords are all exactly 0
    occ_slots = {int(slot_true[j]) for j in range(Y.shape[1]) if is_obj[j] and feat_true[j] == "present" and (Y[:, j] == 1).any()}
    occ = np.array([is_obj[j] and int(slot_true[j]) in occ_slots for j in range(Y.shape[1])])
    return {"presence_coords_found": len(pres), "presence_correct": int(sum(is_obj[p] and feat_true[p] == "present" for p in pres)),
            "object_coords": int(is_obj.sum()), "slots_ever_occupied": len(occ_slots),
            "object_coords_assigned_to_correct_slot_frac": float(ok[is_obj].mean()),
            "object_coords_assigned_to_correct_slot": int(ok[is_obj].sum()),
            "coords_of_occupied_slots_assigned_correct": f"{int(ok[occ].sum())} of {int(occ.sum())}",
            "never_occupied_slot_coords_all_zero": bool((Y[:, is_obj & ~occ] == 0).all()),
            "non_object_coords_assigned_to_a_slot": int((slot_of[~is_obj] >= 0).sum()),
            "position_pairs_found": len(pairs), "position_pairs_correct": int(pc0),
            "position_pairs_correct_strict_same_slot_cos_sin": int(pc)}


res = {"seed": seed, "rules": "physim research/alife/vecworld/review/blind_typing.py and blind_coarse.py, unchanged thresholds"}
# objects view
h = np.load(f"{BASE}/results/hero_objects_s{seed}.npz")
Y, om = h["obs64"], h["out_map"]
st, ft = obj_truth(om)
res["objects"] = {"n_obs": int(Y.shape[1]), "ticks": int(len(Y)), **score_typing(Y, st, ft, np.ones(len(om), bool))}
part, fz = partner_rule(Y)
res["objects"]["partner_rule_best_partner_same_slot_frac"] = float((st[part] == st).mean())
# coarse view
h = np.load(f"{BASE}/results/hero_coarse_s{seed}.npz")
Y, om = h["obs64"], h["out_map"]
blk = np.where(om < 128, om % 64, om - 128)
part, fz = partner_rule(Y)
res["coarse"] = {"n_obs": int(Y.shape[1]), "ticks": int(len(Y)), "best_partner_in_same_block_frac": float((blk[part] == blk).mean()),
                 "frac_zero_entries": fz}
pres, slot_of, pairs = typing_rule(Y)
res["coarse"]["typing_rule_presence_coords_found"] = len(pres)
# both view (336 coords: 192 coarse then 144 objects in the designer basis)
h = np.load(f"{BASE}/results/hero_both_s{seed}.npz")
Y, om = h["obs64"], h["out_map"]
is_obj = om >= NC
st = np.where(is_obj, (om - NC) // NF, -1)
ft = np.where(is_obj, FEAT[np.clip(om - NC, 0, None) % NF], "coarse")
res["both"] = {"n_obs": int(Y.shape[1]), "ticks": int(len(Y)), **score_typing(Y, st, ft, is_obj)}
part, fz = partner_rule(Y)
blk = np.where(om < 128, om % 64, np.where(om < NC, om - 128, -1))
c = ~is_obj
res["both"]["coarse_coords_best_partner_in_same_block_frac"] = float((blk[part][c] == blk[c]).mean())
res["both"]["coarse_coords_best_partner_is_object_coord"] = int(is_obj[part][c].sum())
res["both"]["object_coords_best_partner_same_slot_frac"] = float((st[part][is_obj] == st[is_obj]).mean())
json.dump(res, open(f"{BASE}/results/blind.json", "w"), indent=1)
print(json.dumps(res, indent=1))
