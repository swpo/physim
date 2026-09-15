# Documentation and repository audit

Audit date: 9 September 2026. Scope: the current working tree, all 29 HTML pages, repository entry points, the blob simulator/registry, and the active prediction-function evaluation path. This is a rewrite plan; the site and scientific code have not been changed.

**Keep the science and the executable evaluation machinery. Rebuild the public explanation around one path: choose a blob-field world, investigate it through experiments, submit a prediction function, and evaluate its forecasts.** The current documentation is organized around older benchmark families and the sequence of research campaigns. An external reader cannot readily identify the program that now exists.

The registry is part of this work, not a later documentation add-on. See the [world registry plan](REGISTRY_PLAN.md) for the proposed artifact model, hosting decision, and first release.

## 1. What the documentation should say

Suggested opening:

> Physim studies whether AI agents can learn to predict unfamiliar physical systems through experiments. Its worlds are spatial fields whose interactions produce persistent structures and collective dynamics. An agent observes and intervenes through instruments, then submits a Python function that predicts what those instruments will measure under new experimental programs.

Immediately distinguish the program from its present coverage:

> The current evaluation demonstrates this workflow on one prepared blob-field world. Additional worlds exist as simulation assets and research candidates; they do not yet have the same prediction-suite coverage.

The current implementation supports these statements:

| Concept | Current meaning | Source |
|---|---|---|
| World | A field model and its numerical dynamics. The current worked world has 4 activator fields and 8 coupled channels. | [genome](../../environments/physim/physim/blobdata/p4g2_044.json), [CPU simulator](../../probes/blobs/blobkit/blobkit/soup/sim_cpu.py) |
| Prepared instance | One exact field state and apparatus configuration, rebased to experimental time zero. | [origin binding](../../probes/blobs/agentenv/round6/worked_example/p4g2_044/origin.py) |
| Experiment | A complete action/query program, restarted from that preparation with independent ongoing noise. | [exploration service](../../environments/physim/physim/blobround6_explore.py) |
| Deliverable | `predict(actions, queries, n_samples=64, seed=0)` plus learned data/parameters. Each member describes a coherent possible trajectory across the requested readings. | [agent contract](../../probes/blobs/agentenv/round6/worked_example/AGENT_SPEC.md) |
| Evaluation | Frozen code runs without experimental access. Forecasts are compared with independent truth realizations on undisclosed programs. | [native taskset](../../environments/physim/physim_r6/taskset.py), [grader](../../environments/physim/physim_r6/evaluation.py) |
| Scientific score | Mean predeclared joint energy, lower is better; marginal CRPS supplies diagnostics. Verifiers additionally maps the error to `1 / (1 + error)` for its reward field. | [scorer](../../environments/physim/physim/blobround6_eval.py), [reward hook](../../environments/physim/physim_r6/taskset.py) |
| Demonstrated coverage | One preparation of `p4g2_044`, 15 programs, 64 forecast members and 2 retained independent truth realizations per case in the native model runs. | [grader](../../environments/physim/physim_r6/evaluation.py) |

Use “prediction function” in explanatory prose and `predict(...)` in API material. Keep round numbers, pilot names, and protocol IDs in metadata and references. Describe “world”, “prepared instance”, “evaluation suite”, and “run” separately throughout.

## 2. Main findings

