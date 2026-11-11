# foundrylong: the long-horizon hidden-weights exam. Declared before any GPU request

Round 6, 11 Nov 2026. Written and committed before the first request of this study. Later changes go to
`DEVIATIONS.md`, never into this file. Form: `../dials/PLAN.md`, sections 2 and 3.

**PILOT ONLY.** Every world, weight, Lab episode and item of this study is a public function of public seeds or is
written to public outputs. Nothing here may ever be reused as an exam.

## 1. Question

The pilot `../foundryexam` found one setting where the no-hypothesis recipe falls short: the screened prior (arm P),
queries at 16 ticks, at most 32 Lab episodes (sigma 0.31 [0.25, 0.38] at 32 episodes against a 16,384-episode
reference). Its checker left three doubts: the null there was an untuned single-seed fine-tune; P0 was not saturated
in prior worlds (64 to 210 worlds: +0.061 to +0.065 of skill at 16 ticks); no policy held a hypothesis that worked.
Stage 1 asks whether the gap is only the recipe's compute. Stage 2, run only if stage 1 leaves the gap open, asks
whether a hypothesis (the 250 weights, fitted through the simulator) closes it and whether experiments pay.

## 2. The studies

### Stage 1. Is the gap only the recipe's compute?

**Exam.** The foundry's two-kind transport automaton (`../../round5/foundry/tnca.py`, 64 x 64, float64), all 250
numbers hidden, observed in the block view (192 numbers). An item is 17 observed frames (ticks 0 to 16 after a
burn-in of 300, no input) plus a public 32-tick test program from the pilot's mix (none, blind 200 nats, aimed 200,
regional 400; commands in the first 4 test ticks; equal shares); the answer is the block view 8, 16 and 32 ticks
ahead. The pilot's queries at 1, 2 and 4 ticks are dropped. Score: fair energy score with the RMS norm, coordinates
divided by the hidden world's climatological SD per channel, one score per item and query. A Lab episode is
exam-shaped (16 free ticks, then 32 ticks under a mix program, 49 frames; caps 100 nats per tick, 400 per episode).

**What is reused from the pilot, exactly.** (i) The 16 hidden worlds of arm P (labels in
`inputs/pilot_worlds.json`, copied from `origin/gpu-jobs:jobs/r6-foundryexam-005/out/full/P/worlds.json`; each is
`tnca.draw_theta(2027, index)`). (ii) The pilot's 210 training worlds of P0, in the pilot's order (same file), so
P0 on 64 worlds is the pilot's subset. (iii) The public code standardisation of the net's 33 window statistics
(`inputs/code_norm.json`, from job 005). (iv) The family, the gate, the program mix, the nats caps, the net family
and its inputs, the ridge, the scorer, by import of `../foundryexam/fx_lib.py` and `fx_net.py` with the episode
constants set to H = 32 and horizons (8, 16, 32). **Not reused:** items, Labs and the noise secret. The pilot's
items end at 16 ticks, their replicate futures were not written and its secret was never kept, so every item, Lab
episode and training simulation here is new. The training driver is new (below).

**New prior worlds.** P0 on 1,000 worlds needs about 790 more draws of the screened prior. They are made the way
the hidden worlds were: prior seed 2028, pool indices 0 to 159,999; round 5's weights-only pre-screen with the
model and the score threshold of the seed-2027 enriched arm (`make_sel.py`, which first reproduces the seed-2027
selection; CPU, committed list `inputs/sel_2028.json`); the screen of `../../round5/foundry/job2.py` at its sizes
(6 members x 290 ticks plus 8 test states) and the four gates of `criteria.py`; the pilot's exam-time gate (8 free
episodes at burn-in 300, cv_cell >= 0.25, vp(1) <= 1.0, vp(16) >= 0.2 on the 33-frame window). The training worlds
of P0(1,000) are the pilot's 210 followed by the first 790 new worlds that pass, in index order. If fewer than 590
new worlds pass (P0 on fewer than 800), that is a deviation and is reported; the curve is then read at the number
reached.

**One change of episode shape that matters.** With 49-frame episodes a 16-tick prediction has 17 anchors per
episode where the pilot's 33-frame episodes had one, for every policy alike, the Lab-based ones included. A Lab
budget of 32 episodes here is therefore more 16-tick data than the pilot's 32. The pilot's cell cannot be repeated
like for like in an exam whose queries reach 32 ticks; sigma is defined within this design, and the 32-tick query
is the one that sits in the pilot's regime (one anchor per episode).

