# Decisions on the roadmap

The lead's answers to the decisions of `ROADMAP.md` section 6, taken one at a time from 9 Nov 2026. The numbering is the
order in which they were put to the lead; the roadmap's own number is in brackets. Quotes are the lead's words.

| # | question | status | decision |
|---|---|---|---|
| 1 [1] | what may be hidden | decided 9 Nov | (a) stays the default; (b) and (c) are subjects of study |
| 2 [2] | the agent's compute | decided 9 Nov | a compute budget relative to the cost of the full simulation, not a hardware class |
| 3 [4] | rollouts with real agents | decided 9 Nov | cleared to spend; a cheap model first for mechanics, then Astra |
| 4 [7] | the same model on v1 and v2 fed vortices | put 9 Nov, open | |
| 5 [6] | sealer and grader with a private store on the lead's Mac | not yet put | |
| 6 [5, 6] | defer the collective pilot and the large foundry pass | not yet put | |

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

## Earlier standing decisions that bear on the roadmap

- GPU spending up to $1,000 in total is approved (7 Nov); jobs with a cap of $25 or less start without asking
  (`../gpu/LEDGER.md`).
- The PhySim v1 energy-score estimator stays as it is for now (8 Nov, relayed through the Mac session): "I think plugin
  might be fine for now", and the v2 work "would not depend heavily on any of this". v2 scoring uses `vw/scoring.py`.
