# Rehearsal requests of round 4 (cloud container)

PILOT_NEVER_REUSE_AS_EXAM. These are the request files (schema `rollout-job/v1`) of the two model rollouts that the
integrator of port round 4 ran in the cloud container while rehearsing `RUNBOOK_MAC.md`, step 3. They live HERE and
not under `research/alife/vecworld/program/rollouts/requests/`, because the runner on the lead's Mac executes
every request that appears there. Step 3a's second command was therefore issued through `../fetch4.py`, which
runs the pinned `tools/check_request.py` with the one constant that says where requests live changed in memory
(`results/rehearsal_round4.json` holds the literal command). The configs they name are where the protocol puts
them: `round6/rollouts/configs/qwen_ring_002_cut.toml` and `qwen_ring_002.toml`.

Nobody runs these again: a job id, an instance name and a config name are each used once.

Second pass of round 4 (fixer, 11 Nov 2026): `qwen-ring-003.json`, one short job (30 turns, 15 minutes, $0.50) that
rehearses step 3 at the third round-4 pin (`841b4a1e1`); its config is `round6/rollouts/configs/qwen_ring_003.toml`.
