# Adversary's critique of the three dial designs (round 6, crit_adversary)

11 Nov 2026. CPU only (23 CPU-minutes), no GPU, no model call. Measured: `sublevel_second/gvh.py`'s own check (state given, 64 px, 16 Lab episodes; pilot values, never to be reused as an exam). `R` = `results/summary.json` here. "Not run" marks argument.

**Verdict.** Two designers built my policy themselves and forecast failure; I agree. The third claims to resist generic repair, and on its own check resists at one horizon of four: up to 16 ticks its simplest recipe closes 0.8 of the gap; at 32 ticks nothing generic closes anything, mine included.

## 1. sublevel_second (measured)

`adv_sim.py` repeats `gvh.py` call for call and keeps every tick; on seeds 5 and 6 its L(pub), L(O), L(G2) equal the designer's files exactly, and H re-run on seed 6 gives the same 0.773. Added, knowing of no carrier, cells or saturation: **A_act** (`adv_act.py`), the public law under a linearly filtered command (direct gain, lagged gain, lag time, blur), four numbers fitted by least squares on the Lab: H's procedure with a generic actuator for the told form.

Share of the public-to-oracle gap closed (`R` [rows]; ± bootstrap over test members):

|seed|policy|4 ticks|8|16|32|pooled|
|---|---|---|---|---|---|---|
|5|G2, the designer's gain|0.91|0.87|0.66|-0.45|0.10 ± 0.17|
|5|A_act|0.88|0.82|0.69|0.06|0.38 ± 0.20|
|6|G2|0.81|0.94|0.77|-0.05|0.34 ± 0.10|
|6|A_act|0.92|0.90|0.84|0.06|0.42 ± 0.15|
|6|H, told the form|0.56|0.62|0.60|0.91|0.77 ± 0.08|
|7|G2|0.98|0.84|0.52|0.03|0.27 ± 0.17|
|8|G2|1.02|0.92|0.66|0.06|0.58 ± 0.10|

Seed 5 was my development seed; A_act was frozen before seed 6 ran and chose the same filter there from 4 Lab episodes (seed 5 needed 8). A response-mixing variant is worse (0.31, 0.08). Seeds 7 and 8 repeat the designer's runs only.

1. Table 3b's "generic closes 0.10-0.34" is the 32-tick horizon, which holds 0.31-0.67 of the gap; two seeds understated the spread (0.58 on seed 8). Up to 16 ticks G2 closes 0.76-0.84 and A_act 0.78-0.88; on seed 6, where H fitted lam = 0.5, G2 beats H there by 0.24 ± 0.04.
2. At 32 ticks I could not break it: on seed 6 H leads A_act by 0.85 ± 0.24. That gap sits in few cells: one test member of eight carries 55% of the whole gap on seed 5, 50% on seed 7. On seed 5 its focus mass goes from 386 to 64 without input, 214 under the public law, 470 under the hidden law.

**Gates.** Pooled over 8, 16 and 32 ticks, rho_G <= 0.7 survives my policy given the state (A_act 0.33, 0.36); it fails at 8 ticks alone and is marginal at 16. Gate 1's interval is in doubt: these shares carry ± 0.10-0.20 over 6 to 8 members, and the job has 12 truths.

**Changes.** (a) G2 and A_act into G*, each horizon gated: a pass is then a claim about 32 ticks. (b) The truth off H's grid. (c) The focus view sums the cells within 16 px, hiding which cell the carrier fed, which no gain can express: score the cell-resolved list (not run). (d) Stage 1 first: does a history-only C keep the 32-tick gap?

## 2. defect_gliders

My policy is the designer's RES at n = 1: one Lab episode per triggered class closes 0.94 ± 0.08 (aimed) and 0.70 ± 0.03 (regional), two close 1.46 and 0.93 (`defect_gliders/results/surrogate.json` [rows.generic_residual]). Bars 2 and 3 fail; bar 4 too if nets behave like the surrogate. Bar 1 would pass only because its null omits RES.

It is this cheap because the mix's two triggered classes have fixed dose and footprint (`track2/gliders_exam/pilot.py`, `C_AIM`, `C_REG`): the Lab's mix episodes are the exam's conditions. The term is also a memoryless function of |E|, which the public simulator computes, so a residual on that field would carry to other doses (not run): a wider mix or transfer items only raise n.

Change: none rescues XW. Run stage 1 as the calibration that puts RES in every null. A (b) exam on gliders needs a correction that depends on hidden state inferred from history, not on a public field.

## 3. compute_limit

Again the designer's policy: pooled small boxes. At r = 1/4 pooled regression scores 0.448 ± 0.023 against 0.454 ± 0.021 at exam size; a per-tick mean of pooled boxes, no model, 0.359 (`compute_limit/results/summary.json` [transfer_128.skill.all]: `ridge64pool4`, `ridge128_loo`, `Ktick64pool4`). Bar 3 fails: sigma_c is 0.013 if the exam-size regression stands for C. At r = 1/16 bar 4 fails (`law32pool16` 0.004, `ridge32pool16` 0.287).

Two more routes, not run:
- Full-history items show 130 to 370 ticks of the true world at exam size (`round5/vortexexam/README.md`, "Exam shape"); two exam-size episodes lift the designer's rescaled regression from 0.359 to 0.434. Recalibrating on each item's own history would defeat r.
- Level-1 nets pool by mosaic: the vortex lists of k boxes joined with tile offsets. That removes the risk the stop-rule job tests.

Change: none on this world; I would not spend the $5. On the card, report the pooling defect after 1/area extrapolation.

## 4. For the program

Every (b) and (c) null needs RES, A_act and pooled boxes. Screen by the state-given gap that generic repair leaves, per horizon.
