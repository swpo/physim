"""check_config -- the STRICT SCHEMA of a rollout config, checked before anything is started.

    python -B tools/check_config.py --config research/alife/vecworld/program/round6/rollouts/configs/NAME.toml

A new rollout config needs no new review of the pin, and that is only safe because of what this tool refuses.
A config passes only if ALL of this holds:

  where      the file is `round6/rollouts/configs/<name>.toml` (given from the repository root, from the study
             folder or absolute), directly in that folder, a regular file, not a link, at most 16 KiB of UTF-8,
             with a name of lower-case letters, digits and `. _ -`
  flat       top-level keys only, each a string, an integer, a number or a boolean: no table, no array, no date
  known      every key is one of physim2_env/rollout_config.py's FLAT_KEYS, with its type and range (that file
             is the schema; `python -B tools/check_config.py --schema` prints it as JSON for the runner)
  fixed      what the config expands to is the pin's model rollout and nothing else: the env of the pin, the
             taskset `physim2-env` with the image of the profile, the pin's preinstalled `bash` harness with
             exactly its pinned options, the docker runtime with nothing but `cpu` and `memory`, one rollout, no
             retries, `push = false`
  absent     nowhere in the expansion: a tool, a url, a network rule, a mount, an environment passthrough, an
             image other than the profile's, a command, a script, a path, a client or a store

The tool reads the one file and nothing else, starts nothing and writes nothing. On success it prints one JSON
line (the config's sha256, the flat values with defaults, what the pin fixes) and exits 0; otherwise it prints
`refused: ...` with every violation and exits 2.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONFIG_DIR = os.path.normpath(os.path.join(ROOT, "..", "rollouts", "configs"))
REPO_PREFIX = "research/alife/vecworld/program/round6/rollouts/configs/"
NAME = re.compile(r"^[a-z0-9][a-z0-9._-]{0,79}\.toml$")
MAX_BYTES = 16 << 10
# Keys that may appear NOWHERE in what a config expands to (rollout_config.expand): each would let a config
# reach beyond the pin. `image` and `harness` are checked by value below.
FORBIDDEN = {"tools", "toolsets", "url", "colocated", "network", "network_allow", "allow", "block", "mounts", "mount", "volumes",
             "volume", "env", "forward_env", "box_env_allow", "command", "entrypoint", "script", "agent_dir", "args", "python",
             "collect", "collect_dir", "collect_tree", "system_prompt", "client", "base_url", "api_key_var", "headers", "store",
             "index", "output_dir", "endpoints", "skills", "gpu", "disk", "workdir", "judges", "extra_body", "compaction"}


class Refused(Exception):
    pass


def light(name: str):
    """A module of physim2_env loaded BY PATH, without importing the package (whose first lines import verifiers).
    For the modules that are standard library only: rollout_config, profiles, boxcaps."""
    import importlib.util
    import types
    pkg = sys.modules.get("_physim2_light")
    if pkg is None:
        pkg = types.ModuleType("_physim2_light")
        pkg.__path__ = [os.path.join(ROOT, "physim2_env")]
        sys.modules["_physim2_light"] = pkg
    full = f"_physim2_light.{name}"
    if full in sys.modules:
        return sys.modules[full]
    spec = importlib.util.spec_from_file_location(full, os.path.join(ROOT, "physim2_env", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[full] = mod
    spec.loader.exec_module(mod)
    return mod


def locate(path: str) -> str:
    """The absolute path of a config named from the repository root, from the study folder, or absolutely; raises
    Refused unless it is a plain file directly in round6/rollouts/configs/."""
    if not isinstance(path, str) or not path or "\x00" in path or len(path) > 512:
        raise Refused("the config path is not a path")
    if path.startswith(REPO_PREFIX):
        full = os.path.join(CONFIG_DIR, path[len(REPO_PREFIX):])
    elif os.path.isabs(path):
        full = path
    else:
        full = os.path.join(ROOT, path)
    full = os.path.normpath(full)
    if os.path.dirname(full) != CONFIG_DIR or not NAME.match(os.path.basename(full)):
        raise Refused("the config is not a file `<name>.toml` directly in round6/rollouts/configs/ (lower-case letters, digits, `. _ -`)")
    try:
        if os.path.realpath(CONFIG_DIR) != os.path.realpath(os.path.dirname(full)) or os.path.islink(CONFIG_DIR):
            raise Refused("round6/rollouts/configs/ is not a plain folder")
        st = os.lstat(full)
    except OSError:
        raise Refused("the config file does not exist") from None
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
        raise Refused("the config is not a regular file of its own (a link, a folder or something else)")
    if st.st_size > MAX_BYTES:
        raise Refused(f"the config is larger than {MAX_BYTES} bytes")
    return full


def walk_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.{k}" if path else str(k), str(k)
            yield from walk_keys(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_keys(v, path + "[]")


def fixed_violations(expanded: dict, flat: dict, RC, PROFILES) -> list[str]:
    """Why an expanded config is NOT the pin's model rollout (empty = it is). Independent of how expand() is
    written: the expansion is compared with what the pin says a model rollout is."""
    bad = []
    p = PROFILES.get(flat["exam_profile"])
    env = expanded.get("env") or {}
    agent, taskset = env.get("agent") or {}, env.get("taskset") or {}
    want_top = {"model": flat["model"], "num_rollouts": 1, "max_concurrent": 1, "push": False}
    for k, v in want_top.items():
        if expanded.get(k) != v or type(expanded.get(k)) is not type(v):
            bad.append(f"{k} is not {v!r}")
    if set(expanded) - {"model", "num_rollouts", "max_concurrent", "push", "sampling", "env"}:
        bad.append("unexpected top-level tables: " + ", ".join(sorted(set(expanded) - {"model", "num_rollouts", "max_concurrent", "push", "sampling", "env"})))
    sampling = dict(expanded.get("sampling") or {})
    if sampling.pop("max_tokens", None) != flat["max_output_tokens_per_turn"]:
        bad.append("sampling.max_tokens is not the config's max_output_tokens_per_turn")
    # reasoning (rulings E10, E14): nothing for "default"; an effort alone as `reasoning_effort`; a summary request as
    # the route's `reasoning` object, with the effort inside it and never twice
    want = {}
    if flat["reasoning_summary"] != "default":
        want["reasoning"] = {"summary": flat["reasoning_summary"]}
        if flat["reasoning_effort"] != "default":
            want["reasoning"]["effort"] = flat["reasoning_effort"]
    elif flat["reasoning_effort"] != "default":
        want["reasoning_effort"] = flat["reasoning_effort"]
    if sampling != want:
        bad.append("sampling holds more than max_tokens and the config's reasoning settings")
    if env.get("id") != RC.ENV_ID or set(env) - {"id", "taskset", "agent", "retries", "verifier"}:
        bad.append("the env is not the pin's")
    if agent.get("harness") != RC.HARNESS:
        bad.append("the harness is not the pin's preinstalled bash harness with its pinned options")
    runtime = agent.get("runtime") or {}
    if runtime.get("type") != "docker" or set(runtime) - {"type", "cpu", "memory"} or runtime.get("memory") != flat["box_memory_gb"] \
            or runtime.get("cpu") != p["box_cpus"]:
        bad.append("the runtime is not docker with the profile's CPUs and the config's memory, and nothing else")
    if agent.get("max_turns") != flat["max_turns"] or (agent.get("timeout") or {}) != {"rollout": 60.0 * flat["wall_minutes"]}:
        bad.append("max_turns or the wall time is not the config's")
    if set(agent) - {"max_turns", "timeout", "runtime", "harness", "retries"}:
        bad.append("the agent table holds more than turns, time, runtime, harness and retries")
    if (agent.get("retries") or {}) != {"max_retries": 0} or (env.get("retries") or {}) != {"max_retries": 0} or (env.get("verifier") or {}) != {"retries": 0}:
        bad.append("a retry is allowed somewhere")
    if taskset.get("id") != "physim2-env" or taskset.get("image") != p["image"] or taskset.get("instances") != [flat["instance"]] \
            or set(taskset) - {"id", "image", "instances", "task"}:
        bad.append("the taskset is not physim2-env with the profile's image and the config's one instance")
    task = taskset.get("task") or {}
    limits = task.get("limits") or {}
    if set(task) - {"limits"} or limits.get("cap_usd") != flat["cap_usd"] or limits.get("max_context_tokens") != flat["max_context_tokens"] \
            or set(limits) - {"cap_usd", "max_context_tokens", "box_cpus", "box_memory_gb"}:
        bad.append("the task table holds more than the limits of the config")
    # (the top-level table `env` is vf-eval's environment table; an `env` anywhere below it is a passthrough)
    hit = sorted({path for path, key in walk_keys(expanded) if key in FORBIDDEN and path != "env"})
    if hit:
        bad.append("forbidden fields: " + ", ".join(hit[:8]))
    return bad


def check(path: str) -> dict:
    """Everything above for one config. Returns {"path", "name", "sha256", "bytes", "flat", "expanded"}; raises
    Refused with every violation in one message."""
    RC, PROFILES = light("rollout_config"), light("profiles")
    full = locate(path)
    with open(full, "rb") as f:
        raw = f.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES or b"\x00" in raw:
        raise Refused("the config is too large or holds a NUL byte")
    try:
        cfg = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as e:
        raise Refused(f"the config is not UTF-8 TOML ({type(e).__name__})") from None
    nested = sorted(str(k)[:40] for k, v in cfg.items() if isinstance(v, bool) is False and not isinstance(v, (str, int, float)))
    if nested:
        raise Refused("the config is not flat: " + ", ".join(nested[:8]) + " is a table, an array or a date")
    bad = RC.validate(cfg)
    if bad:
        raise Refused("; ".join(bad))
    flat = dict(RC.defaults(cfg.get("exam_profile", RC.DEFAULT_PROFILE)), **cfg)
    expanded = RC.expand(cfg)
    bad = fixed_violations(expanded, flat, RC, PROFILES)
    if bad:
        raise Refused("the config does not expand to the pin's model rollout: " + "; ".join(bad))
    return {"path": full, "name": os.path.basename(full), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "flat": flat, "expanded": expanded}


def schema() -> dict:
    """The schema as data, for the runner's mechanical check and for the runbook's table."""
    RC, PROFILES = light("rollout_config"), light("profiles")
    keys = {}
    for k, (types, allowed, required) in RC.FLAT_KEYS.items():
        row = {"type": " or ".join(t.__name__ for t in types), "required": bool(required), "default": RC.DEFAULTS.get(k)}
        if isinstance(allowed, re.Pattern):
            row["pattern"] = allowed.pattern
        elif k in RC.RANGES:
            row["range"] = list(allowed)
        else:
            row["one_of"] = list(allowed)
        keys[k] = row
    return {"schema": RC.SCHEMA, "config_folder": REPO_PREFIX, "file_name": NAME.pattern, "max_bytes": MAX_BYTES, "keys": keys,
            "fixed_by_the_pin": {"env": RC.ENV_ID, "taskset": "physim2-env", "harness": RC.HARNESS, "runtime": "docker",
                                 "num_rollouts": 1, "max_concurrent": 1, "retries": 0, "push": False},
            "forbidden_fields": sorted(FORBIDDEN), "exam_profiles": PROFILES.table()}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="the strict schema of a rollout config")
    ap.add_argument("--config", help="round6/rollouts/configs/<name>.toml")
    ap.add_argument("--schema", action="store_true", help="print the schema, the exam profiles and their item counts as JSON")
    a = ap.parse_args(argv)
    if a.schema:
        print(json.dumps(schema(), indent=1))
        return 0
    if not a.config:
        ap.error("--config or --schema")
    try:
        got = check(a.config)
    except Refused as e:
        print("refused: " + str(e))
        return 2
    print(json.dumps({"config": got["name"], "sha256": got["sha256"], "flat": got["flat"],
                      "fixed_by_the_pin": schema()["fixed_by_the_pin"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
