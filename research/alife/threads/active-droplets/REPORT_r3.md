# active-droplets: sprint 3 report (final sprint)

## 1. Headline

The committee's turnover protocol now runs in a ledger world (`ad9-ledger`):
- births are coupled to Moran deaths;
- mutation is a logged ±1-rung copy error at birth (p=0.1);
- the neutral twin replays the identical event streams.

The 3-seed landscape confirms a broad optimum in membrane output at kp 0.5-1.5. **But the evolution test does not pass at the scale we could afford** (128², t=30000): mutation supply is the bottleneck. Each run had about 27 births and only 2-5 mutations, so S and N stay inside each other's range. RESULT_LINE

## 2. Claims

| world | claimed level | strongest evidence | known weaknesses |
|---|---|---|---|
| `ad9-ledger` landscape | L3 + L4c Weak, plus the **fitness landscape** of a heritable membrane trait | `screens/ad9_landscape.png`, `runs/land_r*_s*` (3 seeds, harmonic gate). Births by t=6000 for kp 0 / 0.25 / 0.5 / 1 / 1.5 / 2.5 / 4: 0.3 / 4.7 / 6.7 / 6.7 / 6.3 / 1.7 / 1.0. Droplets: 4.7 / 9.0 / 11.7 / 11.7 / 11.3 / 6.7 / 6.0. | t=6000 only; no dx=0.5 test this sprint. |
| `ad9-ledger` S vs N | L7[L3] **not supported** (does not pass) | `runs/{S,N}_a{1,5}_s{0,1,2}/ledger.json`, `screens/ad9_evo.png`. Ledger table below. | Scaled down: 128² vs 192², t=30000 vs ≥40k, cap=6 cells, so drift is strong. |
| ad7 family (carried) | L6[L3] medium (committee) | sprint-2 packs; showcase movie | |

LEDGER_TABLE

## 3. Mechanisms and what the ledger taught

- **Turnover had to be designed.** At cap=12 (carrying capacity), the kp=2.5 ancestor made 9 births in t=30000, with 1 mutation and 1 kill: no turnover at all (`runs/cap12`). Births are fuel-limited at full occupancy. Only below capacity (cap=6) do cells divide continuously, with births = kills over about 4 turnover generations.
- **Conversions and off-kind daughters are now zero by construction** (whole-droplet rung, transported with the catalyst). The ledger confirms 0 conversions and 0 off-kind daughters. That addresses the r2 criticism of r=5 patches relabelling intact droplets.
- **Mutation supply is the limit.** At the committee's ceiling p≤0.1 per birth, with ~27 births per run, each run sees about 3 mutants. With Moran drift in 6 cells, most are lost whatever their kp. A pass needs roughly 10x more births: bigger boxes, faster division, or longer runs.

## 4. Negative results

- The cap=12 protocol gave no turnover (above).
- `ad8-parasite`: written, never run, deleted (the autopoiesis thread covers parasites).
- Not done for lack of compute: R arm at D=M and 2M (3 seeds), the bu=1.0 vs 0.5 landscape, L4c flux budget with a local fuel cut, dx=0.5 for the gated shell. The one R check from sprint 2 (ad7: 5 vs 12 droplets, 1 seed) stays unreplicated.

## 5. If there were a next sprint

Run the same ledger world at 192² with cap ≈ 15 and t ≥ 100k (about 1.5 h per run), or speed up division (higher F and k) so ≥300 births per run give ≥30 mutations. The pass criterion and the N-twin machinery are already in place.
