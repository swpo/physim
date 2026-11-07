# Lab-world rollout kit (PhySim)

Nine frozen PhySim lab bundles and their rollout configs, for running the first lab-world rollouts from a machine
whose Prime login can create sandboxes. Built in the cloud research session (2 Nov 2026); every bundle was graded end
to end there without credits (a naive predictor scores about 0; the true simulator scores 0.38-0.71, rods 0.17-0.21).

| bundle | world | suite | cases |
|---|---|---|---|
| fedvortex | c53 fed vortices | original fed-vortex suite | 15 |
| vortex_main, vortex_formation | c53 fed vortices with heredity | capability suite; formation from noise | 13; 3 |
| pm_main, pm_formation | phase-membrane protocells | capability suite (refrozen); formation | 15; 8 |
| cips_main, cips_formation | CIPS cells, isotropic stencil | capability suite with moat (refrozen); formation | 12; 4 |
| rods_main, rods_formation | Marangoni rods | capability suite (refrozen); formation | 16; 3 |

Bundle ids are in `bundle_ids.json`. Each config sets the predictor limits from the measured cost of running the true
simulator (4 CPUs, 3x the faithful predictor's CPU time), a 24 h agent timeout, and a scoring timeout derived from
the suite. `mech_fedvortex.prime-agent.toml` is a capped mechanics test (45 min agent, 5000 tu, 150 s predictor wall).

## 1. Environment

The bundles bind the exact PhySim sources and numpy/scipy versions, so run from swpo/residency-environments branch
`fix/physim-fair-energy-labworlds` (19f30c1 or later with the same pinned sources: the PR #40 branch `labworlds-adapter`
plus the ruff-format commit and the fair scorer; `labworlds-adapter` alone still has the old scorer and is refused),
with the environment's pinned numpy 2.5.2 and scipy 1.18.0:

    cd residency-environments/environments/physim && uv sync
    uv run python /path/to/rollout_kit/check_kit.py     # must print "ok" for all nine
    python /path/to/rollout_kit/localize.py             # writes configs_local/ with absolute bundle paths

`check_kit.py` names the source file or library version that differs if a bundle refuses to open.

## 2. Mechanics test (small model; cents of inference)

    export OMP_NUM_THREADS=1   # the laboratory simulates each experiment on this machine, single-threaded
    uv run vf-eval @ $KIT/configs_local/mech_fedvortex.prime-agent.toml --model qwen/qwen3.5-9b \
      --sampling.max-tokens 32768 --env.agent.harness.context-window 65536 \
      --env.agent.harness.compaction.reserve-tokens 36864 --env.agent.harness.compaction.keep-recent-tokens 12000 \
      --output-dir $RUNS --run.dir mech-fedvortex-qwen9b

Pass: the rollout reaches the agent's turns (stop condition not `sandbox_error`), experiments are charged, the
predictor sandboxes (4 CPU, 2 GiB, long wall) start, and grading writes a reward.

## 3. Pilot (GPT-6 Astra and GPT-6.1 Sol, Codex harness, one rollout each)

Stage A, fed vortices, both models (can run concurrently):

    for M in openai/gpt-6-astra openai/gpt-6.1-sol; do
      uv run vf-eval @ $KIT/configs_local/fedvortex.codex.toml --model $M \
        --output-dir $RUNS --run.dir pilot-fedvortex-${M##*/} &
    done; wait

Stage B, after stage A looks sane: the same for `vortex_main`, `pm_main` and `cips_main`
(`$KIT/configs_local/<bundle>.codex.toml`). Rods and the formation suites come later.

Prices on Prime Inference (per million tokens): Astra $10 in / $50 out, Sol $2 / $10, Qwen3.5 9B about $0.02.
In the October BF case study Astra cost $23 and Sol $7.60 per rollout; expect the same order here.
Grading runs the predictor once per case in a fresh 4-CPU sandbox, so a rollout's grading can take hours.

## 4. Results

Each run directory holds `traces.jsonl` (reward, grade, limit audit) and the agent's artifacts under
`outputs/r6/artifacts`. Keep the run directories; the cloud session will read the traces for the write-up.

## Re-sealed for the fair scorer (8 Nov 2026)

The bundles now pin the fair (unbiased) ensemble estimator for the energy score and CRPS:
`blobround6_eval.py` 9deb1738, plus the ruff-formatted `labworld.py` 501fffd3 and `labbundle.py` 060e39ae, with
`blobround6` d1b4a8b4, `devices` 43229b50, numpy 2.5.2 and scipy 1.18.0. That is
swpo/residency-environments branch `physim-fair-energy-labworlds` at ef1f58c. Only `manifest.json` and the ids
changed: every data and truth file is byte-identical, member 0 of one truth per bundle re-simulates bit for bit, and
the fed-vortex reference demo reproduces `checks.json` exactly. The bundles are refused by a PhySim environment
whose scorer is the old plugin estimator (`blobround6_eval` 3d8e3fb3); the previous ids are in git history.