| Priority | Finding and evidence | Recommended change |
|---|---|---|
| First | The [homepage](../../docs/index.html) introduces prediction, state preparation, and executable theories as separate objectives, then promotes bulk/chemistry/ecology/evolution leaderboards. Blob fields appear as a “new” side project. | Rewrite the homepage and primary navigation around the current program. Start with the physical system and one experimental example. |
| First | The [scoring page](../../docs/scoring.html) explains scalar contracts, noise-floor-subtracted accuracy, preparation policies, and optional executable-theory bonuses. These do not describe the current prediction-function scorer. | Replace the page. Explain samples, joint dependence, fixed score groups/scales, scientific error, and the separate framework reward. |
| First | [Measuring evolved worlds](../../docs/blobs/measuring-evolved-worlds.html) calls the stopped R5 pilot “current”, describes `ready()` and six answer payloads, and includes operator cancellation/authorization notes. | Replace its public entry with the current experiment → validate → submit → grade workflow. Retain the old article only as an archival record. |
| First | The root [README](../../README.md), [environment README](../../environments/physim/README.md), [`physim` exports](../../environments/physim/physim/__init__.py), and [run script](../../run_grid.sh) lead to the older taskset. The run script also contains a machine-specific working directory. | Provide one current installation/example path. Link directly to its code and explain its present scope. |
| First | Active evaluator modules, taskset modules, and the worked-example fixtures exist locally but are not tracked in Git. | Establish the reviewed release set before claiming that an external checkout reproduces current results. Keep generated runs and large data outside that source set. |
| First | [`physim_r6.evaluation`](../../environments/physim/physim_r6/evaluation.py) imports `origin`, `contract`, and `isolation` through research-tree path injection. [`origin.py`](../../probes/blobs/agentenv/round6/worked_example/p4g2_044/origin.py) reads a local cache and study metadata. | Extract the reusable runner pieces into the installable package and supply world/preparation data through the registry. A wheel or clean checkout currently lacks the complete supported path. |
| Next | [`physim.results`](../../environments/physim/physim/results.py), [`physim.viz`](../../environments/physim/physim/viz.py), and [`physim.traces`](../../environments/physim/physim/traces.py) generate the old public pages, including `scoring.html`. | Change ownership of public page generation before rewriting generated HTML. Retire these outputs from the default build or direct them into an archive. |
| Next | The blob series makes readers traverse campaign identifiers, repairs, cost histories, and “what happened next” sections to recover enduring scientific ideas. | Extract concept-oriented explanations, world cards, and a few well-captioned films. Keep experimental qualifications; remove the process narrative from the main reading path. |

The local homepage and the “Measuring evolved worlds” reading path were also inspected in a browser. The same mismatch is visible in the rendered pages. The deployed GitHub Pages site could not be verified through the web fetch tool; these findings are about the repository's site sources and their local rendering.

## 3. Keep, rewrite, or archive

“Archive” means retain recoverable provenance and old URLs where useful, with a short archive notice and a link to the current page. It does not mean deleting scientific evidence or inserting a history section into each new page.

### Public pages

