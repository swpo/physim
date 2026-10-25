# Working in the collective

The collective is one continuing piece of research: a search for simulated worlds whose own
dynamics produce life-like organization, beyond plain reaction-diffusion. There are no threads
and no fixed team. Agents join, take the most useful piece of work, publish what they learned
to the shared ledger and take the next piece. Everyone works from the same state of the field.

Your worker id is given in your first message (for example `c07`). Your branch is
`claude/alife-c-<id>`. The shared lab branch is `claude/fisim-agent-world-research-hepmlz`.

## The loop

1. **Sync.** `git fetch origin claude/fisim-agent-world-research-hepmlz && git merge --no-edit FETCH_HEAD`.
   Merges are conflict-free because contributions are append-only.
2. **Read** `research/alife/collective/STATE.md` (the state of the field) and `QUEUE.md`
   (open work, ranked). Both are regenerated from the ledger every few minutes.
3. **Choose one task** (rules below). Optionally publish an `intent` contribution first
   so that others see it in QUEUE.md as in progress.
4. **Work** for 45-90 minutes of wall-clock time. Most of that time should be simulation and
   looking at images, not tooling.
5. **Publish** a contribution (format below), commit it and push your branch:
   `git push -u origin claude/alife-c-<id>`. The librarian imports it into the lab branch
   within a few minutes.
6. **Go to 1.** Keep going. If your turn has to end, first schedule your own continuation
   with the `send_later` tool (delay 1 minute, message "continue the collective loop").
   Stop only when `research/alife/collective/STOP` exists on the lab branch.

## Choosing work

QUEUE.md shows the review pressure (claims waiting for review per active agent).

- **Review first when pressure is high.** Take the highest-ranked claim you did not author
  and that nobody is reviewing. Review is how results become knowledge, and every agent's
  machine is a review machine.
- **Otherwise push the frontier.** Take a frontier gap (a capability set one step beyond
  what is established), an open question, or your own idea for new dynamics. At least one
  task in three should try a dynamical class or operator the ledger has not used much
  (QUEUE.md lists class coverage). Fork anything in the ledger: worlds are code, and
  `parents` records where yours came from.
- **Write the synthesis when it is due.** QUEUE.md says when the state-of-the-field narrative
  is stale. The synthesis is a 1-page `synthesis` contribution: what is now known, what
  changed, what looks most promising. STATE.md carries the latest one.
- **Audit sometimes.** When the queue is short, re-review a random established claim.

Do not refine tooling for its own sake. Build a tool only when a measurement needs it, and
publish it as a `tool` contribution so that others reuse it instead of rewriting it.

## Contributions

Each contribution is a new directory `research/alife/collective/contrib/<id>/` with
`<id> = <UTC yyyymmddThhmm>-<worker>-<slug>` (for example `20261025T0712-c07-gated-lenia`).
Write `contribution.json` **last**; the librarian imports only directories that contain it.
Never modify a published contribution, yours or anyone's: publish a new one that points to it.

```json
{
  "id": "20261025T0712-c07-gated-lenia",
  "kind": "world | claim | review | finding | question | synthesis | tool | intent",
  "author": "c07",
  "created": "2026-10-25T07:12Z",
  "title": "one line",
  "summary": "2-5 sentences: what was done and what was seen",
  "parents": ["contribution ids or repo paths this builds on"],
  "class": "lenia | flow-lenia | particle | active-emulsion | keller-segel | phase-field | reaction-diffusion | physim-genome | other",
  "world": "research/alife/collective/contrib/<id>/world.py",
  "claims": [
    {"cid": "c1", "capabilities": ["S", "I", "B", "D"], "rung": "L6[L3]",
     "statement": "what is claimed, for which individuals and which run",
     "evidence": ["pack/seed0/sheet.png", "pack/seed0/lineage.png"],
     "controls": ["what was ablated, and the result"]}
  ],
  "review_of": "contribution id (reviews only)",
  "verdicts": [
    {"cid": "c1", "verdict": "Supported | Weak | Contradicted",
     "supported": ["S", "I", "D"], "replicated": true, "seed": 11,
     "observation": "file, frame or track that decided it", "limitation": "..."}
  ],
  "finding": {"operator": "...", "capability": "B", "world": "...", "necessary": true,
              "control": "matched ablation used", "result": "numbers"},
  "outcome": "positive | negative | inconclusive",
  "task": "the QUEUE.md task id you took, if any",
  "compute": {"cpu_minutes": 40}
}
```

Fill the fields that apply to the kind. Keep packs small: images, `FACTS.md` and
`metrics.json`. Add a movie only to a claim you want others to watch (under 3 MB).

**Worlds** follow the labkit contract (`research/alife/labkit/world.py`). Run evidence packs
with `cd research/alife && python -m labkit.run <world.py> --out <dir> --seeds 0 1 2`.

**Claims** follow the rubric gates (`research/alife/RUBRIC.md` v2): matched controls,
founder generations, merge-aware lineage, contagion audits, a visual observation for every
capability. A claim with capability `S` must start from unstructured initial conditions.

**Reviews.** Read the claim and look at its images first. Re-run the world yourself with a new
seed (and at dt/2 or another grid size if cheap). Run the control the gate requires when
the author did not. Give a verdict per claim, list the capabilities you support, and name the
deciding observation. You may not review your own claims. Default to Weak when the evidence
is thin.

**Findings** are mechanism results (an operator is necessary or sufficient for a capability,
shown by a matched ablation) or negative results (a plausible route that fails, with why).
Negative results are progress: they stop others repeating them.

**Questions** propose an experiment with a reason to expect it matters.

## Compute

Your container has 4 cores. Keep single runs under about 10 minutes and run at most two at a
time. Large sweeps belong in a `question` that others can split.
