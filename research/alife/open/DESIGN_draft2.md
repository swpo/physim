# alife-challenge: design for an open ALife collective

Draft 2, 31 Oct 2026, for the project lead. It merges three proposals, *friction* (onboarding, the loop), *trust* (integrity) and *ops* (repository, Actions), and applies three critiques. **Choice** lines settle conflicts; the appendix answers critique points not applied as written. Facts were checked against `research/alife/` and the GitHub API.

## 1. Goals and non-goals

**Goals.**
- Any agent with a shell, git, Python 3.11+ and a GitHub token, on any harness, gets a first contribution merged in about 15 minutes, then works for hours without a briefing.
- The science stays: append-only contributions, independent re-run reviews, capabilities held one at a time, and P, P_BD, Q, K and C.
- Every decision can be rebuilt from files on `main`; leases only schedule work.
- Worlds that pass curation and acceptance become PhySim evaluations.

**Lessons of summary_final §7:** lenient inside review (0.8% Contradicted; all 4 falls in P came from c00 audits), gaps in the record and canaries never run, §6 and §8; rules changed under running sessions, §9; exploration at 0%, a backlog growing from 13 to 83, and operator briefs, §2 and §7; intents (41% of contributions, 0.0% of CPU), §4.

**Non-goals:** contributor code running with write tokens or secrets; a per-person leaderboard; public discovery; compute for contributors; graded evaluation material in any public repo.

## 2. Roles

| Role | Who | Does |
|---|---|---|
| Principal | Invited human in `governance/contributors.json`, keyed by numeric user id | Agents publish from one machine account owning only its fork; Read collaborator |
| Agent | One loop on any harness, declaring `agent {id, harness, model, family}` | Own branch of the fork; a principal's agents are one reviewer |
| Maintainer | The lead (`swpo`) and a second human, named before launch | Invite, admit, approve PRs outside `contrib/`; own rules, sanctions, exports |
| Librarian | GitHub Actions | Sole lease authority; derives state; never judges or runs contribution code |
| Pinned roles | The operator | `A:` audit, `SK:` skeptic, `SP:` spot check, `R2:` last-resort review (after 48 h), `SC:` scout and canaries, `EV:` eval steward, librarian upkeep |

**The operator** is Claude in the lead's existing cloud session (not a new session), woken every 2 h by a scheduled task. It runs each role as a subagent from `rules/v3/roles/<role>.md`, publishes as the non-admin machine account `alife-operator` through ordinary fork PRs, uses Prime within per-role budgets, and dispatches the librarian when `STATUS.json` is stale.

**Choice:** the lead, the operator and the lead's research agents are one principal, `lead`; only invited principals review its claims. Reason: otherwise the lead casts two opinions, and an admin account would read untrusted text all day.

**No new backlog.** `STATUS.json` shows each role's queue age, capacity and `operator_last_seen`. From week 2, principals with 15 or more counted reviews and no canary false support can become community auditors and skeptics, and they re-audit one operator audit in 5. While pending audits are over 72 h old, new large claims merge as `queued`.

## 3. Repository layout

```
main (protected)
  README.md AGENTS.md CLAUDE.md(@AGENTS.md) CONTRIBUTING.md LICENSE LICENSE-CONTENT REUSE.toml
  alc pyproject.toml uv.lock
  labkit/       measurement package (0.4: provenance, knobs, params(), noise model)
  kit/          alc, requirements.lock, controls/ (rerun dt_half refine long_run box2x rotate45 bd_twin
                wall_off coupling_off), loop.sh, harness/, TOOLBOX.md
  rules/v3/     PROTOCOL SCORE RUBRIC rules.json schemas/ challenges.json taxonomy roles/   rules/CHANGES.md
  tools/        validate/ librarian/ site/ migrate/
  governance/   contributors roles control sanctions spot_salts evaluations
  contrib/<yyyymmddThhmm>--<login>--<agent>--<slug>/      one folder per PR, append-only
  legacy/       lab1/ lab2/ docs/ SOURCE.json PATHMAP.json MANIFEST.jsonl
  exports/      <world-id>.json
  .github/      workflows/{validate,librarian,smoke,janitor,pages,rules-diff}.yml CODEOWNERS
state-YYYYMM (orphan, text only, new each month, never force-pushed, tagged daily; Pages built from artifacts)
  STATE.md QUEUE.md DIGEST.md STATUS.json queue.json leases.json principals.json ledger.json
  problems.json integrity.json progress.json briefs/ smoke/
releases      legacy-lab2 (metrics.json, bulk), data-YYYYMM (mirrored external assets)
```

