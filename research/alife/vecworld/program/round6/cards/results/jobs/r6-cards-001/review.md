# Review of r6-cards-001 (study `cards`)

Reviewed by the runner Mac while the job ran. The code is the eleven request paths at c6ea6942.

Method:
- four reviewers, one each for GPU memory, time and deadlines, outputs and hygiene, and correctness;
- each minor-or-worse finding re-checked by independent skeptics: two for a major, one for a minor;
- estimates are from the code's shapes plus measured float64 rates of earlier round-5 jobs on A100 40GB (vortexexam, bias2, foundry);
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 6 minor.** Two of the minor findings are about estimators behind pre-registered gates and should be settled before the cards are read (items 1 and 2). One can be corrected offline from the saved cards; the other cannot.

## Checked

- **Memory.** A device batch is state_batch x 30 arms: gliders 240; vortex64, foundry64 and the controls 960; vortex128, membrane and foundry128 480.
  - Every group peaks at about 5 GB or less on the A100 40GB. The largest is the gliders branch at about 3-5 GB: its FFT phase about 2.5 GB, its reintegration scatter phase about 2.6-3.8 GB, plus cuFFT workspace.
  - Cross-checks: r5-foundry-001's compiled gliders cost, 9.2 MiB per member, gives about 2.4 GiB at 240. The r5-vortexexam bench gives 2.8 GB for vortex128 at 480.
  - No int32 overflow: the largest index array is 0.13 of 2^31.
- **Time.** By group, from measured A100 float64 rates:
  - vortex64 runs 264 s in all;
  - vortex128 about 250 s;
  - gliders 190 s for 3 runs (measured 617-734 member-ticks/s, not the notes' 1,200);
  - foundry64 10-40 min over 103 runs (overhead-bound);
  - foundry128 2-8 min;
  - compiles 4-12 min.

  Total: 31-78 min, central about 46 min, against the last run start at 95 min (5,700 s, counted after setup). The run started just before 5,700 s still has about 24 min before the kill, against a longest post-presmoke run of 2-3 min. Priority-1 runs would need a 2x slowdown to be skipped. The presmoke may take up to about 22 min, not 10-15.
- **Outputs and exit codes.**
  - Each card and series file is written as soon as its run ends, and job_state.json is replaced atomically after every run, so a kill keeps every finished card.
  - Exit codes as promised: 0 all done; 1 any failure or a skipped priority-1 run; 2 a presmoke group of priority 1-3 failed; 3 not on the GPU (checked before anything compiles).
- **Hygiene.** No network or subprocess use outside setup, and nothing hidden-but-secret is written. progress.txt carries the pilot marker, after a timestamp.
- **Correctness.**
  - Held-out states are held out from the closed-form fits. RNG streams are independent where independence is assumed.
  - The 30 branch arms are built as described: 6 oracle replicas, 12 hidden-part neighbours, 8 input arms and 4 response-difference arms.
  - No shape, dtype, chunking or recompile defect on the paths only the full size runs. The 128-px programs have still not been run end to end anywhere.

## Minor

1. **The tick share pools every channel before the covariance, so the `stationary` gate is too lenient and H6 is refuted almost by construction.** cardlib.py:378-388 averages each member half over members and over every channel (and every block at the grid level), then takes the covariance of those two scalars per tick.
   - If one of d standardised components carries a tick function with share s, the pooled estimate is about s/d^2, not s/d.
   - At the population level (d = 6 live components), even s = 1 reads as about 0.028, below the 0.1 bar in HYPOTHESES.md:105-106.
   - Nothing is lost: the per-channel values (tick_share_q) are in every card.
   - Fix offline, before reading H6: make gates.derive and make_cards use the mean of the per-channel shares. Correct cardlib for the next run, and add a check_cardlib case with one trending channel.
2. **The response-difference estimator is biased low** (cardlib.py:466). It subtracts var(d) + var(d') as if the two responses had independent noise, but the arms share noise. E[RD] is the squared mean difference minus the cross-covariance of d and d', so RD, and xresp = RD(4)/V_orc(4) (gates.py:130), are pushed down, possibly below 0.
   - This matters on the box-prior worlds (gliders, vortex, membrane), where the neighbour move is moderate. For foundry, the neighbour is an independent weight draw and the bias is near zero.
   - **It cannot be recomputed from the card.** Treat H2's "response difference at least the oracle variance" as a lower bound for the box-prior worlds in this run.
   - Fix: use the variance of the per-replica difference d' - d, averaged and divided by R_u. Add a check_cardlib case where d varies with the replica.
3. **$OUT is about 35 MB, not about 9 MB.** The series npz files are not small. The realistic total is about 28-43 MB and the raw upper bound about 51 MB, against the 50 MB git cap.
   - Anything past the cap stays on the Mac, marked in_git false in the manifest. fetch.sh reads only the gpu-jobs branch, and make_cards globs whatever exists, so missing runs would drop out of the tables without an error.
   - Next time: store the population series as float16 or every second tick, drop tracks_member0 for the size checks, or stop writing series past about 40 MB.
   - For this run: check manifest.json for in_git false entries before building tables. Ask the Mac for any that stayed here.
4. **Each card records whether its run stayed finite, but nothing reads it** (gates.py:205; computed at cardlib.py:231). A world that blows up on the GPU over the full window, which the CPU test never ran at full length, would read as "dull". For a control, dull is the expected verdict.
   - Fix: when finite is false, set the verdict to "invalid: non-finite", count the run as failed, and print finite in the log line. make_cards should refuse such cards.
   - For this run: filter on card["finite"] when building tables.
5. **The diffusion controls keep the mobility gain gam** (adapters.py:138-143). diffusion_theta copies a full prior draw and overrides only beta and kappa. The leave rate then still depends on local density through the hidden net, so these are not round 5's diffusion controls, and a draw with strong negative density dependence could cluster.
   - Fix: one line, gam = 0.0 in diffusion_theta. Otherwise rename the control in HYPOTHESES.
6. **The size-robustness check compares quantities that scale with area,** and, for vortices, different block scales (make_cards.py:27, 338-342).
   - At 128 px a box has about 4x the bodies and events. The fixed 200-nat input spreads to half the push per block, so D and MS fall by about 4x for a linear response.
   - The vortex grid compares 8-px with 16-px blocks.
   - s.nb_mean, s.events100, grid.act_ms and the vortex grid entries therefore fail by construction.
   - Fix offline in make_cards: compare densities per area, scale act_ms by the input density, or drop these keys from the check.

## Notes

- The cost entries (make_cards.py:301, 377) say "compile excluded", but for vortex128 and foundry128 they include the compile: these groups' only run is their first call. That gives a spurious cost jump for the 128-px checks. Record the compile time separately, by compiling ahead of time with lower().compile(), or label the fallback.
- check_elems (cardlib.py:168-172, 281-283) checks only the output records, and counts elements, not bytes. It is an index-overflow guard, not a memory guard. It is harmless at these shapes (3% of its limit). For bigger requests, log each group's compiled memory figures in the presmoke instead.
- scipy is not in the install line, but import vw needs it (certificates.py:35). jax pulls it in transitively, so this run is fine. Pin it as in earlier jobs.
- "Quiet" body steps check events only at t and t+h, not in between (cardlib.py:678, 699-704). The skeptic found the consequence for the free-body control unsupported; the code does what its comment says.
- Two controls are dull essentially by construction, so their "dull" verdict tests little beyond the plumbing.