| Existing page(s) | Disposition | Material to carry forward |
|---|---|---|
| `index.html` | Rewrite | Project name and the question of learning through experiments. |
| `worlds.html` | Rewrite | The distinction between physical behavior and instrument observations. Replace the old track taxonomy with blob-field worlds and registry status. |
| `scoring.html` | Rewrite | The motivation for distributional scoring. Take the actual contract and formulas from the current evaluator. |
| `results.html` | Rewrite | A compact evidence summary tied to a suite revision and run conditions. The current trials are development evidence, not a broad world-generalization leaderboard. |
| `rollouts.html` | Replace with selected examples | One coherent experiment-to-predictor walkthrough and downloadable full traces. |
| `worlds-bulk.html`, `worlds-chemistry.html`, `worlds-life.html`, `worlds-evolution.html` | Archive | Their figures can remain with the old benchmark; they do not define the current world family. |
| `results-bulk.html`, `results-chemistry.html`, `results-life.html`, `results-evolution.html` | Archive | Preserve the original results and conditions without pooling them with prediction-function scores. |
| `rollouts-bulk.html`, `rollouts-chemistry.html`, `rollouts-life.html` | Archive / separate downloads | Raw evidence, reachable from archived results rather than primary navigation. |
| `blobs.html` | Merge into Worlds and World generation | A short field-based introduction; replace the numbered-series table and campaign status with reader-oriented links. |
| `blobs/what-is-a-blob.html` | Keep and edit | Best starting explanation and simple field illustration. Present the three-field system as a foundational example; the current worked world has 12 fields. |
| `blobs/blobs-move.html` | Extract | Drift, motion, a clear film, and the measured relationship. Put numerical-method detail in the simulator reference. |
| `blobs/blob-chemistry.html` | Extract | Binding, interaction outcomes, and persistent structures; define the physical meaning of species. |
| `blobs/molecules-that-move.html` | Extract | Moving bound structures and rotors, with a small selection of evidence and films. |
| `blobs/living-landscape.html` | Extract | Feedback between structures and fields, trails, and memory. |
| `blobs/machines.html` | Extract a showcase; archive campaign narrative | One or two compelling examples of composition and transport. Label which worlds demonstrate them. |
| `blobs/bounded-structures.html` | Extract | Rings, permeability, and boundaries. Prefer these physical labels to “the first cell”. |
| `blobs/searching-equation-space.html` | Rewrite as World generation | Genome representation, variation, selection, and the distinction between generating candidates and validating evaluation tasks. |
| `blobs/accelerating-blobs.html` | Move to simulator reference | Backend architecture and numerical parity. Keep hardware/performance measurements in a separately versioned technical note. |
| `blobs/evolving-at-scale.html` | Archive campaign; reuse selected world cards | Selected genomes and films, with provenance. Campaign yield and operator scoreboards need not be part of the introduction. |
| `blobs/measuring-evolved-worlds.html` | Replace / redirect | The instrument illustration and motivation; use the current task contract and examples for the explanation. |
| `blobs/breeding-spatial-economies.html` | Archive campaign; reuse qualified examples | Candidate provenance and selected films. Descriptor-bin occupancy should not be presented as the number of validated physical worlds or tasks. |

### Code and repository material

| Existing material | Keep | Clean or change |
|---|---|---|
| `blobkit` genome and CPU/GPU simulation code | Numerical implementation, packaged genomes, lock/parity machinery | Make it a clear dependency with consistent package metadata and one authoritative world-artifact loader. Avoid copying the simulator into the evaluator. |
| `blobkit.worlds` | Existing packaged-genome lookup | Extend through a versioned registry resolver. It currently lists 15 packaged genomes; it is not an evaluation-suite registry. |
| `blobround6.py`, `blobround6_explore.py`, `blobround6_eval.py` | Scheduler, experiment semantics, validation, proper scores | Give these clear public module roles and move version history out of docstrings. Preserve numerical behavior during packaging work. |
| `physim_r6/taskset.py` | Native Verifiers integration and laboratory tools | Make it the documented current entry. Consolidate repeated roster/limit definitions and replace prose-budget string substitution with rendering from the same validated specification. |
| `physim_r6/evaluation.py`, worked-example `isolation.py`, `container_worker.py`, `origin.py`, `contract.py` | Their present responsibilities | Package reusable runtime code; make the preparation and suite explicit data inputs instead of import-path conventions. Use a portable temporary directory instead of a literal `/private/tmp`. |
| `physim_r6/scaling.py` | Inference-spend accounting | Keep the distinction between science budgets and inference/runtime limits. Put per-run choices in example configs and result metadata, not the scientific definition of a world. |
| Tests and physics/control studies | Semantic checks, causal evidence, score-ablation checks | Expose a small offline check and one full demo. Keep research-sized studies separate. |
| Root `DESIGN.md`, `REPORT.md`, `IDEAS.md` | Research record and sources worth extracting | Remove from the onboarding route; consolidate under a clearly secondary research archive when path dependencies have been checked. |
| `HANDOFF.md`, `SESSION_MIGRATION.md`, `handoff/` | Maintainer continuity | Keep outside the public explanation. Agent-session instructions are not the project introduction. |
| Old `engine/session/taskset`, `blobround2/5`, old MCP server and custom rollout loops | Reproduction of historical results | Make their legacy role explicit; do not put multiple equivalent-looking quickstarts in the main README. Defer bulk moves until active dependencies have been extracted. |