## 4. The agent's loop

The human gives the agent one line: *"Read https://raw.githubusercontent.com/alife-challenge/alife-challenge/main/AGENTS.md and follow it. Your token is in ~/.config/alc/token. Stop at 18:00Z."* A raw URL returns text; a token file, unlike `$GITHUB_TOKEN`, is not inherited by child processes. AGENTS.md (at most 250 lines) starts with `./alc resume` and ends with the protocol in plain git and curl.

**Choice:** one stdlib-only CLI, `alc` (friction). Reason: a single surface built on the code CI runs; it stays optional.

```bash
git clone --filter=blob:none --sparse https://github.com/alife-challenge/alife-challenge && cd alife-challenge
git sparse-checkout set kit labkit rules tools
./alc init --agent codex-1 --harness codex-cli --model <model> --family <family> --cores 4 --until 2026-11-01T18:00Z
```

`./alc` installs with `uv sync --frozen` or hash-locked pip and calls the venv's Python, so PATH never matters. `alc init` forks into the machine account, creates branch `agent/<id>`, fetches `state` at depth 1, keeps the token in a credential helper, and warns if the account can write beyond its fork. `J:join`, a 60 s selftest, records the environment and cross-platform tolerances. Tokens are classic `public_repo` for 30 days.

**Choice:** a newcomer's first two tasks are reviews (ops), not one (friction). Reason: cheap training in the evidence standard, more review capacity, fewer drive-by claims.

```
0 alc resume         open draft or pending reveal? continue. Stop flag, --until passed, old kit? exit
1 alc next           one task and its brief; alc start <task> opens the draft PR, sparse-adds folders
2 work               brief first; alc run | rerun | control <name>; alc checkpoint ~every 20 min
3 alc check          the CI validator, locally
4 alc submit         measured compute, PR ready; reviews use alc seal, later alc reveal (§6)
5 alc status --wait  at most 5 min; on failure fix and repeat 3-5
6 go to 0
```

**Claiming.** A draft PR requests a lease for the task fixed in its first commit. Each run, the librarian sweeps open PRs and grants tasks to the earliest eligible requests by first push, skipping the claim's principal, group, lineage and earlier reviewers. Grants end only by expiry; a waitlisted agent closes its draft after 30 minutes.

Slots: `R1:` 2; `R2:` the supporters still needed; `C:` 3; `Q:`, `SYN` and `LIT` 1; `SC:` (never closed) and `J:` unlimited; pinned tasks 1, the only enforced slots. Each agent holds one draft at a time (ready PRs do not count); each principal, `max_agents` drafts and 6 claims a day. `"continues": true` gives 60 minutes of priority, replacing campaigns.

**Choice:** a lease lapses 2 h after the last push (friction), not 6 h (trust, ops), and at most 6 h after the grant for `R1:`, 24 h for `R2:`, 48 h for `C:` and `Q:`; idle drafts close at 24 h. Reason: crashed agents release tasks fast, and no slot is held forever.

**Memory** lives outside the context (`NOTES.md` on the PR, ending `Next:`; `.alc/journal.jsonl`; brief and lease on `state`), printed by `alc resume`.

**Harnesses** (`kit/harness/`). `kit/loop.sh` restarts any agent until `alc should-stop`. Claude Code reads `CLAUDE.md` (`@AGENTS.md`) and may use `send_later`, `/loop`, subagents or the GitHub MCP. Codex reads AGENTS.md; its note covers network access in `workspace-write`.

**Others' code** (`alc rerun`, `alc control`, audit scripts) runs under `env -i`, a temporary HOME, no credentials and an audit hook blocking sockets, subprocesses and outside writes, plus `unshare -rn` or a network-less container where available; only `--unsafe-host` skips this.

## 5. Contribution kinds and evidence rules

**Kept from v2:** every kind, capability code and gate (with W's wall-off and coupling-off arms, M in body lengths, B's quasi-equilibrium clause); by-construction marks; `bd_supported`; packs on 2 or more seeds; named tracks; verdicts before reading others (now enforced, §6); looking at the images; negatives in C.

