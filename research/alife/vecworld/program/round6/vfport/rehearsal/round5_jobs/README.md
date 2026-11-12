# Rehearsal requests of round 5 (cloud container)

PILOT_NEVER_REUSE_AS_EXAM. The request file (schema `rollout-job/v1`) of the one model rollout that the fixer of port
round 5 ran in the cloud container while rehearsing `RUNBOOK_MAC.md`, step 3, at the round-5 pin. It lives HERE and
not under `research/alife/vecworld/program/rollouts/requests/`, because the runner on the lead's Mac executes every
request that appears there; step 3a's second command was issued through `../fetch4.py` (the pinned
`tools/check_request.py` with the folder of requests changed in memory), as in round 4. The config it names is where
the protocol puts it: `round6/rollouts/configs/qwen_ring_004.toml`. Nobody runs it again: a job id, an instance name
and a config name are each used once.

Second pass (12 Nov 2026): `qwen-ring-005.json`, the one model rollout of the fixer's rehearsal of the second-pass
pin `19b6beb83` (40 turns, 15 minutes, $0.50; its config `round6/rollouts/configs/qwen_ring_005.toml`). The same
rules: never under `requests/`, used once, step 3a's second command through `../fetch4.py`.