| policy | what it is |
|---|---|
| K, Kp, O | climatology pool of the hidden world (96 runs); persistence; the simulator from the hidden state (leave one out over 12 replicate futures) |
| C(n) | the net trained from scratch on n simulated mix episodes at the true weights; n = 1,024, 4,096, 16,384 (nested). 16,384 is what the budget allows: 16 worlds x 16,384 episodes x 348 ticks = 91 million member-ticks, about a quarter of the job; a stack of 8 nets' data is 1.23e9 elements, 16 would pass 2^31. The reference C at a horizon is the n with the lowest pooled loss at that horizon on the unscored half of the items |
| P0(w) | the net trained on 64 mix episodes of each of w prior worlds, w = 64, 210, 1,000 (nested); reads each item's own history; no hypothesis, no experiment |
| P0x2 | P0(1,000) with twice the schedule, one seed: what doubling the recipe's training steps gives |
| FT(N) | P0(1,000) fine-tuned on N Lab episodes, tuned per hidden world, seed and horizon by 4-fold cross-validation over the Lab episodes: constant rate from {5e-5, 2e-4, 8e-4}, steps from {0, 50, ..., 400} (0 = P0 itself), the pair with the lowest mean held-out fair energy score at that horizon; then one run on all N episodes at that rate, stopped at that step |
| D(N) | the same net trained on N Lab episodes alone (a tenth of the episodes, at least one, held out for the best step; 400 steps at N = 8, 800 at N = 32) |
| Dr(N) | the pilot's local ridge on N Lab episodes, one model per horizon |
| plug-ins | from the hidden state: true weights (check on O), true weights without the test program (input-blind oracle), another screened world's weights |

Lab budgets N = 8 and 32 (nested prefixes of one Lab of 32 mix episodes per hidden world). Not run: the pilot's
amortised S (it added nothing) and P0s.

**Training driver (new, the same for every net).** The net, its inputs, the loss and the optimiser are the
pilot's. Three declared changes: (1) examples are drawn with equal weight per horizon (the pilot drew uniformly
over episode, anchor and horizon, which at 49 frames would give the three horizons 25 : 17 : 1); (2) the held-out
loss is computed per horizon and the best parameters are kept per horizon, and a query at horizon h is answered by
the parameters that were best for h; (3) the rate schedule is the pilot's warm-up and cosine to a tenth, run over
the first 75% of the steps and then held, so that the last quarter shows whether more steps at the final rate
still help. Fine-tuning runs at a constant rate.