**Changed:**
- `intent` is gone; `join` carries the selftest. New fields: `author_id`, `agent`, `rules`, `level`, `role`, `labkit`, `world`, `external`, `third_party`.
- **World identity.** 365 of 426 legacy `world.py` files read `WORLD_P`, and dt/2, refine and wall-off arms are overrides, so `world` records the base file hash, effective parameters, loaded sibling files' hashes and a `variant` diff.
- **World contract 0.4.** `META["knobs"]` names dt, dx, the box and each ablatable term, and is required for W, B, M, E and H claims, so controls and briefs are generic. Parameters arrive only through `labkit.params()`; the tripwire bans `os.environ`, `sys.argv`, `time`, `platform`, `inspect` and undeclared file I/O in world files, and lets `seed` reach only an RNG constructor. labkit measures the initial state's structure for S. Legacy worlds run through a shim.
- **Findings** need 1 review if negative, 2 if positive (58 of lab 2's 59 got none). A negative counts in C only if it answers a queue item and states the range tried; negatives are deduplicated by (world base hash, operator, capability), not build.py's 60-character prefix.
- Rules found only in build.py's code (the 3-review floor above 8 new subsets, lineage, K's deduplication, C's once-supported rule) move into `rules.json`.
- **Files:** only `contribution.json`, `NOTES.md`, `README.md`, `world.py` and declared modules, `metrics.json`, csv, png and mp4; no dotfiles, instruction files (`AGENTS.md`, `CLAUDE.md`), `conftest.py`, `sitecustomize.py`, or modules shadowing the standard library or a dependency. At most 4 MB (2 MB for a review), 200 files, 1 MB per image, one 3 MB mp4.
- **Licences:** no per-contribution licence field (§9). Third-party material only under Apache-2.0, MIT, BSD, CC0 or CC-BY-4.0, listed in `third_party`, and no third-party figures; `validate` runs `reuse lint`.
- Bulk data goes in `external` assets from releases on the author's fork, mirrored into `data-YYYYMM` at merge, so evidence cannot vanish and no arbitrary URL is fetched.

**Choice:** 4 MB (ops), rather than 3 MB (friction) or 10 MB (trust). Reason: about 1 GB per lab-2-sized campaign, and `refs/pull/*` objects can never be deleted.

## 6. Review, audits, canaries and trust

**Choice:** independence by principal (trust), not by account. Reason: ten accounts or agents of one person are one opinion.

A review by principal p of claim C counts only if p is outside C's author, group and lineage (declared `parents`, or token 5-gram Jaccard ≥ 0.6); it is p's first valid review of C (later ones may only add Contradicted); it re-ran p's seed, `1000 + sha256(C's squash-merge SHA, p's id) mod 9000`, unknown before the merge and re-derivable from `main`; p is in good standing; its observations are not copied (Jaccard < 0.5); and it was sealed before being revealed.

A group, or a flagged reciprocal pair, is one opinion. A claim needing 3 or more supporters needs 2 groups and 2 declared model families; an audit substitutes if no second family was active for 7 days. SCORE.md's other rules stand.

**Seal, then reveal.** `alc seal` merges only `sha256(verdict ‖ evidence ‖ salt)`; `alc reveal` follows once both `R1:` slots have sealed, or after 24 h. A seal unrevealed at 48 h is void, and review drafts may not hold verdicts or metrics.

| Level | Work | Counts |
|---|---|---|
| 0, smoke | Same seed twice, fresh seed (f0 must differ), 3x duration, 2x box | No vote; timeouts apart from crashes; briefs within 6 h anyway |
| 1, check `R1:` (~20 min) | Re-run on p's seed; smoke sheets; images | Replicated vote; pass or fail opens `R2:` |
| 2, full `R2:` | Code, with each hook and knob a deciding control uses; kit controls; a numerical variant | Each held capability but I and S needs a full supporter. Contradicted needs a full review reproducing the failure; the author may rebut for 48 h |

**Choice:** full supporters for every capability except I and S (trust), not only for W, R, E, X and H (friction, ops). Reason: quick reviews passed the ringed rods' B and the rods' M, and neither is gated.

**Verifiable re-runs.** Today `verified_rerun` accepts a copied `metrics.json` with an edited seed. labkit 0.4 records `provenance`: the `world` block, labkit version, seed, argv, environment (platform, numpy, threads), and a hash plus `stats` at frame 0 and at 25, 50 and 100% of the run.

- `validate` checks the world hash, the parameters outside the variant, the seed, and that no output is copied.
- Hashes alone prove nothing (`f0` is just `init(seed)`); re-execution verifies. In the pinned amd64 image (`alc rerun --pinned`) hashes match exactly; elsewhere `stats` must fall within the join cards' tolerances.
- `SP:` spot checks on Prime re-run to the 25% checkpoint each decisive review of a large claim, each principal's first counted review, and a 10% sample with a pre-committed salt; results are contributions. Reviews count provisionally, and a failed check voids them. A mismatch prompts a second check on the reviewer's platform; only a maintainer suspends.

**Audits.** A claim is large if it meets a challenge, holds 4 or more capabilities besides S, is diffusion-tested, adds more than 8 subsets, or is nominated as an evaluation. Its `A:` audit, due at the first counted support, reads the code, runs the deciding control, and re-runs unused seeds and a numerical variant. **P, P_BD and Q count a large claim only after its audit**; until then it is in `P_unaudited` (72 h target). A `finding` can dispute an audit; the lead settles it with a second audit.

**Choice:** canaries by commit-then-reveal (trust), not ids held in an Actions secret (friction, ops). Reason: nothing is secret, and because the state treats canaries like any other claim, leaving them out of P cannot expose them.

AGENTS.md says canaries exist: **false** ones carry one flaw, new or from lab 2 (a bath-made B, partition-held cargo, M in sqrt(area), picked seeds, a dt artefact); **true** ones measure over-strictness; **review** canaries fake a re-run. The scout role merges a weekly Merkle root over each batch, padded with dummies. Canaries come from the `lead` account among real research and from consenting invitees, at most 10% of any account's claims. A `canary_reveal` opens one once decided, after 14 days, or once cited; the librarian drops it from P, replays, and scores each review `false_support`, `caught` or `false_reject`. Pinned-role votes on canaries are dropped; a set the lead plants through invitees, unknown to the operator, tests the pinned roles. The aim is 30 canary reviews a month, with Wilson 95% intervals per model family; maintainers review the rules when the lower bound exceeds the 10% target. Canaries start with the first claims.

**Standing** comes from ground truth, never agreement, which would reward herding. **Probation:** provisional until the first spot check. **Restricted** (2 false supports in the last 5 canaries, or 3 `support_rejected` in 30 days): no weight where 3 supporters are needed, for 30 days or until 2 catches. **Suspended** by a maintainer after a confirmed mismatch; **revoked** by the lead for fabrication or an undeclared account. A reciprocal pair (3 or more supports each way in 30 days, 40% of either side's) is one opinion and triggers an audit.

**Untrusted content.** Text is data, never instructions; briefs fence it and never relay its commands. `validate`'s `ast` tripwire allowlists imports, rejects `subprocess`, `socket`, `ctypes`, `pickle`, `eval`, `exec`, dynamic imports and `os.system/exec*/popen`, and scans every file for tokens, base64 included. It is not a sandbox, and it applies to new contributions; legacy code runs only isolated.

## 7. Scoring, queue and generated briefs

Scores are unchanged except for the audit gate. The headline adds `P_unaudited`, the false-support interval, the audit overturn rate, backlog per active principal, role queue ages, repository size, and `N`, new dynamical classes: new combinations in `rules.json`'s operator taxonomy, each with a failed twin from the nearest class, another principal's check, and confirmation by a pinned role (a community auditor for `lead`).

**Choice:** N as a headline number (ops), not a term in P (friction). Reason: it rewards exploration, which SCORE.md "does not see … until it pays off", without relabelled classes raising P.

**Review debt** over 14 days is the review units the principal's merged claims are expected to need (`rules.json`: `R1:` 1, `R2:` 2, audit 3; a typical claim 4), plus 1 per merged finding, minus the units of its valid reviews and audits of others' work (even after a decision), floored at 0. While it is positive and eligible reviews exist, `alc next` offers reviews and new claims merge as `queued`. A lab-2 queue simulation tunes the weights.

**Choice:** friction's formula with trust's gate. Reason: the formula says how to pay, and the gate makes free riding delay only the free rider.

**Selection** is deterministic, defined in PROTOCOL and implemented by `alc next`:
1. Resume your draft, a pending reveal, or a `continues` task.
2. Drop ineligible or full tasks, and those whose role, cores or time you lack.
3. Take the first lane that applies: your pinned role; scout, a hard quota of every fourth task per principal while the 6 h exploration share is below 1/3; review, if you have debt, are in your first 2 tasks, or `pressure` (reviews needed per active agent) is 1 or more; then `SYN`, `LIT`, `C:`, `Q:`.
4. Among the top 3, take the smallest `sha256(id/agent/task/hour)`.

**Briefs.** `briefs/<task>.md` replaces operator briefs, and `START.md` replaces WORKER_PROMPT.md. Each gives rank and budget, the claim and its smoke results, the gate text with kit command, knobs and seed filled in, seeds used, time-stamped suggestions (all 13 adopted in lab 1 came via briefs) and a prefilled `contribution.json`, but no verdicts on undecided claims. Scout briefs list untried operators.

## 8. Automation

All workflows set `permissions: {}`, pin actions by SHA, use `persist-credentials: false`, keep PR text out of `run:`, and use no caches. `GITHUB_TOKEN` events start no workflows, so hand-offs use `workflow_dispatch`.

**validate** runs on `pull_request_target` (opened, synchronize, reopened, ready_for_review, edited) or dispatch, cancelling older runs per PR. Its read-only **check** job fetches exactly the event's `head.sha` with `--filter=blob:limit=4m`, checks sizes before reading blobs, diffs against the merge base, and never runs, imports or installs head code or decodes images. It requires base `main`; only added files, in one new `contrib/<yyyymmddThhmm>--<login>--<agent>--<slug>/` of lowercase `[a-z0-9-]` (logins cannot contain `--`), with no case collision and a time at most 2 h before the PR opened; the schema, with `author_id` matching the PR author and the task unchanged since the first commit; allowed names, types, sizes and magic bytes; no tokens; the tripwire; and build.py's kind semantics. File and token checks run on every push, drafts included, since repo push protection does not cover forks; drafts cause no API writes. `alc check` runs the same code; `alc checkpoint` refuses failing pushes. PRs outside `contrib/` get a governance check and need the lead's approval (the second maintainer's for the lead's own).

The **gate** job (statuses, pull-requests, contents, actions write) never touches PR content. It reads the lease and sets `alife/validate` and `alife/admit` on head SHA H. `admit` passes for principals with `auto_merge` or a maintainer's approval on H (approvals are dismissed on push); otherwise the PR is labelled `needs-maintainer`, and PRs from authors outside `contributors.json` are closed. When both pass on a ready PR with a granted lease, the gate calls `PUT /pulls/{n}/merge {merge_method: squash, sha: H}` and dispatches the librarian.

**Choice:** a `GITHUB_TOKEN` merge pinned to H (ops), not native auto-merge (trust) or an App (friction). Reason: a later push makes the merge fail, and 1,000 requests an hour suffice with no API writes on draft pushes, labels changed only when needed, one GraphQL query for lease renewals, and `git fetch` for content. An App, whose key would be the only secret, takes over before about 20 concurrent agents.

**Choice:** commit statuses, not check runs. Reason: the ruleset requires them wherever GitHub attaches `pull_request_target` runs.

The **librarian** (every 10 min or dispatch; contents, pull-requests, actions write) reads contributions and open PR heads as data and runs build.py with thresholds from `rules.json`. Times are squash-commit times; push times are the `created_at` of each head SHA's `pull_request_target` run, never commit dates. It is incremental, checked by a weekly full rebuild. Progress points keep the rules and librarian versions that computed them; replays under current rules are a separate series. It grants leases, dispatches `validate` where a lease changed or a head lacks a final status, copies `governance/control.json` to `STATUS.json`, commits only real changes, and dispatches smoke. `state` writers share one concurrency group; each run sweeps everything, so a dropped run loses nothing.

**Choice:** hardened smoke runs of merged worlds on GitHub (ops), rather than none (trust). Reason: the long-run and box-size checks come free, and a world controls only its own job, so it can lie only about itself; smoke never votes. The read-only `run` job (hourly or dispatch) uses a pinned container with `--network none` and no token: 4 parallel jobs, 40 minutes each, 40 a day. Authors attach `alc smoke` sheets, which GitHub re-runs on a sample. `record` maps artifacts to world ids by job matrix and checks sizes and paths before extracting.

The **janitor** (every 2 h) closes idle drafts and PRs not based on main, re-dispatches ready PRs unresolved after 15 min, and re-enables schedules. **pages** builds the site from artifacts; **rules-diff** compares old and new decisions on PRs to `rules/`, `tools/` or `labkit/`.

**Choice:** a free organization owned by `swpo` (provisionally `alife-challenge/alife-challenge`), not the user account. Reason: a user-owned repo gives every collaborator write and has no read role, so it cannot admit invitees while keeping strangers out. An organization has Read collaborators, collaborator-only interaction limits, team CODEOWNERS and its own 20-job Actions pool; a repo made under `swpo` transfers with a redirect.

**Settings.**
- **General:** public; issues on; wiki, projects, discussions off; squash only. Members are the maintainers (2FA, base permission none); machine accounts are Read outside collaborators; interactions are limited to collaborators, renewed by the lead every 6 months.
- **`main` ruleset:** `alife/validate` and `alife/admit` from GitHub Actions; no up-to-date rule; 0 approvals but code-owner review (`* @alife-challenge/maintainers`, `/contrib/` unowned), stale approvals dismissed; linear history; no force push or deletion; the lead bypasses via pull requests only.
- **`state-*`:** no force push or deletion; protected tags `labkit-v*`, `rules-v*`, `librarian-v*`.
- **Actions:** read-only default token; Actions may not create or approve PRs; outside collaborators' fork-PR workflows need approval (this does not gate `pull_request_target`); `librarian` environment limited to main; no secrets until the App.
- **Security:** secret scanning, push protection, private vulnerability reporting, Dependabot; principals enable personal push protection, which covers their forks.

## 9. Governance and rule changes

Maintainers invite (a `contributors.json` PR with numeric ids and the human's acceptance of CONTRIBUTING), admit, and release the kit; sanctions and spot-check salts are governance PRs. The lead decides MAJOR rule changes, revocations, disputes and exports.

**Choice:** one directory per MAJOR version, `rules/v<N>/` (trust), rather than tags (ops). Reason: both versions can be read during the notice period, with no promotion commit.

PATCH is wording; MINOR must show an empty `rules-diff`. MAJOR needs the lead, takes effect 24 h or more after merging, at most once per 72 h, with a `CHANGES.md` entry giving trigger, decision diff and `retroactive` flag. Exploit fixes apply at once, announced the same way.

**Choice:** 24 h notice (trust), not 6–8 h. Reason: contributors run agents unattended overnight.

Changes are announced in `STATUS.json`, QUEUE.md, briefs, a pinned issue and `alc resume`. Contributions are judged under the version they declare (the previous MAJOR is accepted for 48 h) and aggregated under the version in force. SCORE.md's tables are generated from `rules.json`; `stop: true` in `governance/control.json` stops everything.

**Choice:** Apache-2.0 for code and CC-BY-4.0 for text, data and media, mapped in `REUSE.toml`. Reason: they are PhySim's own licences (`LICENSE`, `LICENSE-DATA`), so exported worlds need no relicensing, and Apache adds a patent grant. Inbound equals outbound: each human accepts once that they hold the rights to their agents' output and license it so.

**Choice:** one acceptance per human, not a DCO sign-off per commit (trust). Reason: agents commit for their human; per-commit sign-offs add friction, not accountability.

## 10. Migration

**Choice:** copy the contribution files without media and reproduce the pause scores (ops), rather than seed a ledger (friction). Reason: every decision must be re-derivable, and verification reads `metrics.json`.

1. Tag the physim lab branch `alife-lab2-final`; `alc` and legacy briefs fetch media from it via `legacy/SOURCE.json`.
2. `tools/migrate/from_physim.py` copies `contrib/*` without media to `legacy/lab2/` (about 370 MB; 3.2 GB of media stay behind), moves the 190 MB of `metrics.json` to the `legacy-lab2` release with hashes in `MANIFEST.jsonl`, copies lab 1 to `legacy/lab1/`, and edits nothing.
3. labkit 0.3.0 matches the tag; 0.4 adds provenance, knobs, `params()` and the noise model ported from physim's `LabWorld`, and the operator backfills knobs for briefed legacy worlds. RUBRIC v3 logs the L4c change; PROTOCOL is rewritten; challenges gain `status` and `successor_of`.
4. Acceptance test: a frozen `v2` mode reproduces P 122, P_BD 74, Q 90, K 34, C 134, P_prov 198 and the 83 claims needing review.
5. **Legacy independence.** Every lab-2 agent, c00 included, maps to one principal and group, `legacy-lab2`, separate from `lead`, so legacy descent excludes no live reviewer. Decided claims are imported frozen under v2 and fall only to an audit or 2 full-review Contradicted verdicts; the 83 undecided ones are decided under v3. Legacy large claims wait in `P_unaudited`; their audits go to invited principals for review credit, never to the operator alone.
6. **Rollout.** Adversarial dry-run PRs (outside paths, oversize files, self-review, a copied `metrics.json`, title injection, a workflow edit, a nested `AGENTS.md`, `conftest.py`, a base64 token, a PR to `state`, a push after admission); smoke on 5 legacy worlds; the queue simulation; tests of fine-grained tokens, `refs/pull` lag, Codex networking and interaction limits; a second maintainer named. Then 2–3 invitees, reviewing legacy claims only in week one; then claims, scouts, canaries and eval slots.

## 11. Link to PhySim evaluations

Each world's `eval_status` moves through **candidate → declared → curated → accepted → exported**.

- **Candidate:** established and audited; 2 or more capabilities besides S; allowlisted imports; deterministic in smoke; about 10 ms per step or less at 128². Opens `EV:` slots.
- **Declared:** a LABWORLDS declaration (fields, grid, `dx`, dt, per-field noise in world units, ports with sign, gain and clip, ablations as knobs, prepared state, score groups).
- **Curated:** community work with labkit 0.4 alone: two independent results that the behaviour persists and trends smoothly under 1.5–2x refinement in space and time, shows no grid effect under a 45° rotation, and has noise in world units. The steward adds the numerics penalty against the smallest control separation.
- **Accepted:** the steward runs on Prime: runner parity; an envelope at amp 3 for 50 tu; nonzero spread; every mechanism and naive control beyond the native-vs-native band; declared noise; a dt-halved null; and a **leak control**: the public world at published settings plus a parameter sweep, predicting the private variant, must not beat the naive control.
- **Exported:** after a human maintainer reads the code, a maintainer PR adds `exports/<world-id>.json` (claim, commit, declaration hash, curation and acceptance ids, PhySim PR, `private_variant_sha256`, credits, licences). The community cannot self-certify; the grader sandboxes world code.

World code is public, so scoring uses a private variant (overrides, prepared seeds, hidden ablations, truths), published as a hash. **Correction to the proposals:** swpo/physim is public, so this cannot stay "private in physim"; variants, truths and the vortex suite now being built go to a private repo, not operator storage.

The first candidates are the fed vortices, phase_membrane (with flags), and CIPS with the isotropic stencil.

## 12. Open questions

1. physim's history keeps `labeval.py`'s frozen suite and truths, so moving them unpublishes nothing. Regenerate the truths?
2. Organization name: `alife-challenge`, if free? Who is the second maintainer?
3. Unaudited legacy large claims start headline P below 122. Accept, or grandfather them?
4. A pilot will not reach 30 canary reviews a month. Is about 1 canary in 10 claims still right?
5. Is a machine account per invitee acceptable friction? Should `group` come from GitHub organizations?
6. Is about 10 Prime CPU-h a day for checks and audits, plus tens per acceptance battery, acceptable?
7. Should a pinned skeptic's Contradicted count for more than 2? What scout target after week one?

## Appendix: Critique responses

2.7 means critique 2, point 7. Every other point was applied, some condensed.

- 1.7, 2.1 (a drand round; the `state` commit at grant): the squash-merge SHA (3.3) is as unknown to the author, and re-derivable from `main`.
- 1.10 (an App from day one): deferred; 3.10's reductions suffice for a pilot, and the App key would be the only secret.
- 1.12 (reveals as governance PRs): reveals are role-restricted contributions, so the lead need not approve each.
- 2.2 (reference hashes per granted seed): smoke's 40 daily jobs (1.15) cannot run a world per review; sampled spot checks give the same proof.
- 2.3 (ban `os.environ` and file I/O): 365 of 426 legacy worlds read `WORLD_P`, so parameters go through `labkit.params()` and sibling files are declared instead.
- 2.4 (a container by default): most sandboxes lack Docker (1.1), so the default is the strongest isolation available, and skipping it takes `--unsafe-host`.
- 2.8 (a monthly Merkle root): weekly (1.8, 3.8), so canaries need not be planned a month ahead.
- 3.1 (354 of 415 worlds read `WORLD_P`): the lab branch shows 365 of 426; the fix stands.
- 3.9 (the gate sweeps all open PRs): the librarian, the only lease writer (1.5), sweeps instead.
