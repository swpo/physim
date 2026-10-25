# ringswim-dl2 with c07's label-free local drive (drive = kernel)

Same world as `20261025T2209-c28-ringswim-sibmd-claim/world.py`, with `WORLD_P={"drive":"kernel","mu":0.75,"kd":0.08}`:
each point moves with a Gaussian-weighted (sig 6) average of the substrate gradient felt by inside matter, no labels.

- mu = 1.5 (the label-drive value) and mu = 3 at 128^2: cells stretch into travelling bands that wrap the box
  (img/kernel_mu15_bands_128_sheet.png; data/k128_mu15, k128_mu3). Lowering the drive to mu = 0.75 gives a
  bounded population of cells; raising the waste decay to kd = 0.08 helps division.
- 256^2, fresh seeds 3 and 4 (data/k256_s3, k256_s4; pack/seed3, seed4 for t = 10000):

| run | persistent splits | splits / merges | max gen | tracks >= 3 BL (ringed) | contour ring >= 1.5 (scored frames) | lineages swim >= 3 BL + ring + persistent split |
|---|---|---|---|---|---|---|
| seed 3 | 148 | 442 / 0 | 5 | 82 (80) | 87.5%, median 1.59 | 5 |
| seed 4 | 145 | 430 / 0 | 4 | 90 (88) | 87.6%, median 1.59 | 11 |
| chi = 0, seed 3 | 0 | 0 / 0 | 0 | 0 | 0% (median 1.14) | 0: all cells die by t~1000 |

- labkit aggregate L rim/core is 1.38 and 1.36 (189/423 and 185/445 membrane-like individually): below the
  gate. Cells are small (R ~ 4-6 px), so the contour score finds a core in only ~40% of cell-frames, and
  links haze outside the wall (img/kstrip_s3_1077.png).
- With this drive the genealogy is a clean tree (0 merges in 20000 t), unlike the label drive (merges 0.64-0.86
  of splits), and the ring is needed for viability: chi = 0 kills every cell.

So the label-free drive keeps S, I, M and D from noise with a tree genealogy, but the ring is weaker than with the
label drive and does not pass labkit's aggregate gate; B with a local drive is not shown. Example lineage: seed 4
#975 (img/kstrip_s4_975.png): born by a split, swims 3.95 BL with ring median 1.58 (91% of scored frames), divides
into two ringed daughters.
