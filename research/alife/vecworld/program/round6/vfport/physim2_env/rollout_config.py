"""The rollout config: a FLAT file that says which model sits which exam under which limits, and nothing else.

    schema = "physim2-rollout/v1"
    model = "qwen/qwen3.6-35b-a3b"
    exam_profile = "ring"
    instance = "pilot-example-001"
    max_turns = 150
    max_output_tokens_per_turn = 8192
    max_context_tokens = 200000
    wall_minutes = 60
    box_memory_gb = 4
    cap_usd = 5.0
    reasoning_effort = "default"
    push = false

Top-level keys only: no table, no array, no path, nothing executable. `validate` refuses every unknown key,
wrong type and value out of range; `expand` turns a valid flat config into the vf-eval config of the profile.
Everything a flat config does not hold is fixed here for every model rollout: the env, the taskset, the image
of the profile, the stock `bash` harness without search, compaction or environment passthrough, the docker
runtime, one rollout, no retries, no upload.

The limits an agent can meet are all in the flat file, and all of them are told to the agent in its task
statement (physim2_env/bundle.py renders them from the run's resolved config): turns, wall time, tokens per
reply, the context limit and the spend cap. No other cap is set on a run (verifiers' own total-token caps stay
unset), so that no undisclosed limit can end it.

Standard library only: a tool can call this before verifiers, numpy or the package are imported.
"""
import re
import tomllib

from . import profiles

SCHEMA = "physim2-rollout/v1"
EFFORTS = ("default", "none", "minimal", "low", "medium", "high", "xhigh", "max")
MODEL = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}/[A-Za-z0-9][A-Za-z0-9._:-]{0,95}$")
INSTANCE = re.compile(r"^pilot-[a-z0-9-]{3,40}$")

# key -> (python types, None | (low, high) | tuple of allowed values | compiled pattern, required for a model run)
FLAT_KEYS = {
    "schema": ((str,), (SCHEMA,), True),
    "model": ((str,), MODEL, False),
    "exam_profile": ((str,), tuple(sorted(profiles.PROFILES)), False),
    "instance": ((str,), INSTANCE, True),
    "max_turns": ((int,), (1, 400), False),
    "max_output_tokens_per_turn": ((int,), (256, 32768), False),
    "max_context_tokens": ((int,), (8192, 2_000_000), True),
    "wall_minutes": ((int,), (5, 180), False),
    "box_memory_gb": ((int, float), (1, 4), False),
    "cap_usd": ((int, float), (0.01, 500), True),
    "reasoning_effort": ((str,), EFFORTS, False),
    "push": ((bool,), (False,), False),
}
RANGES = {k: v[1] for k, v in FLAT_KEYS.items() if isinstance(v[1], tuple) and len(v[1]) == 2 and not isinstance(v[1][0], (str, bool))}
REQUIRED = tuple(k for k, v in FLAT_KEYS.items() if v[2])
DEFAULT_MODEL = "qwen/qwen3.6-35b-a3b"
DEFAULT_PROFILE = "ring"
ENV_ID = "physim2-verifier"                                  # physim2_verifier: the stock isolated grader + ruling E1 for failed runs
HARNESS = {"id": "bash", "edit": True, "search": False}      # verifiers' stock harness; its program is preinstalled in the image


def defaults(profile: str = DEFAULT_PROFILE) -> dict:
    """What a flat config gets for the keys it leaves out (the required keys have no default)."""
    p = profiles.get(profile)
    return {"model": DEFAULT_MODEL, "exam_profile": profile, "max_turns": p["max_turns"],
            "max_output_tokens_per_turn": p["max_output_tokens_per_turn"], "wall_minutes": p["wall_minutes"],
            "box_memory_gb": p["box_memory_gb"], "reasoning_effort": "default", "push": False}


DEFAULTS = defaults()


