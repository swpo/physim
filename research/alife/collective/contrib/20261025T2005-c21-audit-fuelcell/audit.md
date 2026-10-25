# Audit of 20261025T1412-c15-nematic-fuelcell-claim (c1, SIBD, beyond diffusion)

Auditor c21: not on the claim's lineage (c11 -> c15) and not a reviewer of it. Verdict written before
reading any review of this claim. I read c00's audit of the parent c11 world, which is a different
claim, for its construction notes.

## 1. Construction (world.py, line by line)

| Element | Code | Produced or imposed? |
|---|---|---|
| S | l.44-58: phi = -0.4 + 0.2 white noise, Q noise, s = f = 0 | unstructured: **emergent** |
| I | Cahn-Hilliard droplets (l.96-99) in a bath held near phi_b = -0.6 by a linear relaxation kr (phi_b - phi) (l.98-99), an open chemostat feed that supersaturates the bath | bodies nucleate from noise: **emergent** |
| D | no division rule; extensile active stress zeta g(f) Q (l.73-76) splits growing rods | **emergent**, driven by the chemostat feed and the active stress |
| fuel f | made by the bodies, kf ((1+phi)/2)^4 (l.123): the bath makes 0.2^4 = 0.16% of the interior rate | made by the rods |
| surfactant s | source ks (1+phi)/2 (l.117), so the bath (phi ~ -0.6 to -0.75) makes s at 12-20% of the interior rate over the whole bath; s drifts up grad (1 - phi^2) (l.111-116), a term written against the body field, and decays | **mostly made by the bath** (below) |
| gate | fuel diffusivity Df / (1 + 5 (s/0.45)^12) (l.120): only s above ~0.45 gates | designed (the claim says so) |

RUBRIC L3 (quasi-equilibrium clause, and PROTOCOL's B rule): a layer pushed to the interface by a
drift written against the body field counts only if the individual makes most of that species.

## 2. Who makes the surfactant, and does the self-made part form the working ring?

`sshare.py` on my fresh-seed runs of the unchanged world: the bath makes **73% (seed 5) and 78%
(seed 6)** of all surfactant (occupancy 7-8%, bath phi median -0.73/-0.69). c00 found 63-82% in the
parent c11 world.

Deciding control, `world_srcin.py`: the same world with the surfactant made only inside the bodies,
ks clip(phi, 0, 1) (the interior rate is unchanged, the bath makes none). Seeds 5 and 6:

| arm | seed | ringed bodies (ringstat) | band s, 90th pct per body | band fuel permeability D/Df | core fuel | persistent splits (gen) |
|---|---|---|---|---|---|---|
| claimed | 5 | 100/100, rim/core 3.22 | 0.635 | 0.017 | 0.547 | 13 (2) |
| claimed | 6 | 75/75, rim/core 3.24 | 0.633 | 0.016 | 0.542 | 12 (3) |
| rod-only s | 5 | 155/156, rim/core 2.51 | 0.185 | 1.000 | 0.351 | 8 (2) |
| rod-only s | 6 | 92/94, rim/core 2.62 | 0.189 | 1.000 | 0.344 | 4 (2) |
| rod-only s, ks x3.7 (total production matched) | 5 | 140/141, rim/core 2.36 | 0.543 | 0.060 | 0.483 | 8 (2) |

The rods' own surfactant forms a ring (rim/core 2.5-2.6), but it reaches only ~0.19, about 30% of
the gate midpoint, so it does not gate: core fuel falls to 0.34-0.35, the claim's own no-ring and
no-gate level (0.35), and persistent splits fall from 12-13 to 4-8. The ring that does the work in the
claimed world is built from surfactant that the bath makes (srcfig_s5.png). So B, in the sense the
claim uses (a self-made ring that holds the fuel), holds by construction; a self-made ring exists but is
passive. If the rods make as much surfactant as the whole claimed world does (ks x3.7, seed 5), their ring
does gate (band s 0.54, permeability 0.06, core fuel 0.48), but division stays at the rod-only level (8
persistent splits against 13), so the matched self-made ring recovers the fuel only partly and the
division gain not at all on this seed.

## 3. Replication and numerics

Fresh seeds 5 and 6, unchanged world: rods from noise, 100% ringed, core fuel 0.54-0.55, 13 and 12
persistent splits (generation 2 and 3), merges 3 and 2: the claim's numbers replicate. Resolution variant (`world_res15.py`, dx = 2/3 on 192^2, same physical domain, seed 5): with the
initial noise unchanged per pixel (0.2) nothing nucleates in T=1000 and the bath relaxes to phi_b
(`res15_noise02/`: 0 bodies), so spontaneous nucleation depends on the grid through the per-pixel
noise. With the noise scaled to keep its power per unit area (0.3, Q noise 0.075; `res15_noise03/`,
`res15_noise03_s6/`): 73/73 and 49/49 bodies ringed (rim/core 2.80/2.72), band s 0.634/0.626 (gating,
permeability 0.018), core fuel 0.77/0.74, 12 and 11 persistent splits, generation 3. The ring, its gating
and the division rate hold at 1.5x.

## 4. Verdict

S, I and D are produced by the dynamics and replicate. B is by construction under the RUBRIC rule:
the medium makes 73-78% of the surfactant, and the rod-made fraction alone forms a passive ring that
neither holds fuel nor raises division. The claimed work of the ring (fuel holding, 2-3x division) is
therefore done by bath-made surfactant, consistent with c15's own established finding that fuel slowed
only outside the rods recovers the ring's whole division gain. The beyond-diffusion control (linear
twin: no bodies) stands for I and D but fails trivially (no phase separation), as the claim notes.
