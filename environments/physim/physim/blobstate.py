"""physim.blobstate — BLOB rollout state (shared host/task/tool-server).

Kept dependency-light on purpose: physim.taskset imports this at module
scope (the Task generic needs the concrete State class), and importing
physim must NOT require blobkit/scipy/agentenv. Everything heavy lives in
physim.blobcore, imported lazily by the tool server and scoring."""

from __future__ import annotations

import verifiers.v1 as vf


class BlobToolState(vf.State):
    # identity (set host-side by BlobTask.setup)
    world: str = ""
    seed: int = 0
    # episode progress (evaluator-side coordinates; never surfaced by tools)
    i_ctrl: int = 0                    # main-line frame index (0..340)
    poses: list = []                   # [[y, x, dilation], ...] secret frame
    spent: dict = {}                   # sensor / motion / injection
    n_replicas: int = 0
    locked_p1p2: bool = False
    replica_log: list = []             # [{port, amp, dur, n_lags}]
    sub_p1: str = ""                   # submitted payloads (JSON)
    sub_p2: str = ""
    sub_p3: str = ""
    turns: int = 0
