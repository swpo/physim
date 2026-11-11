# Profile 2 feasibility: F and G in a 2-CPU box

Measured 11 Nov 2026, 21:47-22:31 UTC, on 2 x86 cloud cores (Xeon @ 2.10GHz, `taskset -c 0,1`, XLA intra-op
threads 2, jax 0.12.0.1, float64 worlds). One process per measurement; memory is its peak `ru_maxrss` (0.25 GB
imports). Compile timed apart. Times: median [min, max] of 3 calls unless n is given.
Scripts `f_time.py`, `g_time.py` (via `run_f.sh`, `run_g.sh`, `run_f32.sh`); outputs `raw/`; every number with
its source in `timing.json` (`make_timing.py`). **The Mac was not measured.**

## F: foundry hidden weights (64 x 64; foundryexam's shape; full episode 332 ticks)

| | B = 1 | B = 16 | B = 64 | B = 256 |
|---|---|---|---|---|
| member-ticks/s | 112.5 | 118.6 | 116.5 | 108.9 |
| item future, 16 ticks (s) | 0.14 | 2.16 [2.04, 2.19] | 8.79 [8.64, 9.48] | 37.6 [36.5, 38.0] |
| Lab episodes (s) | 2.99 [2.99, 3.15] | 43.6 [43.4, 44.7] | 192.7 (n = 1) | - |
| compile start / run (s) | 4.1 / 3.2 | 6.4 / 5.1 | 6.4 / 5.1 | 6.0 / 4.8 |
| peak memory (GB) | 0.49 | 0.56 | 0.65 | 1.08 |
| float32 member-ticks/s | 131 | 217 | 216 | - |

