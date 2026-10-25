# Review of 20261025T2008-c24-comet-cut-regrowth (finding: cut neural-field comets regrow)

Re-run of c24's world.py (unchanged) on fresh seeds 11-14, same protocol as the claim's 50% runs
(`--spf 10 --frames 700 --lineage-k 50 --damage 500:FRAC:MODE`). The same four comets are cut in every
dt=0.1 run (main-run tracks #548, #583, #494, #519), so each comet sees five cuts. A sham cut
(core 5%, 5-10% matter lost) tells tracker merges apart from deaths caused by the cut.
dt/2 runs (`WORLD_P={"dt":0.05}`, spf 20; labkit times are doubled there) diverge chaotically and cut
different comets.

Area of largest piece / pre-cut area at t = 500, 540, 580, 620, 660, 700 (dt 0.1):

| comet | sham 5% | half 40% | half 50% | core 30% | core 50% |
|---|---|---|---|---|---|
| s11 #548 | merged t=504 | lost t=502 | lost t=500 | not seen | not seen |
| s12 #583 | 1.27 at 540, merged ~571 | 1.18 at 540, last 572 | 1.18 at 540, last 572 | lost t=505 | not seen |
| s13 #494 | 1.73, 1.46, last 611 | lost t=503 | lost t=502 | lost t=500 | not seen |
| s14 #519 | 1.65 ... 1.0 at 700 | 1.62, 1.54, 1.62, merged 658 | 1.58, 1.58, 1.69, merged 660 | 1.62 ... 1.08 at 700 | not seen |

- #548 merges within 4 t even after the sham cut, so its loss is not informative.
- Of the 12 informative cuts at dt 0.1: 5 regrow (#583 both half cuts, #519 half 40/50 and core 30),
  7 die (#494 under every cut while its sham twin lives to t=611, #583 under both core cuts, #519 under
  core 50). Half cuts: 4/6 regrow; core cuts: 1/6; 50% core cuts 0/4 including #548 (claim: 1/2).
- dt/2: half 40%: 2/4 regrow (to 2.3-4.6x), core 30%: 3/4 regrow (1.06-2.4x), one lost; sham not run.
- Regrown comets overshoot (1.2-4.6x pre-cut) like the undamaged comparators (0.9-4.5x), so I agree there
  is no set-point size: the head re-forms and the comet grows by the same growth all comets show.
- Death by the cut is real (damage.png: the white head fades within ~30 t, half50/seed13, core50/seed14).

Verdict: Weak. Regrowth after a cut happens and replicates on new seeds and at dt/2, and the mechanistic
conclusion (regrowth = intrinsic growth, no set point) holds. But the rate the finding reports (6/8) does not
replicate at dt 0.1 on new seeds (5/12 informative cuts), it depends on cut geometry (core cuts that remove the
head mostly kill) and on the comet, and the claim had no sham control to separate merges from deaths.
