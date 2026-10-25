# kstrail vs a matched slow-inhibitor reaction-diffusion twin (Q:bd-kstrail-laplacian-twin)

**Twin (`world.py`, rdtrail).** kstrail's three fields with both taxis terms removed. `a` and `h` keep
kstrail's linear equations exactly (Da 4, ka 0.1, Dh 0.2, kh 0.05, beta 1); the body u keeps Du = Dr = 1.2.
They act on u only through local kinetics, by raising the threshold of a bistable production:
`du/dt = Du lap u + r u(1-u)(u - th0 - ga a - gh h)`. `a` becomes the fast long-range inhibitor that localizes
spots, `h` the slow self-made inhibitor (the Krischer-Mikhailov drift-bifurcation ingredient).
`world_slow.py` (kh 0.02, beta 0.4) and `world_slow5.py` (kh 0.01, beta 0.2) keep the static load h = 20u
and make only the inhibitor slower (tau_h = 50 and 100 against kstrail's 20).

**Initial condition.** The twin's uniform state decays (th >= u everywhere for th0 >= 0), so it does not
form spots from noise (screen: 8/8 from-noise runs went extinct, rho0 0.5 + noise 0.3). The packs plant
6 disks (r = 7) at seed-random positions plus noise. That favours the twin. kstrail forms from noise.

## Results (192^2, T = 600, labkit; tracks from `metrics.json`)

| arm | seeds | moving tracks (>=1 BL) | top-10 tracks >= 5 BL | max BL | speed of top tracks | body size sqrt(area) | what the sheet shows |
|---|---|---|---|---|---|---|---|
| kstrail (fresh seeds 3, 4) | 2 | 23, 25 | 10/10, 10/10 | 31.6, 19.1 | 0.28-0.59 | 6-14 | isolated crescents swim through open space (`packs/kstrail_s34/seed3/sheet.png`) |
| twin, matched kh 0.05 | 3 | 3, 2, 0 | 0, 0, 0 | 1.4, 1.5, 0.9 | 0.04-0.17 | 26-30 | round spots self-replicate until they tile the domain, then sit (`packs/twin_kh05/seed0/sheet.png`) |
| twin, kh 0.02 | 3 | 7, 9, 8 | 0, 0, 0 | 2.4, 1.9, 1.4 | 0.08-0.18 | 21-32 | arcs and replicating spots, jammed (`packs/twin_kh02/seed0/sheet.png`) |
| twin, kh 0.01 | 3 | 4, 7, 7 | 0, 0, 0 | 1.7, 2.9, 2.2 | 0.13-0.31 | 16-35 | kstrail-like crescents with the trail behind them, crawling but jammed by replicating neighbours (`packs/twin_kh01/seed1/sheet.png`) |

Screens at 128^2 with two planted disks (`screens/`): at kh 0.05, 30 kinetic points (r 1-4, th0 -0.05..0.05,
gh 0.004-0.04, ga 0.06-0.1) gave extinction, a sea, stationary spots/labyrinths, replicating spots or
chaotic expanding patches; none gave isolated travelling spots (`s7.png`, `s8.png`). Travelling crescents
appear at kh 0.02 and 0.01 with gh 0.01-0.02 (`s9.png` rows 2-3, `s6.png` row 4), and in small domains
they do travel several radii before crowding.

## Reading

- At kstrail's linear rates, this twin family does not swim: M is lost (0/3 seeds, no track >= 1.5 BL).
- Slowing the inhibitor 2.5-5x recovers the crescent shape and a crawl (speed about half of kstrail's,
  bodies about 2x larger), but in a matched domain the twin's bodies multiply and jam, so no track
  reaches 5 BL. The RD twin gains self-replication (persistent splits 5-15, max generation 3-5), which
  kstrail lacks (it conserves rho).
- So the drift mechanism itself is not specific to taxis (crescents with a trail exist in RD, as
  Krischer-Mikhailov predicts), but at matched rates kstrail's sustained free swimming needs the taxis
  coupling and mass conservation.

## Limits

One kinetic family (bistable threshold kinetics); someone could find RD kinetics that swim at kh 0.05.
The twin is planted, not from noise. Bodies are larger than kstrail's, so body-length counts penalize the
twin; raw speeds (0.04-0.31 vs 0.28-0.59) say the same. Twin bodies collide, and the tracker breaks
tracks at collisions, which caps BL. No dt/2 or grid check of the twin. Not reviewed.