| size | value |
|---|---|
| hidden worlds | 16 (the pilot's) |
| per hidden world | Lab of 32 mix episodes; 96 items x 12 replicate futures, 24 samples per policy and item; items with an even index are scored, odd ones are the unscored half used for every pick |
| seeds | P0(64), P0(210), P0(1,000): 3 each; FT(N), D(N): 3 each (FT seed s starts from P0(1,000) seed s and has its own cross-validation); C(16,384): 2; C(4,096), C(1,024), P0x2: 1 |
| steps, batch | P0(64) 6,000, P0(210) 16,000, P0(1,000) 40,000, P0x2 80,000, batch 256; C(16,384) 16,000, C(4,096) 8,000, C(1,024) 4,000, batch 128; Lab nets batch 64 |
| simulation | screen of about 15,000 pre-screened draws (49 million member-ticks); gate; P0's 1,000 worlds x 64 episodes (22 million); C (91 million); hidden worlds (about 9 million) |
| GPU job | one, A100 40 GB, expected 2.2 to 2.6 h, about $4.5 to $5.5; its own clock stops new work at 2.75 h; max_hours 3.0 |

**Order under the clock** (cut from the end): screen and gate; training simulations; hidden worlds, ridge; P0(1,000);
C(16,384) seed 0; FT(32), FT(8); D; C(16,384) seed 1; C(4,096); P0(210); P0(64); C(1,024); P0x2.

**Quantities.** L(policy, h) is the mean fair energy score at query h over the scored items of the worlds in the
analysis set, averaged over the policy's seeds.
sigma(h, N) = (L(null) - L(C)) / (L(K) - L(C)), null = the candidate among P0(1,000), FT(N), D(N), Dr(N) with the
lowest pooled loss at h on the unscored half, picked once for the analysis set.
Bounds: 4,000 resamples; hidden worlds resampled as clusters, one training seed drawn per trained policy in each
resample (P0 of 3, FT of 3, D of 3, C of 2); the one-sided 90% lower bound is the 10th percentile, the upper bound
the 90th. Every bound is computed with all 16 worlds and with each world left out in turn (pick, estimate and
resamples redone on the 15). Medians over worlds and leave-one-world-out ranges are printed beside every mean.

| criterion, declared now | number |
|---|---|
| S1, the gap at 16 ticks and 32 Lab episodes | **SURVIVES** if the one-sided 90% lower bound of sigma(16, 32) is >= 0.15 with all 16 worlds and with each world left out; **CLOSED** if the upper bound is < 0.15 with all 16 worlds and with each world left out; otherwise **UNDECIDED** |
| S1a, robust to one more step of compute (a reading, not the verdict) | SURVIVES is "robust" if the lower bound stays >= 0.15 after subtracting from sigma the gain of the last step in prior worlds, (L(P0(210)) - L(P0(1,000))) / (L(K) - L(C)), and the gain of doubling the schedule, (L(P0(1,000) seed 0) - L(P0x2)) / (L(K) - L(C)) if positive, both at 16 ticks on the scored half. CLOSED is "robust" if the upper bound stays < 0.15 after adding (L(C(4,096)) - L(C(16,384))) / (L(K) - L(C)), the gain of the reference's last fourfold step in data. Otherwise the verdict carries the words "at this compute" |
| S2, training rule | a net counts as trained at a horizon only if its best held-out step for that horizon falls in the first 80% of its schedule; for FT, only if the chosen step is below 400. The schedule is not doubled in this job (doubling P0(1,000) and C would cost about $2); nets that miss the rule are listed, their policy is then a lower bound of what the recipe reaches (C: of the ceiling), and the gain of the held-out loss over the last fifth of the schedule is printed beside the flag. P0x2 measures the doubling for P0 |
| S3, the trend in prior worlds | s0(w) = (L(P0(w)) - L(C)) / (L(K) - L(C)) at 8, 16 and 32 ticks for w = 64, 210, 1,000, with paired bounds for both steps. "Still falling" if the step 210 to 1,000 lowers s0(16) by more than 2 SE; "flat" if its 90% interval lies within +-0.02 |
| S4, the reference's data curve | skill of C(1,024), C(4,096), C(16,384) per horizon with paired steps; C is "not converged in data" at a horizon if the last step gains more than 0.01 of skill there (the pilot's rule) |
| S5, actions | on items with a program, (L(input-blind oracle) - L(O)) / (L(K) - L(O)) per horizon and class; "actions matter" at 0.10 or more (the pilot's criterion 4) |
| reported without a verdict | sigma(h, N) for h = 8, 32 and N = 8, with the same bounds; sigma with no Lab; each candidate's share; the cross-validation's choices; per-world values |
| stage 2 runs | if S1 is SURVIVES, or UNDECIDED with a point estimate of sigma(16, 32) >= 0.15. Otherwise the study stops and reports |

### Stage 2. Can a hypothesis close the gap, and do experiments pay? (only if stage 1 says so)

**Exam.** Stage 1's, on the same 16 hidden worlds with new items and Labs (new secret). P0(1,000) and C(16,384)
seed 0 are stage 1's own parameters, read from its public outputs and scored again on the new items.

| policy | what it is |
|---|---|
| G*(N) | the best generic recipe: stage 1's null candidates, picked on the unscored half |
| W(N) | the hypothesis is the 250 numbers. They are fitted by gradient through the family's differentiable simulator to N Lab episodes in the block view, from several starts drawn from the screened prior (training worlds), the start with the lowest fit loss kept. The hidden state is not observed: it is marginalised by an ensemble of the candidate world's own states, held to the observed block means of both kinds at every observed tick, and the fit loss is the fair energy score of the ensemble's short forecasts against the next observed frames. Prediction: the same assimilation over the item's 17 frames at the fitted weights, then simulation under the item's program |
| W+(N) | W's fitted weights, then simulate-to-train: the net trained on simulated episodes at the fitted weights (what C does at the true ones) |
| W(true), W(prior) | the W predictor at the true weights (the ceiling of the pipeline, designer side) and at another screened world's weights |
| mix / designed | each Lab-using policy (W, W+, FT, D, Dr) on N exam-mix episodes and on N designed episodes of the same nats caps: programs that spend the episode cap over all 32 test ticks (regional push of 12.5 nats per tick on the 3 x 3 blocks around the densest block, and an aimed push on the densest block, alternating, directions on a fixed 8-point compass by episode index). The rule is fixed in `DEVIATIONS.md` (dated addendum) before the stage-2 request and uses nothing of the hidden world |

Criteria, declared now, at 16 ticks with N = 32 mix episodes unless stated (same bounds and resampling as stage 1;
fit starts are resampled like training seeds):

| criterion | number |
|---|---|
| T1, science share against the best generic recipe | sigma_G = (L(G*) - L(C)) / (L(K) - L(C)): pass if the one-sided 90% lower bound is >= 0.15, fail if the upper bound is < 0.15 |
| T2, generic share | rho_G = (L(P0) - L(G*)) / (L(P0) - L(C)) <= 0.7, tested the same way; read only if L(P0) - L(C) exceeds 2 SE |
| T3, solvable | W* = the better of W and W+ (picked on the unscored half) recovers at least 0.7 of the gap from G* to C, (L(G*) - L(W*)) / (L(G*) - L(C)) >= 0.7 at the point estimate, and beats G* at t >= 3 over the 16 worlds (paired) |
| T4, experiments pay | L(W*, mix) - L(W*, designed) exceeds 2 SE (paired over worlds), and exceeds L(G*, mix) - L(G*, designed) at the point estimate (their difference is reported with its SE) |
| T5, actions matter | S5 of stage 1 on the new items, at 0.10 or more |
| T6, not one horizon and not one world | T1 and T3 hold at the point estimate at 8 and at 32 ticks, and at 16 ticks with each world left out |
| **pass** | T1 to T6 |
| **fail** | T1 fails, or T2's lower bound is above 0.7 |
| **undecided** | anything else; reported as undecided, never as a pass |

Sizes, steps and the assimilation's details are fixed in a dated addendum before the stage-2 request, after CPU
tests of the fit on public worlds; the criteria above are not changed by it.

### Also, on CPU (no criterion)

For the next step of the program: the automaton's speed on 2 cores of this container in member-ticks per second
(64 x 64, float64 and float32) and the research and prediction budgets of the lead's decision 2 in full-episode
equivalents; the size on disk of an instance bundle (Lab episodes, items, replicate futures, climatology); which
reference rows a box cannot make and must be precomputed on a GPU.

## 3. What each outcome would mean

| outcome | what it decides |
|---|---|
| S1 SURVIVES, robust | At about five times the pilot's prior compute and with a tuned fine-tune, the generic recipes still leave 0.15 or more of the range at 16 ticks with 32 Lab episodes, and one more step of compute does not close it. The setting is a candidate for a test that is not trivially easy; stage 2 asks whether it is solvable. |
| S1 SURVIVES or UNDECIDED (point >= 0.15), "at this compute" | The gap is open at this compute and within one step of the bar. Stage 2 runs. An exam profile on this setting must state its research compute budget, because the bar moves with it. |
| S1 CLOSED, or UNDECIDED with a point estimate below 0.15 | The pilot's long-horizon gap was a limit of the recipe's compute, its tuning, or the one-anchor layout, not an opening for science. Stage 2 does not run. Hidden weights alone do not make a non-trivial test on this family at 16 ticks; what remains is the 32-tick query (reported) and the designs of decision 1. |
| S3 still falling at 1,000 worlds | P0 is not saturated; every share is a value at this compute. The cost of the recipe in screened worlds becomes the dial of the exam, and a compute-limited exam on this family is the design to price. |
| S4 not converged in data | C is a lower bound; sigma is a lower bound; a CLOSED verdict holds only if robust (S1a). |
| stage 2 passes | The first setting where a scripted hypothesis beats every generic recipe by the bar and designed experiments beat the mix. A pilot instance goes to rollouts with the budgets from the CPU part. |
| T1 passes, T3 fails | The gap is real but no scripted policy closes it: the exam may be hard for the wrong reason (the state, not the law). W(true) against C says which: if W(true) is below C the state inference is the limit. Not ready for rollouts as a test of science. |
| T3 passes, T4 fails | A hypothesis pays, experiments do not: the wind channel is too weak on screened worlds for designed programs to add information (the pilot's reading). An agent must infer, not experiment. |
| T1 fails in stage 2 after stage 1 survived | The two jobs disagree on new items; the between-job spread is the result and no pass is recorded. |

## 4. Budget

Study cap $25 of GPU in at most three jobs: stage 1 about $5 (cap of the request about $8), stage 2 about $8 to $10
if it runs, a third job only for a declared follow-up. Job ids r6-foundrylong-001, 002, 003.
