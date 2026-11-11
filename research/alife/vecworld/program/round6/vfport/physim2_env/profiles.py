"""Exam profiles: what a rollout config may name as `exam_profile`, and everything that follows from the name.

A profile fixes the world, the exam config (agentenv/configs/<config_name>.json: items, replicate truths,
laboratory budget, per-item predictor limits), the image of every box, the box's CPU and memory caps, the
default turn and wall-time limits, and the scripted policies of the reference table. A rollout config
(physim2_env/rollout_config.py) names a profile and may lower the memory cap; it cannot name a world, an exam
config or an image.

Standard library only: tools read this before anything heavy is imported.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PROFILES = {
    "ring": {
        "world": "ring",
        "config_name": "smoke_ring",
        "image": "physim2-ring:2",
        "box_cpus": 2,                                       # docker --cpus of every box (agent, verifier, item boxes)
        "box_memory_gb": 4,                                  # docker --memory; a rollout config may lower it, never raise it
        "max_turns": 150,
        "wall_minutes": 60,
        "max_output_tokens_per_turn": 8192,
        # the scripted policies of the reference table, in the order tools/prove.py runs them
        # (K and O need no rollout: they come from the frozen exam itself)
        "reference_policies": ["null", "D", "P0", "PM", "S", "C"],
        "reference_sizes": {"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512},
    },
}
# What a box gets when the exam is not one of the profiles above (development configs such as probe_ring):
# the same caps as the ring profile, and the wall time of the exam config's own envelope.
FALLBACK_BOX = {"box_cpus": 2, "box_memory_gb": 4}

BASELINE_EPISODES = 512                                      # size of the null policy's pool (bundle.null_pool)


def get(name: str) -> dict:
    if name not in PROFILES:
        raise ValueError(f"unknown exam profile {name!r}; this pin defines: {', '.join(sorted(PROFILES))}")
    return dict(PROFILES[name])


def for_exam(world: str, config_name: str) -> dict | None:
    """The profile that uses this world and exam config, or None."""
    for name, p in PROFILES.items():
        if p["world"] == world and p["config_name"] == config_name:
            return dict(p, name=name)
    return None


def exam_config(name: str) -> dict:
    """The raw exam config of a profile (public numbers only), read from agentenv/configs."""
    root = os.environ.get("PHYSIM2_AGENTENV") or os.path.join(HERE, "..", "..", "..", "round5", "agentenv")
    with open(os.path.join(os.path.abspath(root), "configs", get(name)["config_name"] + ".json")) as f:
        return json.load(f)


def items(name: str) -> int:
    """Number of exam items of a profile."""
    return int(exam_config(name)["exam"]["n_items"])


def table() -> list[dict]:
    """One row per profile, for the runbook and for the runner's mechanical check."""
    return [{"profile": n, "world": p["world"], "exam_config": p["config_name"], "items": items(n), "image": p["image"],
             "box_cpus": p["box_cpus"], "box_memory_gb": p["box_memory_gb"], "max_turns": p["max_turns"],
             "wall_minutes": p["wall_minutes"], "reference_policies": list(p["reference_policies"])}
            for n, p in sorted(PROFILES.items())]


if __name__ == "__main__":
    print(json.dumps(table(), indent=1))