There is no root license file, while `blobkit/pyproject.toml` currently declares `Proprietary`. Resolve the intended code/data/media licenses before the external release. Also reconcile the package versions: the blobkit README says 0.3.0, source metadata says 0.3.5, and the local installed distribution reports 0.3.4. Version numbers alone are currently insufficient to identify the executed source.

## 4. Proposed public structure

Keep six primary destinations and a small reference area:

| Destination | Reader's question | Required content |
|---|---|---|
| Overview | What is Physim? | Short definition, one field film, one experiment/prediction illustration, current coverage, links to Try and Worlds. |
| Worlds | What systems can I study? | Registry-derived cards; world versus preparation; observed phenomena; availability and evaluation status. |
| Experiment and predict | What does an agent do? | Instruments, independent experiments, actions/queries, sample output, validate/submit/freeze lifecycle. |
| Evaluation | How is a predictor judged? | Independent truth, coherent samples, joint energy, diagnostics, fixed scales/groups, failures and limitations. |
| Try it | How do I run something? | A small offline scoring example, a registry-backed reference demo, then an explicitly costed model-run example. |
| Results | What has been demonstrated? | Suite identity, run conditions, baseline and selected model evidence, validity/limit status, links to artifacts. |

Reference pages: **World generation**, **Simulator and numerics**, **API and artifact schema**, **Contributing a world**. The archive gets one footer link, not a competing navigation tree. The README should give a short introduction, a working quickstart, and a compact source map.

The public pages should retain a few essential qualifications: current coverage is one preparation; the truth ensemble has two realizations per case; the present primary groups miss some fine timing errors; a low aggregate score does not prove recovery of every mechanism. These affect interpretation and belong near the relevant claim. Failed deployment attempts, operator permission notes, and chronological repair accounts do not belong there.

## 5. Implementation order and completion criteria

1. **Fix the public contract and page ownership.** Set the current terminology, primary paths, and archive mapping. Stop old generators from overwriting current pages. Rewrite the overview, task, and scoring explanations from the code.
2. **Package one reproducible reference world.** Implement the registry manifest/resolver and remove research-tree requirements from the supported example. Preserve the prepared field hash, independent-noise behavior, apparatus, cases, and scientific score.
3. **Make a clean installation work.** Review and track the active source set; declare dependencies; reconcile versions; document and build both container layers; replace local output paths in example configs. Verify from a clean environment without an existing research cache.
4. **Build the world and evidence pages.** Generate registry cards and result tables from small validated manifests. Curate films and the worked example. Move old material out of navigation and preserve useful redirects.
5. **Check the external-reader path.** A reader should be able to explain the task after one page, find a world's downloadable assets, run the documented offline example, inspect a predictor, and interpret its score without opening a handoff or chronological lab log.

Do not make a broad simulator rewrite a prerequisite for the documentation. The necessary code work is packaging, dependency boundaries, a registry-backed example, and a clear supported entry point. A public facade can be introduced while retaining internal compatibility imports.

The site can remain static. Use a shared template/navigation and maintain content in one source format; do not add an application backend for these pages. Add a viewport declaration and check narrow-screen reading. The inventory found 29/29 pages without that declaration, 8 image instances without `alt`, and no missing local link or fragment targets. This is primarily a content and organization problem.

## Audit evidence

- [Inventory and link results](inventory.json): 29 pages; approximately 33,043 words outside the three raw rollout pages. Those three pages contain roughly 663,330 words of embedded trace content. There are 105 media files totaling about 114 MB; their presence does not mean every asset should remain on the main site.
- [Inventory script](inventory.py): counts source text, including collapsed transcript details; it does not claim all text is visible at once. External links and media playback were not exhaustively checked.
- [Local package provenance](local_environment.json), [evaluator check](evaluator_check.log), [exploration check](exploration_check.log): 30 evaluator tests and 10 exploration tests passed, using toy systems only.
- Registry and packaging findings come from current source inspection, not a claim that a clean install or remote registry already works.

No model calls, new native world simulations, publishing, deletion, or scientific-source edits were performed for this audit.
