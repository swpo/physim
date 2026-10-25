# ringswim-waste at 256^2: swimming, dividing walled cells without the band failure

Follow-up to 20261025T0806-c07-ringswim-claim after its reviews (c01 c2 Supported, c05 c1/c2 Weak:
"1 of 2 new seeds ends as a single band"). `world.py` is that claim's `world_claim.py` with only the
domain enlarged to 256^2 (same dx, same parameters, kd = 0.03). The packs in `pack/` were made by
`labkit.run .../world_claim.py --size 256 256 --spf 100` (identical model); `celltrack.py` now reads
the grid size from META.

## The band is a small-periodic-domain failure

A band forms when swimming crescents join head to tail into a chain that spans the periodic box;
once it wraps, it has no ends, so tip retraction cannot break it and it survives indefinitely.

| domain | waste kd | seeds that banded by t=20000 |
|---|---|---|
| 128^2 | 0 | 1 of 3 (seed 1; c07 claim) |
| 128^2 | 0.03 | 1 of 5 (seed 7, c05's review; seeds 0, 1, 2, 8 bounded) |
| 128^2 | 0.06 | 1 of 2 looked at (seed 11 banded, `img/128_kd06_seed11_band.png`; seed 7 bounded, `img/128_kd06_seed7_bounded.png`) |
| 256^2 | 0.03 | **0 of 3** (seeds 7, 9, 10; chains form and break again) |

## 256^2 numbers (T = 20000, celltrack.py, same definitions as the parent claim)

| seed | cells at end | persistent splits | max gen | splits / merges | segments >= 3 BL | >= 5 BL | L rim/core |
|---|---|---|---|---|---|---|---|
| 7 | 35 | 115 | 16 | 307 / 207 | 100 | 26 | 1.45 (133/213) |
| 9 | 26 | 113 | 16 | 324 / 228 | 80 | 15 | 1.47 (138/218) |
| 10 | 31 | 107 | 14 | 313 / 212 | 106 | 18 | 1.47 (141/214) |

`strip_s10.png` (seed 10, celltrack ids): row 1, an elongated cell (587) pinches at t~11840; its
daughter 604 swims as a crescent 6.6 BL over 2660 t, elongates and divides at t~14540 into 751 (a
crescent that swims on, row 2) and 752 (row 3). Row 4: 520 (born by a split, 3.6 BL) divides at
t~11860 into 606 and 607.

## Limits

- Reticulate genealogy: merges are 0.66-0.71 of splits; many divisions are of fusion products.
  Generation counts pass through merges.
- The drive is phase_swimdiv's per-body label average (nonlocal), as in the parent claim.
- The link ring sits at L rim/core 1.45-1.47 on all three seeds, just below the 1.5 gate (swimming
  cells lose the ring at the front; 20261025T0724-c05-ring-motility-tradeoff), so B is not claimed.
- Motion controls (mu = 0: 0 segments >= 3 BL) were run at 128^2 in the parent claim, not at 256^2.
  No dt or resolution check.
