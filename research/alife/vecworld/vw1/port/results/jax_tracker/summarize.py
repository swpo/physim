"""Collect the JAX-tracker verification into summary.json.

usage: python -B summarize.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def load(n):
    p = os.path.join(HERE, n)
    return json.load(open(p)) if os.path.exists(p) else None


def tests(n):
    p = os.path.join(HERE, n)
    if not os.path.exists(p):
        return None
    m = re.findall(r"(\d+) (passed|failed|skipped|error)", open(p).read())
    return {k: int(v) for v, k in m}


L = [load(f"lockstep_{t}.json") for t in ("A", "B")]
L = [x for x in L if x]
keys_sum = ["member_ticks_compared", "slot_map_entries_differing", "discrete_slot_entries_differing",
            "globals_entries_differing", "ticks_with_any_discrete_mismatch", "obs_coords_compared",
            "obs_coords_differing", "continuous_entries_compared", "continuous_entries_not_bit_identical"]
lock = {k: sum(x[k] for x in L) for k in keys_sum}
lock.update({
    "runs": [{"tag": x["tag"], "designer_seed": x["designer_seed"], "members": x["members"],
              "ticks_after_burnin": x["ticks_after_burnin"]} for x in L],
    "members": sum(x["members"] for x in L), "world_seed": 0,
    "obs_equality_rate": 1 - lock["obs_coords_differing"] / max(lock["obs_coords_compared"], 1),
    "jax_overflow_ticks_raw": sum(sum(x["jax_overflow_final"]["raw_overflow_ticks"]) for x in L),
    "jax_overflow_ticks_kept": sum(sum(x["jax_overflow_final"]["kept_overflow_ticks"]) for x in L),
    "jax_peak_raw_components": max(max(x["jax_overflow_final"]["raw_peak"]) for x in L),
    "jax_peak_kept_components": max(max(x["jax_overflow_final"]["kept_peak"]) for x in L),
    "max_abs_diff": {f: max(x["max_abs_diff"][f] for x in L) for f in L[0]["max_abs_diff"]},
    "max_rel_diff": {f: max(x["max_rel_diff"][f] for x in L) for f in L[0]["max_rel_diff"]},
    "max_abs_diff_all": max(x["max_abs_diff_all"] for x in L),
    "max_rel_diff_all": max(x["max_rel_diff_all"] for x in L),
    "min_blur_threshold_margin": min(x["min_blur_threshold_margin"] for x in L),
    "min_mass_mmin_margin": min(x["min_mass_mmin_margin"] for x in L),
    "events_sum_over_members": {k: sum(x["events_final_sum_over_members"][k] for x in L)
                                for k in L[0]["events_final_sum_over_members"]},
}) if L else None
ns = load("lockstep_nosimd.json")
out = {
    "what": "vw.objects.BlobTracker (pure JAX) vs the VW-0 host tracker integrate/lenia_world.Tracker, A_gliders",
    "tests_before": tests("tests_before.log"), "tests_after": tests("tests_after.log"),
    "lockstep": lock,
    "lockstep_numpy_avx512_disabled": None if ns is None else {
        k: ns[k] for k in ("designer_seed", "members", "ticks_after_burnin", "numpy_disabled_cpu_features",
                           "slot_map_entries_differing", "discrete_slot_entries_differing", "globals_entries_differing",
                           "obs_coords_differing", "continuous_entries_compared", "continuous_entries_not_bit_identical",
                           "max_abs_diff_all")},
    "replay_hero": load("replay_hero.json"),
    "replay_closure_jax_B18": load("replay_closure_B18.json"),
    "replay_closure_host_B18_control": load("replay_closure_host_B18.json"),
    "level0_context": load("level0_context.json"),
    "speed": load("speed.json"),
    "default_tracker": "host",
    "default_reason": ("lockstep and hero replay pass; the closure replay (B=18 designer ensemble) does not, "
                       "because level 0 differs, not the tracker: with the JAX tracker XLA hoists the Flow-Lenia "
                       "kernel construction out of the member loop of the init + burn-in program (as it does in "
                       "every B=1 program), the kernel rounds differently, x differs by 7e-10 after 3 burn-in "
                       "ticks and chaos amplifies it. Under 'jax' a member's level 0 is the same for B=1,2,3 "
                       "(= the agent path); under 'host' B=1 differs from B>=2. 'jax' as default would change "
                       "saved B>=2 ensembles, so 'host' stays the default and the reference."),
}
for k in ("replay_closure_jax_B18", "replay_closure_host_B18_control"):
    if out[k]:
        for kk in ("coarse_max_abs_diff_by_tick", "objects_max_abs_diff_by_tick"):
            v = out[k].pop(kk, None)
            if v:
                out[k][kk.replace("_by_tick", "_ticks_0_10_50")] = [v[0], v[10], v[50]]
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
