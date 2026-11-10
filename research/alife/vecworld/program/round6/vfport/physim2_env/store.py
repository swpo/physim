"""The instance store on the trusted worker: where a pointer on a task row becomes a hidden instance.

    <store>/index.json                       PUBLIC pointers: [{instance_id, world, config_name, secret_commitment}]
    <store>/<instance_id>/hidden/            instance.json (theta, secret), exam.npz (items, truths), examples.npz
    <store>/<instance_id>/hidden/labs/<rollout>/    the laboratory's records of one rollout (state, request log)
    <store>/<instance_id>/hidden/grades/<rollout>.npz|.json   per-item scores of one rollout

The store is a local directory here (PHYSIM2_STORE or --env.taskset.store). The sealer and the private Hugging
Face store are a separate study; they replace `hidden_dir` below and nothing else. A task row never carries a
path into the store, only the instance id and the public commitment of its secret.
"""
from __future__ import annotations

import json
import os
import re

ID = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,63}$")
TOKEN_LIKE = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|API_?KEY|ACCESS_?KEY|PRIVATE_?KEY)", re.I)
KEEP = {"VF_STATE_SECRET"}                                   # verifiers' own per-rollout state capability


def store_root(configured: str = "") -> str:
    root = configured or os.environ.get("PHYSIM2_STORE", "")
    if not root:
        raise RuntimeError("no instance store: set PHYSIM2_STORE or --env.taskset.store")
    return os.path.abspath(os.path.expanduser(root))


def hidden_dir(root: str, instance_id: str) -> str:
    if not ID.match(instance_id):
        raise ValueError("bad instance id")
    d = os.path.join(root, instance_id, "hidden")
    if not os.path.isfile(os.path.join(d, "instance.json")) or not os.path.isfile(os.path.join(d, "exam.npz")):
        raise RuntimeError(f"instance {instance_id!r} is not in the store")
    return d


def read_index(root: str, index: str = "") -> list[dict]:
    rows = json.load(open(index or os.path.join(root, "index.json")))
    for r in rows:
        if not ID.match(r["instance_id"]):
            raise ValueError("bad instance id in the index")
    return rows


def token_like(names) -> list[str]:
    return sorted(n for n in names if TOKEN_LIKE.search(n) and n not in KEEP)


def scrub_environment() -> list[str]:
    """Remove every token-like variable from THIS process: from os.environ and, on Linux, from the environment
    block the kernel shows in /proc/<pid>/environ (the bytes are overwritten in place). Returns the names."""
    names = token_like(os.environ)
    values = {n: os.environ[n] for n in names}
    for n in names:
        del os.environ[n]
    try:
        import ctypes
        with open("/proc/self/stat") as f:
            fields = f.read().rsplit(")", 1)[1].split()
        start, end = int(fields[47]), int(fields[48])        # env_start, env_end (fields 50 and 51 of proc(5))
        block = ctypes.string_at(start, end - start)
        for n, v in values.items():
            needle = (n + "=" + v).encode()
            i = block.find(needle)
            while i >= 0 and v:
                off = i + len(n) + 1
                ctypes.memset(start + off, ord("x"), len(v.encode()))
                i = block.find(needle, i + 1)
    except Exception:
        pass
    return names
