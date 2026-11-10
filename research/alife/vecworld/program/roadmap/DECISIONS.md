# Decisions on the roadmap

The lead's answers to the decisions of `ROADMAP.md` section 6, taken one at a time on 9 and 10 Nov 2026. The numbering is the
order in which they were put to the lead; the roadmap's own number is in brackets. Quotes are the lead's words.

| # | question | status | decision |
|---|---|---|---|
| 1 [1] | what may be hidden | decided 9 Nov | (a) stays the default; (b) and (c) are subjects of study |
| 2 [2] | the agent's compute | decided 9 Nov | a compute budget relative to the cost of the full simulation, not a hardware class |
| 3 [4] | rollouts with real agents | decided 9 Nov | cleared to spend; a cheap model first for mechanics, then Astra |
| 4 [7] | the same model on v1 and v2 fed vortices | decided 9 Nov | not a priority now; not scheduled |
| 5 [6] | where sealed answers live, and who grades | decided 10 Nov | a private Hugging Face dataset repo, not the lead's Mac; the grader must build on the verifiers library, not reinvent it |
| 6 [5, 6] | the collective pilot and the large foundry pass | decided 10 Nov | both wait; a collective, if run, is run from the coordinator's session with Claude sessions as agents |

Roadmap decision 3 (the acceptance definition) was not put separately. The two quantities of roadmap section 1
(science share sigma, scripted share rho) are in use as provisional and are to be recalibrated on the first agent table.

## 1. What may be hidden

"Yes I like b and c as subjects of study with a being the default. Both b and c seem to be true in the natural world."

- (a) Hidden parameters of a correct public law: the default exam design.
- (b) A public law that is incomplete by a measured defect (an extra term or a hidden finer level): a subject of study.
  The agent is told that its simulator is approximate; where and how it is wrong stays hidden. At zero defect the design
  must reproduce (a).
- (c) A correct law too expensive to run at exam scale: a subject of study. Under decision 2 this is a setting of the
  compute budget, not a separate kind of exam.
- (d) No simulator: kept as a comparison arm (coordinator's proposal; not objected to).

This widens the hidden set in `../README.md` (level-0 weights, noise secret, exam instances) for designs of type (b) only.

## 2. The agent's compute

"I think cpu vs gpu is the wrong way to think about it. Better to think in terms of the compute budget for rollouts
which we can control and even tune in relation to the expected 'full' simulation time."

Each exam declares its compute budget in units of the cost of fully simulating that world, and the budget is a dial.
The coordinator's reading, stated back to the lead and not objected to, is two numbers per exam, both told to the agent:

- research budget: total compute while the agent investigates, in full level-0 episode equivalents. On the gliders
  pilot the prior-simulation policy P0 uses about 2,300 and the scripted inference recipe about 20,000.
- prediction budget: compute the submitted predictor may use per exam question, as a fraction of fully simulating that
  question. Below 1 the predictor cannot answer by brute force.

Hardware is only how the budget is delivered. Enforcement is a cap on the sandbox's total compute, calibrated against
the simulator's measured speed on that hardware; metering simulator calls alone is not enough, because the agent can
rewrite the simulator.

## 3. Rollouts with real agents

"Yeah that makes sense to do at some point. Exactly when I leave to you. You're clear to spend on the rollouts. I'd run
a cheap qwen or something first to confirm it works mechanically then move to Astra to test how a better agent rollout
looks and if there are leaks or issues or hacking opportunities."

- Timing is the coordinator's. The precondition is that the agent environment (`../round5/agentenv`) passes its
  scripted end-to-end test and its checker.
- Order: a cheap model (Qwen) to prove the mechanics, then Astra.
- The Astra transcripts are read for leaks, shortcuts and ways to game the exam, not only for the score.
- The lead named Astra only. A second model, needed before any exam can be said to order two models, is not chosen.

## 4. The same model on v1 and v2 fed vortices

"Regarding the Astra comparison of the two versions I don't think this is a priority at the moment"

Not scheduled. The four fed-vortex rollouts in roadmap section 4 (workstream A, by 21 Dec) are dropped from the plan
until the lead asks for them. The v2 fed-vortex exam pilot (`../round5/vortexexam`) continues on its own merits as an
exam candidate; it no longer has to match the v1 suite's items.

## 5. Where sealed answers live, and who grades

"Can we use huggingface to store this stuff not on my laptop ?" and then: "Hf approach is good. For the grader Make
sure to take a look at primes verifiers library we're using and make sure we're not reinventing an isolated grader"

- Store: one private Hugging Face dataset repo holds hidden parameters, exam answers and reference runs. The public
  exam package and salted hashes of the answers stay in this repo. Retiring an exam means publishing its files, which
  anyone can check against the hash.
- Access: two tokens scoped to that one repo, one that can write (sealing) and one read-only (grading). The sandbox
  in which an agent takes the exam gets neither. Tokens are entered through a secure form or set on the Mac by the
  lead, never pasted into a chat or committed.
- No token goes to a GPU pod (the Mac runner's standing rule from the lead: Prime credentials, the Hugging Face token
  and the SSH key stay on the Mac). Design agreed with the Mac runner on 10 Nov, replacing the coordinator's first
  wording that pods would upload directly: a sealed job declares `"sealed_outputs": true` and writes its answers to a
  private directory `$SEALED`, separate from `$OUT`; the runner collects `$SEALED` but never publishes it to the
  public `gpu-jobs` branch (the manifest carries counts and hashes only); the Mac uploads it to the private repo with
  its local token and publishes the commit hash and file hashes. The local copy is deleted once the upload is
  verified against the hashes, so exam data passes through the laptop but does not stay there. Until the runner has
  this, anything a job writes to `$OUT` is public: no sealed answers in `$OUT`.
- Grader: not to be designed from scratch. The verifiers library (the version the PhySim v1 environment pins) is read
  first for what it already provides; the result is `GRADER_VS_VERIFIERS.md` in this folder. `../round5/agentenv`
  (written before this decision, with its own orchestration and sandbox) is revised in its light before any rollout
  that is to be quoted.
- Not needed for the Qwen mechanics check or the first Astra look, which use pilot worlds that are never reused.
- Still needed from the lead when it is built: the private repo under an account or organisation of the lead's choice,
  and the two tokens.

## 6. The collective pilot and the large foundry pass

"Yeah let's wait on it. If we run a collective we'll do it from here (you'll run Claude sessions as agents)."

- Both wait: the agent collective pilot (roadmap estimate about $2,150) and the large neural-CA foundry pass
  ($150-300 of GPU). The trigger proposed to the lead, and not objected to, is that one exam has ordered two models.
- If a collective is run, the coordinator runs it from its own session, with Claude sessions as the agents (as the
  ALife collective and this program's rounds were run). The roadmap's cost estimate for the pilot assumed otherwise
  and is to be redone on that basis before the pilot is proposed again.
- The small foundry screen of round 5 (`../round5/foundry`, cap $25) is not affected.

## Earlier standing decisions that bear on the roadmap

- GPU spending up to $1,000 in total is approved (7 Nov); jobs with a cap of $25 or less start without asking
  (`../gpu/LEDGER.md`).
- The PhySim v1 energy-score estimator stays as it is for now (8 Nov, relayed through the Mac session): "I think plugin
  might be fine for now", and the v2 work "would not depend heavily on any of this". v2 scoring uses `vw/scoring.py`.
