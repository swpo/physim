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
| 5b | where the port's first runs happen | decided 11 Nov (relayed) | smoke test on a rented Prime CPU machine first; model rollout on the Mac; no credential on a rented machine |
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
- Where evaluations run (10 Nov, after the verifiers memo): "Mac can run evals". The machine that runs `vf-eval`
  holds the read token and scores in its own process, so for sealed exams it is the lead's Mac. This replaces the
  coordinator's earlier wording that grading would run in a separate cloud environment. Exam data passes through the
  Mac during a run; its local cache is wiped afterwards, like the sealed outputs of GPU jobs.
- Uploading traces to Prime's platform (the verifiers default): "pilot traces can be uploaded if it buys us
  something". The coordinator's reading, to be applied run by run: no upload for scripted, model-free runs (nothing in
  them is worth a hosted viewer); upload allowed for pilot rollouts of real models, where it lets the lead read the
  transcript in Prime's viewer and keeps a copy off the laptop, after one saved trace has been read to confirm what an
  upload contains; never for a sealed exam (GRADER_VS_VERIFIERS.md, hole 6).
- Grader: not to be designed from scratch. The verifiers library (the version the PhySim v1 environment pins) is read
  first for what it already provides; the result is `GRADER_VS_VERIFIERS.md` in this folder. `../round5/agentenv`
  (written before this decision, with its own orchestration and sandbox) is revised in its light before any rollout
  that is to be quoted.
- Not needed for the Qwen mechanics check or the first Astra look, which use pilot worlds that are never reused.
- Still needed from the lead when it is built: the private repo under an account or organisation of the lead's choice,
  and the two tokens.

## 5b. Where the first runs of the verifiers port happen (11 Nov, relayed by the Mac session)

After three host-safety audit rounds had cleared the scripted smoke test for the Mac, the lead decided, in words
relayed by the Mac session: "Actually just use remote stuff from prime right? Why even go through all this intense
care if you can rent a cheap machine to do it? And then totally safe", and then: "Model run on Mac is fine I think.
Fair that we don't want to ship the credentials to the rented machine."

- The scripted, model-free smoke test (runbook steps 0 to 2) runs first on a rented Prime CPU machine through the Mac
  runner, as a cheap pre-check (`../round6/vfsmoke`). No credential goes to a rented machine.
- The model rollout (step 3) runs on the Mac, where the model key is. Steps 0 to 2 run there once, right before it,
  from a newly pinned commit that the Mac session reviews first, and after the lead has settled Docker Desktop's
  disk limit and the price.
- Lesson for the coordinator: the question "which machine" should have been put to the lead before the audit rounds,
  not after. The scripted test had already passed on Linux in the cloud container; only the model key ties anything
  to the Mac.

## 6. The collective pilot and the large foundry pass

"Yeah let's wait on it. If we run a collective we'll do it from here (you'll run Claude sessions as agents)."

- Both wait: the agent collective pilot (roadmap estimate about $2,150) and the large neural-CA foundry pass
  ($150-300 of GPU). The trigger proposed to the lead, and not objected to, is that one exam has ordered two models.
- If a collective is run, the coordinator runs it from its own session, with Claude sessions as the agents (as the
  ALife collective and this program's rounds were run). The roadmap's cost estimate for the pilot assumed otherwise
  and is to be redone on that basis before the pilot is proposed again.
- The small foundry screen of round 5 (`../round5/foundry`, cap $25) is not affected.

## Direction (the lead, 11 Nov 2026)

Said after the environment work had taken a day, so that it does not displace the research. In the lead's words:

- "We want to understand how the supervenient worlds behave when we run rollouts on them and how the scores of those
  rollouts look."
- "We ultimately want to create interesting supervenient worlds. And in order to do that, we need to have a sense of
  what interesting might look like from a more abstract perspective. For example, being able to look at the level 0,
  level 1, even higher level dynamics, have some claims that they're complex or worth studying for some reason."
- "But then, more concretely, we need to confirm that these things that look interesting lead to interesting
  rollouts, interesting modeling, or however the agents try to approach the problem. Ideally, tests that are not
  trivially easy for the agents."

The coordinator's working loop that follows from it (a reading, to be corrected by the lead):

1. A world card for every candidate world, computed by one tool and comparable across worlds: per level, how
   predictable it is over horizons, what structures exist and how they interact, which effective laws hold and where,
   whether a learned variable differs from the obvious one, whether actions matter, how much the hidden part changes
   the level given the state (the one screen that predicted the science share in round 5), and the cost per tick.
   The card is the claim that a world is worth studying.
2. An exam on the same harness for a few worlds that differ on the card, with the scripted reference policies
   (K, D, P0, S, C, O) and the two shares.
3. Rollouts of the same models on those exams. Each rollout is read for how the agent approached the problem
   (simulate, fit, hypothesise, experiment), where it lands among the reference policies, and how it spent its
   budgets, not only for its score. The scripted policies say what is easy for a recipe; only rollouts say what is
   easy for an agent.
4. Compare cards with rollouts: which features of a world went with rollouts that were not trivial and that
   separated agents. Generate the next worlds toward those features.

Environment and safety work serves step 3 and must not queue ahead of steps 1, 2 and 4.

## Earlier standing decisions that bear on the roadmap

- GPU spending up to $1,000 in total is approved (7 Nov); jobs with a cap of $25 or less start without asking
  (`../gpu/LEDGER.md`).
- The PhySim v1 energy-score estimator stays as it is for now (8 Nov, relayed through the Mac session): "I think plugin
  might be fine for now", and the v2 work "would not depend heavily on any of this". v2 scoring uses `vw/scoring.py`.
