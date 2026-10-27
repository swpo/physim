# Audit of 20261027T0040-c49-reacting-thermals-claim c1 (SIMDE), by c53

**Construction (world.py, line by line).** Vorticity-streamfunction Boussinesq fluid; heat T is the body field
(META matter = channel 0). Nothing marks a body, there is no division or death rule, no planted structure.
- `I`, `D`: produced by the dynamics. Caps stretch into arcs and shed arms that curl into new caps; the g=0 twin
  (claim) also splits, so splitting is partly the reaction-diffusion front instability, sharpened by the flow.
- `E`: by construction. T is made only by burning fuel (Q r) and decays at h=0.3; a body is build-from-food plus
  decay, so any fuel cut must put it out (RUBRIC L4c: counts for the rung, scored under mechanism). My fork on seed 32
  (fuel emptied at t=400): 20 -> 2 -> 0 bodies at t=400/401/402, fed twin keeps 18-23 (efork.txt).
- `M`: the only force that moves a body is `g dT/dx`, the torque of a uniform imposed gravity acting on the body field
  itself. The deciding control (passive_control.png, speeds.txt): on seed 32 at t=300 I switched burning off and made
  heat conserved (A=0, h=0). The caps keep their mushroom shape and vortex pair and rise at the same speed as the fed
  caps (median vertical speed 0.48 vs 0.41 px/t over t=300-340, 5 of 6 vs 21 of 22 tracks rising) until diffusion
  and shear smear them below threshold in ~25 t. With burning off and h kept (noburn), they vanish in ~4 t. So the
  motion is the buoyant rise of hot fluid in an imposed field, as for any passive thermal; burning only keeps the body
  hot long enough to cover 3 lengths. Direction is set by gravity (9/10, 14/16, 50/58 dividing caps move up within
  45 deg on my seeds). RUBRIC L4b asks for self-propulsion with no imposed field; sedimentation or buoyant drift in
  a uniform body force is the gravitational analogue of drift in a global gradient. I mark `M` by construction.

**Replication (fresh seeds; claimed world, unchanged).**
| run | survives | persistent splits | max gen | merge/split | dividing caps >= 3 sqrt(area) | >= 3 long axes |
|---|---|---|---|---|---|---|
| rerun seed 31 | no: every pocket burns out by t~60 | 0 | 0 | - | 0 of 0 | 0 of 0 |
| rerun seed 32 | yes | 23 | 7 | 0.18 | 8 of 10 | 5 of 10 |
| dt/2 (world dt 0.02) seed 33 | yes | 34 | 6 | 0.09 | 8 of 16 | 2 of 16 |
| 1.5x grid (192^2, all lengths x1.5) seed 34 | yes | 82 (divmove) / 65 (labkit) | 7 | 0.07 | 43 of 58 | 19 of 58 |
| survival screen seeds 35-46 (t=200) | 12 of 12 | 1-10 | 1-3 | 0.13-0.30 | - | - |

The 1.5x grid scales nu, kT, kY by 2.25, hyper by 5.06, g by 1.5 and the noise length by 1.5 (a true refinement in px
units, with dt 0.025 for the advective CFL). Division and caps survive both numerical variants. Seed 31 shows that S
is not certain: 1 of 16 fresh seeds went extinct in the initial burn-out (T=0 is absorbing, so nothing reignites).
Named individual on my seed: seed 32 track 297 (strip_s32_t297.png), born by a split at t=458, rises 46 px = 9.6
sqrt(area) to its own division at t=545.

**Verdict.** I, D and S are supported and replicate on fresh seeds, at dt/2 and at 1.5x resolution. E holds by
construction (agreeing with the three earlier reviews). M holds by construction: the passive-thermal control shows
the motion is buoyant drift in an imposed uniform field, not thrust the body makes; this lifts the question all three
reviewers left to the operator. The class remains a good PhySim world (reproduction by fluid instability, robust to
numerics); a version where the caps choose their direction (no gravity, e.g. Marangoni or reaction-driven flows)
would be needed for M.
