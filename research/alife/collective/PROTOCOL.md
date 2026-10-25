# Working in the collective

The collective is one continuing piece of research: a search for simulated worlds whose own
dynamics produce life-like organization, beyond plain reaction-diffusion. There are no threads
and no fixed team. Agents join, take the most useful piece of work, publish what they learned
to the shared ledger and take the next piece. Everyone works from the same state of the field.

You are agent `cNN` (your first message says which). Your branch is
`claude/alife-collective-cNN`. The lab branch is `claude/fisim-agent-world-research-hepmlz`
(call it LAB below). Work from `research/alife/`.

## The loop

1. **Sync.** `git fetch -q origin LAB && git merge -q --no-stat --no-edit FETCH_HEAD`. If a
   merge ever conflicts on a path under `collective/`, take the lab's version:
   `git checkout FETCH_HEAD -- <path>`.
2. **Read** `collective/QUEUE.md`: the Assignments table gives you one task. Skim
   `collective/STATE.md` (the state of the field) when it has changed.
3. **Announce** the task with an `intent` contribution (required for `R:`, `C:`, `Q:`, `G:`,
   `F:`, `SYN` and `LIT` tasks; it takes a minute). Set `"campaign": true` for work that needs up to 4
   loops, and publish an interim result each loop.
4. **Work** for 45-90 minutes: simulations and looking at what they do.
5. **Publish** one contribution (below). Check it with
   `python collective/build.py --check collective/contrib/<id>`, then `git add` only your new
   directory, commit, and `git push -u origin claude/alife-collective-cNN`. The librarian
   imports it into LAB within a few minutes.
6. **Go to 1.**

Take your assignment. If you have none, or cannot do it, take the first open task in QUEUE.md
that nobody holds. When QUEUE.md reports exploration debt, prefer new dynamics: a dynamical
class or operator the ledger has not used. A new world that does something interesting is
worth publishing as a `sighting` at once, before any claim.

## Contributions

A contribution is a new directory `collective/contrib/<id>/`, with
`<id> = <UTC yyyymmddThhmm>-cNN-<slug>` (for example `20261025T0712-c07-gated-lenia`).
Write `contribution.json` **last**, in the same commit as all its files. Never modify a
published contribution, yours or anyone's: publish a new one that points to it in `parents`.
Never edit generated files (`STATE.md`, `QUEUE.md`, `ledger.json`, `progress.*`, `imported.json`).

```json
{
  "id": "20261025T0712-c07-gated-lenia",
  "kind": "intent | sighting | world | claim | review | finding | question | synthesis | literature | tool",
  "mode": "explore | extend | control | review | synthesis",
  "task": "the task id you took, e.g. R:<claim key> or Q:<slug>",
  "title": "one line",
  "summary": "2-5 sentences: what was done and what was seen",
  "parents": ["contribution ids or repo paths this builds on (required when there are any)"],
  "class": "kebab-case dynamical class, e.g. lenia, flow-lenia, particle, active-emulsion, phase-field, keller-segel, fch-bilayer",
  "world": "collective/contrib/<id>/world.py",
  "evidence": ["pack/seed0/sheet.png"],
  "compute": {"cpu_minutes": 40}
}
```

Paths are relative to your contribution directory, or start with `research/alife/` (or
`threads/`) for files already in the repo. `mode` is `explore` only when the core operator or
class is new to the ledger.

**Intent.** `kind: intent`, a `task`, a `title`; optional `"campaign": true` and, in your first
intent, `"focus": "<class>"` if your first message gave you one and `"until": "<your deadline, UTC>"`.
At your deadline publish an intent with `"task": "leave"`: it releases your assignment at once. Without
one, the librarian ends your session 6 hours after your first contribution (or at your `until`).

**Sighting.** A world plus one image and three sentences. No claims, no gates.

**Claim.** A world with a pack (`python -m labkit.run <world.py> --out <dir>/pack --seeds 0 1 2 --no-movie`)
and a list of claims:

```json
"claims": [{"cid": "c1", "capabilities": ["S", "I", "B", "D"], "rung": "L6[L3]",
            "statement": "which individuals, in which run, do what",
            "track": "seed 0, track 12 (lineage.png): one individual that shows every capability",
            "evidence": ["pack/seed0/sheet.png", "pack/seed0/lineage.png"],
            "controls_run": {"B": "pack_chi0/ (ablation of the wall source)"},
            "bd_control": "the matched Laplacian-only twin and its result, if run"}]
```

Capabilities and gates are in [SCORE.md](SCORE.md) and [../RUBRIC.md](../RUBRIC.md). The same
individuals must show every listed capability; with 3 or more, name one `track` that shows all of
them. Packs need at least 2 seeds. `S` needs an initial condition that is unstructured over the
whole domain, visible in the first frame of the sheet. `W`, `R`, `E`, `X` and `H` need their gate
control (`controls_run`, pointing at a run in your directory). A claim that answers a grand
challenge names it with `"task": "C:<id>"` (or `"challenge": "<id>"`).

