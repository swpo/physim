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
    sub_p1: str = ""                   # submitted payloads (JSON, round 1)
    sub_p2: str = ""
    sub_p3: str = ""
    round2: str = ""                   # menu name ("E1"/"E2") when round 2
    subs2: dict = {}                   # round-2 payloads: contract id -> JSON
    turns: int = 0
    # ---- round 5 (BLOB2v2, spec v2.1): two-phase closed-book episodes ----
    # All fields serializable (the state crosses the state channel per tool
    # call); live fork sims stay in server-process memory keyed by
    # (r5_nonce, fork id) and are rebuilt deterministically from the logged
    # ops on a cold registry (salted noise streams make replay exact).
    round5: str = ""                   # menu tag ("E1"/"E2") when v2
    r5_phase: str = ""                 # "" = exploration; "revealed" after
    #                                    probe_ready (irreversible)
    r5_nonce: str = ""                 # rollout nonce (fork stream salt)
    r5_ibase: int = 0                  # base read head (5tu grid, monotone)
    r5_poses_base: list = []           # base-context device poses
    r5_forks: dict = {}                # fork id -> record (src, poses,
    #                                    steps, emissions, log, open)
    r5_fork_seq: int = 0               # spawn counter (fork stream index)
    r5_meters: dict = {}               # silent meters: sensor, adjust,
    #                                    injection, sim_tu (never surfaced)
    r5_cap_hits: dict = {}             # meter -> refusal count (target 0)
    r5_open_peak: int = 0              # max concurrent open forks
    r5_n_resets: int = 0
    r5_reads_base: int = 0             # read steps served per context class
    r5_reads_fork: int = 0
    r5_t_ready_sim: float = -1.0       # sim_tu at probe_ready (-1 = never)
    r5_t_ready_turns: int = -1         # turns at probe_ready
    r5_subs: dict = {}                 # round-5 payloads: family -> JSON
