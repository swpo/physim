"""Read-only h9 toy audit. No integration, archive reads, or production edits.
Run from repository root with ~/.venvs/bk3/bin/python -B .../toy_checks.py.
The only output file is toy_results.json beside this script.
"""
import hashlib
import importlib
import json
import math
from pathlib import Path
import sys
import warnings

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import h9_dev as H9
from blobkit import metrics_v1 as BK1
from blobkit import metrics_v2 as BK2
from blobkit.soup.sim_v1 import blob_list_fast
import blobkit.soup.sim_v1 as SV1

MV3 = H9.MV3
L = 128.0
T = 128  # 640 tu of track-frame coverage at the native REC=5 cadence.
results = {}


def digest(path):
    p = Path(path)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


results["provenance"] = {
    "python": sys.version,
    "executable": sys.executable,
    "numpy": np.__version__,
    "scipy": scipy.__version__,
    "sources": {name: digest(mod.__file__) for name, mod in
                [("h9", H9), ("metrics_v3", MV3), ("blobkit_metrics_v1", BK1),
                 ("blobkit_metrics_v2", BK2), ("blobkit_sim_v1", SV1)]},
    "constants": {key: getattr(MV3, key) for key in
                  ["BURN", "REC", "CREC", "LATE_W_MIN", "D7B_MIN_TRACK",
                   "D7B_MIN_ROWS", "D7B_KMAX", "D7B_PERSIST", "D7B_SIL_FLOOR"]},
    "constraints": "Synthetic arrays only; no physical simulation or archive extraction.",
}


def stationary(labels, centers, nt=T):
    pos = [np.tile(np.asarray(p, float), (nt, 1)) for p in centers]
    times = [500.0 + np.arange(nt) * 5.0 for _ in labels]
    return np.asarray(labels, int), pos, times


def score(case, P=4, **kw):
    return H9.h9_from_frames(*case, L, P=P, **kw)


def shifted(case, offsets):
    lab, pos, times = case
    return lab.copy(), [(p + offsets) % L for p in pos], times


# Actual recording helper, not a simulator: one positive grid cell.
N, dx = 64, 0.5
field = np.zeros((N, N))
field[8, 48] = 2.0
blob = blob_list_fast(field, 1.0, dx, N * dx)[0]
rec = {"L": N * dx, "na": 1, "t": np.array([500.0, 505.0]),
       "blobs": {0: [[[blob["y"], blob["x"], blob["area"], blob["peak"]]]] * 2}}
tr = BK1.build_tracks(rec)[0]
results["recording_units"] = {
    "N": N, "dx": dx, "L": N * dx, "cell_yx": [8, 48],
    "blob": blob, "track_yx": np.asarray(tr["yx"]).tolist(),
    "P4_correct_patch_yx": [int(blob["y"] / (N * dx) * 4),
                             int(blob["x"] / (N * dx) * 4)],
    "P4_wrong_divide_by_N_patch_yx": [int(blob["y"] / N * 4),
                                       int(blob["x"] / N * 4)],
}
assert np.allclose([blob["y"], blob["x"], blob["area"]], [4.25, 24.25, 0.25])

# Wrapped distance in bond_frames uses the same physical L.
bond_rec = {"L": L, "t": 500.0 + np.arange(10) * 5.0, "_tracks": [
    {"tid": i, "ks": list(range(10)), "yx": [(64.0, x)] * 10}
    for i, x in enumerate([0.25, 127.75])
]}
bt, be, bd = MV3.bond_frames(bond_rec, r_bond=10.0)
results["bond_units"] = {"wrapped_pair_distance": float(BK1.min_image(127.5, L)),
                         "bond_times": bt.tolist(),
                         "edge_counts": [len(e) for e in be]}
assert all(len(e) == 1 for e in be)

