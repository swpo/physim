# Round 6, study foundryexam: an exam pilot where the hidden law is a network's weights

DRAFT ON JOB 003 (the first full pass). Job 004 (the reference net trained to convergence, like-for-like prior
sizes in the neighbourhood arms) is running; its table replaces the one below when it is done. See PROGRESS.md.

**Question.** Round 5 found that with a correct public simulator and a few hidden parameters, a policy with no
hypothesis and no experiment (train on simulations of the public prior) takes nearly all the skill. Does that still
hold when the hidden part is the 250 numbers of the level-0 network itself and the public simulator is the family,
not the world?

**PILOT ONLY.** Every hidden world here is a public function of public seeds and its weights are written to public
outputs. These worlds, Labs and items must never be reused as an exam.

## Numbers of job 003 (to be replaced)

See `results/analysis_job003.json`, `results/fig_budget_job003.png`; tables by
`python -B tables.py --analysis results/analysis_job003.json`.

- Arm P (screened prior, 16 hidden worlds, 210 prior worlds for the no-experiment policy), pooled skill with
  climatology 0 and the oracle 1: C 0.744, P0 0.664, P0 fine-tuned on 512 Lab episodes 0.732, a net on 512 Lab
  episodes alone 0.710, a local ridge on 8 Lab episodes 0.640, amortised inference flat at 0.66.
  P0 takes 0.892 [0.866, 0.916] of C's skill; sigma 0.100 at 8 Lab episodes, 0.015 at 512.
- Arm N30 (eps 0.3): P0 takes 0.787 [0.705, 0.868] (24-32 prior worlds only). Arm N10 (eps 0.1): 0.953.
- C was not converged by criterion 6 (4 of 32 nets in arm P): C is a lower bound in job 003.