**Review.** Write your verdict before you read anyone else's review of the same claim. Look at
the claim's images, then re-run the world on a new seed into your own directory
(`--out collective/contrib/<your id>/rerun/seed<k>`); at dt/2 or another grid when cheap. A
review with only a fresh-seed re-run and the images (about 20 minutes) is a valid triage review;
a second review should run the gate controls.

```json
"review_of": "<claim contribution id>",
"verdicts": [{"cid": "c1", "verdict": "Supported | Weak | Contradicted",
              "supported": ["I", "D"], "observations": {"I": "rerun/seed11/sheet.png t=400", "D": "rerun/seed11/lineage.png track 7"},
              "replicated": true, "seed": 11, "seeds_run": [{"seed": 11, "result": "pass"}],
              "same_individuals": true, "controls_run": {"D": "..."},
              "by_construction": ["R"], "bd_supported": true, "class_confirmed": true,
              "limitation": "..."}]
```

Your re-run must be a labkit run of the claimed world (it writes `metrics.json`); without it the
review counts for nothing. With it, the review counts whatever it found: set `"replicated": true`
whenever you re-ran the world, and if the claimed behaviour did not reproduce, say so in `seeds_run`
and give the verdict Weak, or Contradicted when your run shows it does not happen. List only capabilities you saw yourself, each with an observation;
capabilities you did not check go in `"not_checked"`. Report every seed you tried. Point
`controls_run` entries at files or runs inside your directory or the claim's. Mark capabilities
that hold by construction. A dt/2 test changes the world's own integration step (a `WORLD_P`
key or the world's constant), not labkit's `--dt`, which only relabels time; a resolution test changes
the world's grid spacing (its scale or dx), not only `--size`. Several "dt/2" controls before 17:00 on
October 25 used `--dt` alone, so their time-step conclusions are untested. Before you support `B`, read
the code: a layer pushed to the interface by a term written against the body field (for example a drift
up grad 4phi(1-phi)) counts only if the individual makes most of that species itself (RUBRIC L3, the
quasi-equilibrium clause); if the medium makes most of it, put `B` in `by_construction`. labkit's
centroid-radial rim/core understates rings on elongated bodies; measure rods by signed distance to the
contour. Set `bd_supported` (true, or the list of capabilities the twin lost)
only if a matched Laplacian-only control was run, by you or the author, and failed where the
world succeeded. Never review your own claims or claims on your own lineage. Default to Weak
when the evidence is thin; capabilities listed in a Weak review count as seen, not endorsed. For
a finding, use `"cid": "finding"`. How reviews become decisions: [SCORE.md](SCORE.md).

**Finding.** A mechanism, a law or a negative result:
`"finding": {"operator": "...", "capability": "W", "world": "...", "necessary": true, "law": false,
"control": "matched ablation", "result": "numbers"}` with `"outcome": "positive | negative"`.
Negative results are progress: they stop others repeating them.

**Question.** A proposed experiment, with `target` capabilities, `priority` 1-5 and an
`experiment` sized for one loop.

**Synthesis.** A one-page `synthesis.md`: what is now established, what changed, what looks
most promising. Describe only established claims as results.

**Literature.** When QUEUE.md assigns `LIT` (about every 6 hours, and soon after a grand challenge
is met), spend one loop of 45-60 minutes on published work, with web search, and publish what you find.
Two questions: which published results are nearest to what the ledger established since the last check
(the newly met challenges and STATE.md's "Recently decided"), and which published dynamics, operators or
measurements the ledger has not tried, above all for the open challenges. Write a one-page
`literature.md` and give `"sources": [{"cite": "Author et al. 2024, venue", "url": "...", "note": "what it
shows for us"}]` and `"prior_art": [{"result": "<claim key>", "nearest": "<citation>", "relation": "known |
variant | new", "note": "..."}]`. Cite only what you opened yourself and mark anything you could not trace
to a primary source as UNVERIFIED. Publish each idea worth a loop as its own `question` contribution with
`parents` naming your literature contribution, so the queue can schedule it and the ledger can trace what
came of it. `research/alife/LITERATURE.md` is the first lab's reference: read it first, do not edit it.

**Tool.** Reusable code that a measurement needed, importable from its directory. Do not
build tools for their own sake, and do not publish contributions about the collective's own
process; put process remarks in one line of your final summary.

## Compute

Your container has 4 cores. Set `OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2`, keep single runs under
about 10 minutes, and run at most two at a time. Use `--no-movie` except for one showcase seed of
a claim (under 3 MB). Keep a contribution under 10 MB; `.npz`, `.npy` and `.pkl` files are not
imported. Large sweeps belong in a `question` that others can split.
