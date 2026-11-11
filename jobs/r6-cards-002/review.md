# Review of r6-cards-002 (study `cards`, job 2)

Reviewed by the runner Mac while the job ran. The code is the eleven request paths at f87fa49c.

Method:
- two reviewers: one checked the fixes and the new code paths against r6-cards-001 (c6ea6942), the other the run risk on the A100 40GB;
- each minor-or-worse finding re-checked by independent skeptics: two for a major, one for a minor;
- timings from r6-cards-001's measured per-run times on the same GPU type;
- the job's code was not executed on the Mac.

**Verdict: fine to run. 0 blocker, 0 major, 3 minor.** All five fixes from the r6-cards-001 review are correct, and gates.py and make_cards.py read the corrected values.

## The fixes, checked

- **Item 1, tick share: correct.** cardlib.py:548-551 and 892-894 average the per-channel shares over live channels. gates.py:71-80 and 148 recompute it from tick_share_q, so r6-cards-001's cards are corrected offline too.
- **Item 2, response difference: correct.** cardlib.py:465-469 uses the per-replica difference on shared noise. The estimate is the squared mean of e minus var(e)/R_u, which is unbiased; with R_u = 2 it equals e1 x e2.
- **Item 4, non-finite runs: done after the presmoke.** The card gets the verdict "invalid: non-finite", the run counts as failed, the job exits 1, and make_cards drops the card. Two caveats:
  - The flag covers the main run only, not the branches (see the notes).
  - In the presmoke, the new error aborts the job (minor 3).
- **Item 5, diffusion controls: correct.** beta, gam and kappa are all 0, which removes every output of the law net. This matches round 5's control. The plug-in loss is exactly 0, so these controls are dull by construction.
- **Item 6, 128-px vortex: correct.** G = 16 gives 8-px blocks, as vortex64 has. The fine view (4 px) and the input bumps (16 px) match at both sizes. make_cards divides body counts and events by the area ratio of 4 and skips the action entries.
- **check_cardlib's two new cases** would both have failed on the old code. Tick share: the old pooled value is off by 0.027 against a tolerance of 0.018. Response difference: the old estimator expects about -0.45 against +0.045.

## New code paths, checked

- **Slower clock (4 world ticks per card tick).**
  - The noise clock is the world tick index, so each world tick draws fresh noise, and the hidden part acts at every world tick.
  - An input held for 4 world ticks is scaled to sigma_u/2, so it still delivers N nats.
  - Burn-in keeps its world time.
  - The branch is 32 card ticks = 128 world ticks.
  - The scan over 4 world ticks stacks nothing per world tick, so memory is not multiplied by 4.
- **Gliders with 1, 4 and 8 hidden parameters.**
  - The sets and boxes match round 5's ladder and its prior files. Neighbours are built in each set's own space, and the oracle replicas use the same centre for every set.
  - All three sets share one compiled program.
  - gliders_n8 never ran in the CPU test, so it was checked by reading the code.
- **Memory.** Device batches equal r6-cards-001's. Every group stays at about 6 GB or less; vortex128g16's 16 x 16 view adds about 0.33 GB.
- **Time.** About 43 min in all: a 27-min presmoke including seven compiles, then the rest.
  - The long pole is vortex64_s4: about 11 min per run.
  - vortex128g16 takes about 9.4 min, not about 5.
  - The 4,200 s limit binds only after about a 2x slowdown.
- **Outputs.** About 4.2 MB; the largest file is about 0.35 MB.

## Minor

1. **On the slower clock, the late window mostly repeats run A, so the late-against-early test is largely a self-comparison.**
   - strided() divides late_gap by the stride (adapters.py:385), but the window stays 400 card ticks (cardlib.py:83). The late run also uses run A's seed, and the noise depends on the absolute tick, so it replays A's trajectory.
   - membrane_s4: A records card ticks 50-450 and late 200-600. They share 250 of 400 ticks (62.5%).
   - vortex64_s4: A records 25-425 and late 125-525. They share 75%, and 24 of the 32 test states are the same.
   - A drift is diluted about 3-4x, so late_vs_early (gates.py:239-260) leans toward "same".
   - For this run: do not count the s4 worlds' "same at late time" as evidence of stationarity. Report the overlap with those results.
   - Next time: keep late_gap at least one window long in card ticks (do not divide it). That costs about 3 minutes more for vortex64_s4.
2. **make_cards' seed check compares run A's corrected response difference with run B's biased one.**
   - For gliders, vortex64 and membrane, run A now comes from this job and run B from r6-cards-001, whose biased value cannot be recomputed. Examples: vortex64 B's xresp is -0.623, gliders B's 0.094.
   - The rerun check already leaves grid.xresp out (make_cards.py:389); the seed check does not (make_cards.py:28, 372).
   - Fix offline: skip grid.xresp in the seed check when runs A and B come from different jobs.
3. **A presmoke failure of vortex128g16 ends the job with exit 2, although the notes say it is dropped.**
   - job.py:217 drops a failed presmoke group only when its priority is at least 4, and vortex128g16 has priority 3 (worlds2.json, make_worlds2.py:33). In r6-cards-001 the 128-px checks had priorities 4 and 5.
   - It is the last presmoke run, at about 1,050 s. If it fails, the 8 remaining runs are lost: both gliders_n8 cells, the late windows of both slow-clock worlds, gliders_n1 B, gliders A and the second pure-diffusion control.
   - Likewise, a non-finite first run (membrane_s4 A) now raises FloatingPointError inside the presmoke and aborts everything.
   - The probability is low. Next time: give the size checks priority 4 or more, and record a presmoke FloatingPointError as a failed run instead of exiting.

## Notes

- The structure gate's time thresholds (HALF_LIFE_MIN 16 ticks, V_NET_MIN, EVENTS_MIN; gates.py:56) are in card ticks.
  - vortex64's half-life of 51 world ticks reads as about 12.8 card ticks at stride 4, below 16, so vortex64_s4 likely loses "reading-worthy" from the change of units alone.
  - Report half-life, speed and events in world ticks (each card's meta holds the stride) when comparing clocks.
- The finiteness flag covers only the main run (cardlib.py:231); nothing checks the branch records. The skeptic found the claimed harm (a branch blow-up reading as "dull") unsupported, because every consumer tolerates NaN, and all 125 cards of r6-cards-001 were finite. Adding the branch arrays to the flag would close it.
- The membrane_s4 late run is 2,400 world ticks, not "up to 1,800"; the extra time is negligible.
