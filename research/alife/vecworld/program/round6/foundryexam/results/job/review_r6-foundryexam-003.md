# Review of r6-foundryexam-003 (study `foundryexam`, rerun of 002)

Reviewed by the runner Mac as the job started. The code is the four request paths at 96d04d50.

Method:
- two reviewers: one checked the changes against r6-foundryexam-002 (0b7e392c), the other the run risk on the A100 40GB;
- each minor-or-worse finding re-checked by an independent skeptic;
- timings from 002's measured rates on this card: simulation 47,000 member-ticks/s, 11.5 s per hidden world, presmoke 6 min, nets about 70 ms per step of two shared nets;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 2 minor.** The changes do what the request and DESIGN.md 5b say.

## The changes, checked

- **50 steps per dispatch** (fx_net.py:340-346, 450-477). This is the same training as 002's per-step loop:
  - the optimizer state and step counter are carried through the scan;
  - every inner step of every net gets its own key (a fresh split per dispatch), so no batch or noise draw repeats;
  - the learning-rate schedule and per-step clipping are unchanged;
  - validation still runs at eval_every.

  A schedule or eval_every that is not a multiple of 50 raises a ValueError; every configured value divides. Deadlines are checked at each validation, so the worst overrun is about 250 steps.
- **Global inputs as per-channel shifts.** _conv pads periodically, so in 002 a constant channel through the 3 x 3 input convolution was exactly a per-output-channel shift. The new input form is the same function class, reparametrised. The extra learned shift in each block enlarges the class, and DESIGN.md 5b declares that.
  - The initialisation differs: local weights about 2.1x the old SD (fan-in 207 instead of 936), global weights about 0.8x.
- **Order and containment.**
  - The order is as declared: P0, A, P0s; C; D(512) and FT(512) seed 0; Cft; smaller budgets; second seeds; then P0[16] and P0[64].
  - Each net kind and each hidden world sits in its own try, and the survivors keep consistent indices throughout.
  - scores_refs.npz is written before any net, meta.json before the quick report, and info.json after the gate and after every arm.
  - The code norm leaves out arm-P hidden worlds.
  - The random context excludes the example's own episode, drawing uniformly over the others.
  - A net cut before 0.8 x its steps is not called converged.
  - make_summary keeps the null at budget 512 and flags it when incomplete.
- **Memory.** The scan keeps only a (nets, 50) loss array. The 16-net lockstep at batch 64 peaks near 5.1 GiB, below 002's 10.4 GiB.
- **Speed guard** (run_fx.py:576-594). It times only the dispatches after the first, compiling one: 150 steps, a stable figure. Its step counts per kind and arm are right.
- **Outputs.** About 22 MB; the largest file is full/P/items.npz at about 6.5 MB.
- **Exit codes as stated:** a guard failure gives exit 4, which job.sh turns into 2; any FAILED entry gives exit 1.

## Expected time on this card

| how much the scan helps | nets | job (job.sh clock) |
|---|---|---|
| fully (round-5 basis, 4.5-5.5 us per sample) | 0.53-0.64 h | about 1.2-1.3 h |
| half | 1.17 h | about 1.8 h |
| not at all (002's 27 us per sample) | 3.18 h | the guard stops it in the presmoke, about 0.15 h and $0.30 |

The narrower first convolution helps little; the speed-up depends almost entirely on the scan.

## Minor

1. **The speed guard lets through runs that the deadlines will then cut.**
   - It passes when the projected net time is at most 1.25 x the time available (run_fx.py:594).
   - It leaves out validation, which is about 8% of lockstep time: shape_test's 200 steps never validate.
   - Between about 2.0 and 2.65 h of projected net time it passes, and the arm deadlines then silently drop the tail, about 20-25% of the net work at the edge: the second seeds (criterion 8), P0[16] and P0[64], and the small-budget D(N)/FT(N) curves.
   - C, D(512), FT(512) and Cft finish in every arm even at the edge.
   - For this run: read presmoke/shape_test.json. If the projected net hours are above about 0.9 of the hours available, expect the tail to be cut, and read the skipped lists before the budget curves.
   - Next time: time one validation of each kind in shape_test and add it, compare against 1.0 x what the deadlines leave, and write the nets that would be cut into shape_test.json.
2. **If the first hidden world of an arm fails, a KeyError loses the whole arm.**
   - The progress log after each world (run_fx.py:352) reads CLOCK["hidden_s"], which is set only when a world succeeds (run_fx.py:277). It runs whenever len(HW) % 4 == 0, which includes 0.
   - So if world 0 of arm P raises, for example a LinAlgError in ridge_fit or a Lab input violation, the KeyError escapes the per-world try. Arm P is recorded as failed, with its references and worlds.json.
   - The chance is low, because the presmoke runs these stages on 3 worlds, but this is exactly the case the new containment is meant for.
   - Fix: use CLOCK.get("hidden_s", 0.0), or log only after a successful append.

## Notes

- C and Cft train seed 0 and seed 1 in one train_groups call, inside one try (run_fx.py:403-432). An error in the seed-1 group throws away the finished seed-0 nets too. If both C and Cft fail that way, the arm has no ceiling, and sigma and rho are undefined. This is unlikely, because the groups have identical shapes. A try per group would keep the finished one.
- The per-world nets now see 2-2.7x fewer examples.
  - C sees 4,000 x 64 = 256k examples where 002 planned 5,000 x 128 = 640k: about 3.4 epochs of its training set instead of 8.6.
  - Cft drops from 256k to 96k, D(512) from 384k to 192k.
  - The N-arm P0s steps go from 4,000 to 3,000 (run_fx.py:60-61). DESIGN.md 5b does not list this.

  An undertrained C raises L_C, which pushes share_noexp up, sigma down and rho up. Before quoting those, check C's and Cft's late_share and best_step in train_info.json, compare C with Cft, and read the stopped_early counts next to ok/nets.