# Stable binary patches; many independent tracks per patch, equal duration.
labels = np.repeat([0, 1], 8)
centers = [(16.0 + (i % 8) * .25, 16.0 + 64.0 * (i // 8)) for i in range(16)]
static = stationary(labels, centers)
results["stationary_binary"] = score(static)
results["stationary_binary_controls"] = H9.controls(*static, L)
assert results["stationary_binary"]["h9"] == 1.0

# Rigid translation preserves identity and separation at every time.
move_x = np.stack([np.zeros(T), np.arange(T) * (L / T)], axis=1)
move_y = move_x[:, ::-1]
results["rigid_translation_parallel_to_separation"] = score(shifted(static, move_x))
results["rigid_translation_perpendicular_to_separation"] = score(shifted(static, move_y))
assert results["rigid_translation_parallel_to_separation"]["h9"] == 0.0
assert results["rigid_translation_perpendicular_to_separation"]["h9"] == 1.0

angle = (np.arange(T) + .5) * 2 * np.pi / T
rot_pos = [np.stack([64 + (40 + (i % 8) * .1) * np.sin(angle + s * np.pi),
                    64 + (40 + (i % 8) * .1) * np.cos(angle + s * np.pi)], axis=1)
           for i, s in enumerate(labels)]
results["rigid_rotation"] = score((labels, rot_pos, static[2]))
assert results["rigid_rotation"]["h9"] == 0.0

# Not just an all-tied median: x order alternates between the two y-regions.
y_centers = [(16.0 + 64.0 * s, 10.0 + j + .25 * s)
             for s in range(2) for j in range(8)]
y_case = stationary(labels, y_centers)
results["y_separation_not_a_ceiling"] = {
    "actual": score(y_case), "controls": H9.controls(*y_case, L)}
assert results["y_separation_not_a_ceiling"]["actual"]["h9"] == 1.0
assert results["y_separation_not_a_ceiling"]["controls"]["seg_control"] == 0.0

# A={u1,u2}, B={u1,u3}: common field has half of all track-frames.
comp_labels, comp_centers = [], []
for region, species in enumerate([(0, 1), (0, 2)]):
    for s in species:
        for j in range(8):
            comp_labels.append(s)
            comp_centers.append((16.0 + j * .25, 16.0 + region * 64))
comp_case = stationary(comp_labels, comp_centers)
results["distinct_multifield_compartments"] = score(comp_case)

# Identical copies of {u1,u2}, with a 2-unit internal separation.
# The locale composition never differs. Patch boundaries split the copies.
repeat_labels, repeat_centers, coincident_centers = [], [], []
for y in np.arange(8.0, 128.0, 16.0):
    for x in (32.0, 96.0):
        for s in (0, 1):
            repeat_labels.append(s)
            repeat_centers.append((y, x + (2 * s - 1)))
            coincident_centers.append((y, x))
repeat_case = stationary(repeat_labels, repeat_centers)
results["identical_multifield_locales_boundary_split"] = score(repeat_case)
results["identical_multifield_locales_global_shift_2"] = score(shifted(repeat_case, np.array([0., 2.])))
results["identical_multifield_locales_P2"] = score(repeat_case, P=2)
results["identical_multifield_locales_coincident"] = score(stationary(repeat_labels, coincident_centers))
assert results["identical_multifield_locales_boundary_split"]["h9"] == 1.0
assert results["identical_multifield_locales_global_shift_2"]["h9"] == 0.0
assert results["identical_multifield_locales_P2"]["h9"] == 0.0
assert results["identical_multifield_locales_coincident"]["h9"] == 0.0


def persistence_record(nt, transient_last=None):
    t = 500.0 + np.arange(nt) * 5.0
    templates = {s: [[y, x, 4.0, 2.0] for y in (10.0 + s * 96, 22.0 + s * 96)
                     for x in (10.0 + s * 96, 22.0 + s * 96)] for s in (0, 1)}
    blobs = {s: [templates[s] if (s == 0 or transient_last is None or k >= nt - transient_last)
                  else [] for k in range(nt)] for s in (0, 1)}
    rec = {"L": L, "na": 2, "nc": 0, "t": t, "ct": t[::5], "memf": {}, "blobs": blobs}
    rec["_tracks"] = BK1.build_tracks(rec)
    v2_stub = {"D": {"d1": {"n_end": 8}, "d3": {"gr": None}, "d5": {"phase": "frozen"}}}
    d7b = MV3.d7b_species(rec, v2_stub)
    lab, why, pos, times = H9.track_table(rec, v2_stub)
    return {"d7b": d7b, "h9_species": len(np.unique(lab)) if lab is not None else 0,
            "h9": H9.h9_from_frames(lab, pos, times, L) if lab is not None else {"why": why}}


results["d7b_vs_h9_200tu_only"] = persistence_record(40)
results["d7b_vs_h9_600tu"] = persistence_record(120)
results["d7b_vs_h9_600tu_plus_200tu_late_arrival"] = persistence_record(120, transient_last=40)
assert results["d7b_vs_h9_200tu_only"]["d7b"]["n_species"] == 0
assert results["d7b_vs_h9_200tu_only"]["h9_species"] == 2
assert results["d7b_vs_h9_200tu_only"]["h9"]["h9"] == 1.0
assert results["d7b_vs_h9_600tu"]["d7b"]["n_species"] == 2
assert results["d7b_vs_h9_600tu_plus_200tu_late_arrival"]["d7b"]["n_species"] == 1
assert results["d7b_vs_h9_600tu_plus_200tu_late_arrival"]["h9"]["h9"] == 1.0

# Permutations preserve label counts over tracks, NOT frame-weighted margins.
# Twelve long tracks occupy separate patches; four short tracks share patch 15.
# Original labels separate perfectly by patch, despite I0 exceeding Hs.
dur = [80] * 12 + [20] * 4
ulab = np.array([0] * 12 + [1] * 4)
upos = [np.tile([16.0 + 32.0 * (i // 4), 16.0 + 32.0 * (i % 4)], (80, 1))
        for i in range(12)] + [np.tile([112.0, 112.0], (20, 1)) for _ in range(4)]
utimes = [500.0 + np.arange(80) * 5.0 for _ in range(12)] + [650.0 + np.arange(20) * 5.0 for _ in range(4)]
u_result = score((ulab, upos, utimes))
rng = np.random.default_rng(0)
null_masses, null_H = [], []
for _ in range(60):
    perm = rng.permutation(ulab)
    mass = np.bincount(perm, weights=dur, minlength=2)
    p = mass / mass.sum()
    null_masses.append(mass[1])
    null_H.append(float(-sum(p[p > 0] * np.log(p[p > 0]))))
results["unequal_durations_null"] = {
    "score": u_result, "track_duration_frames": dur,
    "observed_species_1_frames": 80,
    "permuted_species_1_frames_min_max": [min(null_masses), max(null_masses)],
    "permuted_Hs_min_max": [min(null_H), max(null_H)],
    "permuted_Hs_mean": float(np.mean(null_H)),
}
assert u_result["I"] == u_result["Hs"]
assert u_result["I0"] > u_result["Hs"]
assert u_result["h9"] == 0.0

# Bounded/degenerate behavior. Invalid-input handling is observed, not fixed.
results["one_species"] = score((np.zeros(len(labels), int), static[1], static[2]))
one_patch = stationary(labels, [(16, 16)] * len(labels))
results["one_patch"] = score(one_patch)
results["few_frames"] = score(stationary([0, 1], [(16, 16), (80, 80)], nt=10))
results["no_shared_half_support"] = score((labels, static[1], [np.full(T, 500.0) for _ in labels]))
results["label_permutation"] = score((1 - static[0], static[1], static[2]))
assert results["label_permutation"] == results["stationary_binary"]


def capture(fn):
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        try:
            value = fn()
            out = {"result": value}
        except Exception as ex:
            out = {"exception": type(ex).__name__, "message": str(ex)}
    out["warnings"] = sorted(set(str(w.message) for w in ws))
    return out


results["invalid_empty_tracks"] = capture(lambda: H9.h9_from_frames(np.array([], int), [], [], L))
results["invalid_B_zero"] = capture(lambda: score(static, B=0))
results["invalid_zero_L"] = capture(lambda: H9.h9_from_frames(*static, 0.0))
results["invalid_empty_record"] = capture(lambda: H9.track_table({"t": []}, {"D": {}}))

def json_safe(value):
    # Preserve invalid-case nonfinite outputs as explicit strings, not invalid JSON.
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value


out_path = HERE / "toy_results.json"
text = json.dumps(json_safe(results), indent=2, sort_keys=True, allow_nan=False)
out_path.write_text(text + "\n")
print(text)
print("PASS: all toy expectations; wrote", out_path)
