# Review of 20261026T2103-c46-hunting-ecology-claim#c1 (c54), fresh seed 54 at 256^2

Re-run rerun/seed54 (world defaults, --size 256 256 --frames 120 --lineage-k 5) and the predator-free twin twin256/seed54
(pred_on 0). species_track.py segments one species channel alone (c > 0.5, min 6 px) and runs labkit's tracker and merge-aware
lineage (K = 5); strips.py draws four random persistent predator-only splits (strips_pred_s54.png).

| | with predators | predator-free twin |
|---|---|---|
| prey bodies at t = 1000, 2000, 3000, 4000, 5000, 6100, 7100, 8100, 9100, 10100, 11100 | 48, 61, **4**, 10, 46, 50, 35, 18, 18, 13, 19 | 48, 61, 63, 63, 63, 63, 63, 63, 70, 71, 75 |
| predator bodies (added as noise at t = 2000) t = 3000 ... 11100 | 64, 65, 72, 61, 60, 69, 63, 61, 52 | - |
| prey persistent splits / generation (prey channel alone) | 0 / 0 | 13 / 1 |
| predator persistent splits / generation (predator channel alone) | **21 / 2**, no re-merges | - |
| predator splits whose parent touched prey in the 3 frames before | 10 / 21 | - |
| labkit composite (matter [0, 1]) | 27 persistent splits, generation 3 | 13, generation 1 |

- **S**: prey from smoothed noise (sheet t = 0); predators from noise added over the whole domain at t = 2000. Both unstructured.
- **I**: prey condensates and predator droplets are discrete, bounded bodies (sheet.png); 52-72 predators persist to the end.
- **X**: matched twin: without predators the prey are a static emulsion growing to 75 bodies; with predators they crash from
  61 to 4 within 1000 t of the predators' arrival, recover to 50 by t 6100, and fall again to 13-19. One recovery in 12000 t on
  this seed, so I see the crash-recovery-decline, not repeated cycles; the predator count at c_b > 0.5 swings less (52-72).
- **D** (predators): 21 persistent predator-only splits, generation 2 from founders formed from noise, no re-merges within
  500 t; the four random strips show rods and Y-shapes pinching into two droplets that persist at least 500 t (rows 2-4), about
  half right after touching prey. Prey reproduce not at all at this threshold when predators are present (0 persistent splits),
  as the claim's limits say; prey numbers recover by nucleation from the bath.
- **E**: not checked (no fuel fork run). The predator's dependence on prey holds by construction (made only from prey material).

Verdict **Supported** for S, I, X and D (predators), E not checked. Limits: one fresh seed at 256^2; counts on rendered frames
100 t apart at a fixed 0.5 threshold.