def validate(cfg) -> list[str]:
    """Every violation of the schema, as one line each; an empty list means the config passes."""
    if not isinstance(cfg, dict):
        return ["the config is not a table of top-level keys"]
    bad = []
    for k in sorted(cfg):
        if k not in FLAT_KEYS:
            bad.append(f"unknown key {str(k)[:40]!r}")
            continue
        types, allowed, _ = FLAT_KEYS[k]
        v = cfg[k]
        if isinstance(v, bool) and bool not in types or not isinstance(v, types):
            bad.append(f"{k}: must be {' or '.join(t.__name__ for t in types)}")
            continue
        if isinstance(allowed, re.Pattern):
            if not allowed.fullmatch(v):
                bad.append(f"{k}: does not match {allowed.pattern}")
        elif k in RANGES:
            lo, hi = allowed
            if not (v == v and lo <= v <= hi):
                bad.append(f"{k}: must be from {lo} to {hi}")
        elif v not in allowed:
            bad.append(f"{k}: must be one of {', '.join(repr(a) for a in allowed)}")
    for k in REQUIRED:
        if k not in cfg:
            bad.append(f"{k}: required")
    if not bad:                                              # the memory cap of a profile can be lowered, never raised
        p = profiles.get(cfg.get("exam_profile", DEFAULT_PROFILE))
        if cfg.get("box_memory_gb", p["box_memory_gb"]) > p["box_memory_gb"]:
            bad.append(f"box_memory_gb: at most {p['box_memory_gb']} for profile {cfg.get('exam_profile', DEFAULT_PROFILE)}")
    return bad


def is_flat(cfg) -> bool:
    """Does this parsed TOML claim to be a rollout config (as opposed to a vf-eval config of the scripted tools)?"""
    return isinstance(cfg, dict) and cfg.get("schema") == SCHEMA


def load(path: str) -> dict:
    """Read and validate a flat config; the result holds every key (defaults filled in). ValueError lists every
    violation. Reads the one file and nothing else."""
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    bad = validate(cfg)
    if bad:
        raise ValueError("rollout config refused: " + "; ".join(bad))
    return dict(defaults(cfg.get("exam_profile", DEFAULT_PROFILE)), **cfg)


def expand(flat: dict) -> dict:
    """The vf-eval config of a validated flat config (a plain dict for tomli_w). It holds no path and no store:
    the caller (tools/vfrun.py) adds the run name, the output folder and the store as it does for every run."""
    bad = validate(flat)
    if bad:
        raise ValueError("rollout config refused: " + "; ".join(bad))
    c = dict(defaults(flat.get("exam_profile", DEFAULT_PROFILE)), **flat)
    p = profiles.get(c["exam_profile"])
    sampling = {"max_tokens": int(c["max_output_tokens_per_turn"])}
    # Reasoning (rulings E10, E14). "default" sends nothing: the provider's default applies. An effort goes out as
    # `reasoning_effort`, the field verifiers' sampling config has. There is no key for reasoning summaries: the
    # route's `reasoning` object ({"summary": ...}) was refused by the route for the default model at the first
    # call of the round-4 rehearsal (HTTP 400, 11 Nov 2026), so the key was removed (results/rehearsal_round4.json).
    if c["reasoning_effort"] != "default":
        sampling["reasoning_effort"] = c["reasoning_effort"]
    return {
        "model": c["model"], "num_rollouts": 1, "max_concurrent": 1, "push": False,
        "sampling": sampling,
        "env": {
            "id": ENV_ID,
            "taskset": {"id": "physim2-env", "image": p["image"], "instances": [c["instance"]],
                        "task": {"limits": {"max_context_tokens": int(c["max_context_tokens"]), "cap_usd": float(c["cap_usd"]),
                                            "box_cpus": float(p["box_cpus"]), "box_memory_gb": float(c["box_memory_gb"])}}},
            "agent": {"max_turns": int(c["max_turns"]),
                      "timeout": {"rollout": 60.0 * c["wall_minutes"]},
                      "runtime": {"type": "docker", "cpu": float(p["box_cpus"]), "memory": float(c["box_memory_gb"])},
                      "harness": dict(HARNESS),
                      "retries": {"max_retries": 0}},
            "retries": {"max_retries": 0},
            "verifier": {"retries": 0},
        },
    }


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(expand(load(sys.argv[1])), indent=1))