Batching gains at most 6%. A full episode takes **2.72 s** at B = 16; float32 (an agent's own simulator) is 1.83x
faster.

| F, grading and recipes | 2 cores | memory |
|---|---|---|
| null pool, 512 input-free episodes | 1,433 s | 0.56 GB |
| instance build, ring_r4 shape (64 items, R 16, 256 climatology) | 1,006 s | 0.56 GB |
| plug-in item, 256 samples (assimilate 16, forecast 16) | imports 0.8 + compile 7.4 + 78.6 [76.5, 80.5] = 87 s | 1.06 GB, pool 8 MB |
| one prior world (64 + 8 gate episodes) | 196 s (+345 s if the agent screens) | - |
| P0 step, C 48, batch 256 | 0.899 [0.889, 0.905] s, compile 4.8 s | 1.63 GB |
| P0 step, C 24 (3.4x fewer weights) | 0.390 [0.382, 0.410] s | 1.17 GB |
| C 48, batch 64 (FT, D) | 0.226 [0.217, 0.231] s | 0.92 GB |
| fit gradient, 248 numbers, 8 Lab episodes x 4 members x 2 anchors, 16-tick loss, T = 32 | 41.7 [39.9, 42.0] s, compile 27.7 s, +0.8 s respin | 2.20 GB |
| same, T = 48 (foundrylong) | 46.2 s (n = 1) | 2.17 GB |

## G: gliders, hidden stress conversion (128 x 128, 20 substeps, tracker; dialsA2's shape; 82 ticks)

| | B = 1 | B = 16 | B = 64 | B = 256 |
|---|---|---|---|---|
| member-ticks/s | 8.68 | 6.92 | 5.10 | 4.76 |
| CPU-s per member-tick | 0.230 | 0.289 | 0.392 | 0.420 |
| run (s), T ticks | 1.84 [1.72, 1.90], T 16 | 37.0 [35.7, 37.0], T 16 | 50.2 [47.7, 57.2], T 4 | 107.6 [106.6, 149.1], T 2 |
| Lab episodes (s) | 9.38 [9.07, 9.51] | 193.5 (n = 1) | - | - |
| compile start / run (s) | 17.6 / 5.5 | 20.1 / 7.0 | 20.2 / 10.7 | 21.9 / 10.5 |
| peak memory (GB) | 0.91 | 1.22 | 1.88 | **4.61** |

Best at B = 1: a full episode takes **9.45 s**; round 5's 0.15 CPU-s per member-tick is 1.5 times too low. Null
pool 4,837 s; instance build 3,937 s (dialsA2's two 48-item exams), 4,911 s (ring_r4 shape); a 256-sample plug-in
item at least 944 s (no assimilation code exists). ladder_net step, batch 128 x 4: 0.610 [0.576, 0.693] s at C 48,
0.305 s at C 24 (n = 5), 1.12 GB.

## What a box can do (the whole box on one thing)

| box | F episodes | F prior worlds | F P0 steps C 48 / C 24 | F fit steps | G episodes | G theta points x 8 | G net steps |
|---|---|---|---|---|---|---|---|
| 60 min | 1,322 | 18 | 4,004 / 9,230 | 84 | 381 | 47 | 5,901 |
| 120 min | 2,644 | 36 | 8,008 / 18,461 | 169 | 762 | 95 | 11,803 |
| 180 min | 3,967 | 55 | 12,013 / 27,692 | 254 | 1,143 | 142 | 17,704 |

Pilots' GPU recipes on 2 cores:

| recipe (source) | 2 cores |
|---|---|
| F P0 arm P: 210 worlds x 64 episodes, 12,000 steps, batch 256, 2 seeds (run_fx.py; A100 9.6 ms/step) | 11.4 h sim + 3.0 h per net |
| F P0[16]: 6,000 steps | 0.87 h + 1.5 h |
| F P0(1,000): 64,000 episodes, 40,000 steps (run_fl.py) | 54 h + 10 h |
| F FT(32), FT(512): 400, 2,400 steps at batch 64 | 1.5 min, 9 min |
| F W fit: 4 starts x 200 steps (run_fl2.py) | 9.4 h |
| G public family: 768 points x 8 episodes (DECLARED R7) | 16.1 h |
| G base net: 24,000 to 192,000 steps (run_a2.py) | 4.1 to 33 h per net |

## Memory and /workspace

- F stays under 2.2 GB in every mode. G at B = 256 (4.61 GB) breaks the 4 GB cap; B = 64 peaks at 1.88 GB and
  B = 1 is fastest.
- F net data: 59.8 KB per episode; P0[210] (13,440 episodes) 0.80 GB, up to 1.6 GB while make_dataset's host copy
  lives, about 3.2 GB with the training step. P0[16]: 0.06 GB.
- /workspace counts against the 4 GB. A 180-min box's 3,967 F episodes are 0.11 GB; pools 8 MB (F), 32 MB (G);
  checkpoints under 2 MB. CPU binds first.

## Image

jax and jaxlib 0.12.0.1, numpy 2.5.4, scipy 1.18.1, ml-dtypes 0.6.0, opt-einsum 3.4.0 (no other third-party
import). PyPI has cp312 linux aarch64 wheels for all: jaxlib-0.12.0.1-cp312-cp312-manylinux_2_27_aarch64 (80.9 MB,
sha256 40812201...6774), 134 MB in total; every sha256 is already in `vfport/docker/ring-requirements.txt`
(`raw/wheels.json`). `--platform manylinux2014_aarch64` alone finds no jaxlib 0.12 (that tag ends at 0.7.1).

## What follows for budgets

1. **Unit.** A full episode is 2.72 s (F) and 9.45 s (G) on 2 x86 cores: a 60/120/180-min box is 1,322/2,644/3,967
   F or 381/762/1,143 G episodes. The spec's G figure (1,756 at 180 min) used 0.15 CPU-s per member-tick; measured
   0.23 gives 1,143. Its F figure (3,850 for 348-tick episodes) agrees: 2.85 s per 348 ticks gives 3,789.
2. **No pilot recipe fits a box.** F's best no-experiment recipe in a box is P0 on about 16 listed worlds: 52 min
   simulating plus 6,000 steps (90 min; 39 min at C 24), which fits only 180 min. The pilot's P0[16] took 0.68 of
   C against 0.86 for P0[210] (foundryexam summary.json compute.share_of_C), so box-tier references must be run in
   the box, not taken from GPU jobs. One W fit start (200 steps, 2.4 h) does not fit 180 min. FT and D take
   minutes. G cannot build a training family in any box (142 theta points at most, against 768).
3. **Prediction.** The ring limit (30 CPU-s, 60 s) is 0.19 of F's brute-force plug-in. At b_pred = 0.25 an item
   needs about 43 s wall and 56 CPU-s (T_JIT 8.2 s). G brute force takes at least 944 s per item: nets only
   (T_JIT 11.5 s, plus about 20 s to compile a spin-up).
4. **Mac grading, per 2-core box.** F: null pool 24 min (build once, keep), instance 17 min; G: 81 + 82 min.
   64 F plug-in items at 87 s take 1.6 h, inside the 9,600 s allowance.
5. **Memory** binds only G's batch (B <= 64) and F net data above about 20,000 episodes.

## Not measured

The Mac: no Apple Silicon timing exists. Inferred only: an M-series core does 1-2 Xeon cores' scalar work, but
NEON has 2 float64 lanes against AVX-512's 8, so the factor may be below 1. The three scripts cannot measure it on
the Mac as written (correction after review, `../DESIGN.md` section 8 C4): they hard-code this container's paths
(`PY=/home/user/...`), and the Mac runbook forbids any `docker run` by hand (vfport `RUNBOOK_MAC.md` l. 114). Their
modes must run as a scripted policy through the port's own boxes (`../DESIGN.md` pin item 8), where `--cpus 2` is a
CPU quota rather than the pinned cores used here; host-native work (draw, build, null pool, Lab) needs its own ratio
from the instance stage's clock. Not timed either: the vw Lab path (episodes ran through fx_lib.Runner's compiled tick), W's
prescreen, G's H recipe. Load from other work: 1.2-2.1 (`raw/*_log.txt`).
