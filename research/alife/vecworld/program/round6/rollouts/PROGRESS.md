# First model rollouts of round 6: progress

PILOT_NEVER_REUSE_AS_EXAM: every instance named here is public pilot material and is never to be used as an exam.

The exam is the verifiers port of round 6 (`../vfport`, pinned by `PIN.sha256` at commit
08bd5a669867623a476e7446a74612be47001b3b; nothing under it is changed by this work). Configs, wrappers and
results of the rollouts are in this folder. Spend: `LEDGER.md`.

## qwen_ring_001 (the mechanics rollout; runner session of 11 Nov 2026, in the cloud container)

Purpose: prove that a real model can take the exam end to end here (key, model route, harness, laboratory,
submission, grading) and see what a weak agent does. One rollout; at most one more, on a new instance, if the
first dies on mechanics.

State (newest last; times UTC as this container's clock shows them):

- 10:30 Runner started after a container restart (the earlier runner's work did not survive; nothing was
  committed). Own worktree; the port's tree equals the pin (109 of 109 hashes; sha256 of PIN.sha256 cd67eb4b...).
- 10:35 Docker daemon started (29.9.2). Images on disk: physim2-ring:1, localhost/verifiers-network:1,
  python:3.12-slim. No container of anybody was running.
- 10:40 Model: `qwen/qwen3.5-35b-a3b` (the pinned config's id) is not in Prime's model list (132 models);
  `qwen/qwen3.6-35b-a3b` is, with tools, at $0.11 in / $1.01 out / $0.099 cache read per million tokens (the
  list's own `pricing` field). It is the cheapest Qwen chat model by input price. Bound by the caps: $0.23 plus
  one request.
- 10:42 MECHANICS, found before any rollout, both from this machine's TLS-intercepting proxy (neither applies to
  the lead's Mac):
  1. vf-eval cannot reach the model from the environment `tools/vfrun.py` gives it. The allow-list (ENV_PASS,
     tools/vfrun.py line 62) drops SSL_CERT_FILE; verifiers' model client (httpx) then checks against certifi:
     measured `CERTIFICATE_VERIFY_FAILED` for `GET /api/v1/models` from an environment of PATH, HOME, LANG, and
     200 with the session's environment. Worked around outside the pinned tree: `tools/here.py` adds the one
     name SSL_CERT_FILE to vfrun.ENV_PASS in memory for the model command only.
  2. The stock `bash` harness installs itself INSIDE the agent's box before the network is cut (`pip install
     uv`, `uv sync --script`: verifiers runtimes/base.py:41-46, 274-279). In `physim2-ring:1` that fails here
     (measured in a throwaway container: curl exit 60, `uv: not found`, status 127 after 16 s), because the box
     does not trust the proxy's CA. Worked around outside the pinned tree: image `physim2-ring-ca:1` =
     `physim2-ring:1` + the machine's CA bundle + four variables (`docker/Dockerfile.ring-ca`); the same
     bootstrap then ends with status 0 in 4 s and the chat program starts (`--help`).
  The session's environment also holds two names the tools refuse (UV_NATIVE_TLS, DOCKER_HTTPS_PROXY):
  `tools/here.py` starts every tool from PATH, HOME, USER, LANG and VF_RUN_ID only, as the cloud rehearsals did.
- 10:44 Instance `pilot-qwen-ring-001-r2-w0` made (ring, smoke_ring: 64 items, R = 16, 400 laboratory ticks),
  commitment a125f5016080ec142c86391721dd52bfccad569b6332e88e3c53a9db1b685852. Store (hidden side, never
  committed): the runner's scratch folder `rollq/store`. Reference table started: `tools/prove.py`, policies
  S, D, P0, PM, C, null, C once more with one box per item; disk floor 1.5 GiB (3.0 GiB free on this machine).

Next: the reference table's result; the free dry run; commit; the rollout (run label physim2-rollq-20261111,
run name qwen-ring-001); extraction into `qwen_ring_001/`.

If this session is cut during the rollout: the rollout is recorded as cut with what was spent (the provider's
usage as far as the trace has it), and the instance is not reused.
