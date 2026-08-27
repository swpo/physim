# blobkit MANIFEST — provenance, locks, edits

Packaged 2026-08-27 from the physim source tree at
`/Users/spoho/Documents/prime/test/physim` (git b671958).
Originals stay in place; blobkit is purely additive. Verification transcript: `VERIFY.md`.

## Code modules

"Locked" = the file participates in `blobkit.verify_locks()` (SHA256 self-check
against `blobkit/_locks.json`; drift -> loud ImportWarning; `BLOBKIT_SKIP_LOCK=1`
bypasses). Upstream lock hashes (source tree `l0/complexity/v2_lock_hashes.txt`):
metrics_v2 `bcfd5d00…`, assay_v2 `1eb45780…`, soup_sim_v2 `8541dedd…` — verified
byte-identical to the sources copied here before edits were applied.

| blobkit file | source (repo-relative) | src mtime | src sha256 (12) | pkg sha256 (12) | locked | edits |
|---|---|---|---|---|---|---|
| `blobkit/genome.py` | `probes/blobs/l0/stage2/lib/genome.py` (identical in l0/lib, stage3/lib, deploy libs) | 2026-08-20 | `914fad08dffd` | `8f63c563b5be` | yes | E1, E2 |
| `blobkit/assays_v1.py` | `probes/blobs/l0/stage2/lib/assays.py` (stage-2 variant; stage3/lib adds V4 a2_cross, not packaged) | 2026-08-20 | `1883fdac243e` | `27c1af44a5ce` | yes | E3 |
| `blobkit/metrics_v1.py` | `probes/blobs/l0/complexity/metrics_v1.py` (LOCKED 2026-02-20 battery) | 2026-08-23 | `62d90c53840b` | `65e2d6305b52` | yes | E4, E5, E6 |
| `blobkit/hier_metrics.py` | `probes/search/hier_metrics.py` (== deploy/lib copy) | 2026-08-17 | `bf8a901683cd` | `bf8a901683cd` | yes | none (verbatim) |
| `blobkit/metrics_v2.py` | `probes/blobs/l0/complexity/metrics_v2.py` (LOCKED, sha `bcfd5d00…`) | 2026-08-25 | `bcfd5d00ea58` | `18b50bc7344a` | yes | E7, E8, E9 |
| `blobkit/assay_v2.py` | `probes/blobs/l0/complexity/assay_v2.py` (LOCKED, sha `1eb45780…`) | 2026-08-25 | `1eb457801efc` | `a8672a92a5de` | yes | E12, E13, E14, E14b |
| `blobkit/soup/sim_v1.py` | `probes/blobs/l0/complexity/soup_sim.py` (phase-5 S1 simulator; sim_cpu imports its helpers) | 2026-08-23 | `562aeb5d6c51` | `7f8f4f465a1a` | yes | E10 |
| `blobkit/soup/sim_cpu.py` | `probes/blobs/l0/complexity/soup_sim_v2.py` (LOCKED, sha `8541dedd…`) | 2026-08-24 | `8541deddb8d3` | `4cf2d9ea8d39` | yes | E11 |
| `blobkit/soup/sim_gpu.py` | MERGE of `probes/blobs/gpu/blobgpu/core.py` + `probes/blobs/gpu/blobgpu/packing.py` + `probes/blobs/gpu/blobgpu/soup.py` (gates: GATES.md in gpu/) | 2026-08-25 | core `282b8a268013` / packing `36eebc31a594` / soup `779577bd1e7d` | `c148457699f1` | yes | E15–E21 |
| `blobkit/soup/backend.py` | NEW (thin selector; no numerics) | — | — | `94ffb36141a0` | yes | new file |
| `blobkit/worlds.py` | REWRITE of `probes/blobs/l0/complexity/worlds.py` (data extracted, see below) | 2026-08-23 | `b55ddc1b5361` | `9435f8964f3a` | yes | R1 |
| `blobkit/operators.py` | `probes/blobs/l0/evolve/operators_lib.py` (l0-evolver operators on lib format) | 2026-08-20 | `fcca88b546b1` | `0e117f421546` | yes | E22 |
| `blobkit/soup/__init__.py` | NEW (re-export get_backend) | — | — | `c815014522d3` | yes | new file |
| `blobkit/__init__.py` | NEW (__version__, verify_locks) | — | — | `ef8b70134282` | no (checks the others) | new file |

## Edit log (every deviation from verbatim)

All edits are import/path plumbing only — no numerics, constants, or control
flow were touched. Each edit is also marked inline with `[blobkit edit E#]`.

### blobkit/assay_v2.py
- **E12** — 3 sys.path hacks + absolute imports -> package-relative (soup_sim_v2 -> soup.sim_cpu)
- **E13** — in-function metrics_v1 imports -> package-relative
- **E14** — CLI main(): sys.path hack + absolute worlds import -> package-relative registry
- **E14b** — default results.json next to module (site-packages!) -> cwd, BLOBKIT_RESULTS env override

### blobkit/assays_v1.py
- **E3** — absolute sibling import -> package-relative

### blobkit/genome.py
- **E1** — tree-walk CDATA (../composite/data) -> packaged blobkit/data; L0DIR removed
- **E2** — append_result default path: l0/results.json (tree) -> ./results.json (cwd)

### blobkit/metrics_v1.py
- **E4** — absolute-path sys.path hack to probes/search -> package-relative hier_metrics
- **E5** — self-import inside window_mask -> package-relative
- **E6** — in-function hier_metrics import -> package-relative

### blobkit/metrics_v2.py
- **E7** — two sys.path hacks + absolute imports of metrics_v1 -> package-relative
- **E8** — absolute hier_metrics import -> package-relative
- **E9** — in-function metrics_v1 import -> package-relative

### blobkit/operators.py
- **E22** — absolute sibling import -> package-relative

### blobkit/soup/sim_cpu.py
- **E11** — sys.path hack + absolute soup_sim import -> package-relative genome/.sim_v1

### blobkit/soup/sim_gpu.py
- **E15** — core.py module-level `import jax`/`HI` -> lazy _jax() helper; enable_x64 lazy
- **E16** — diffusion_E: lazy jnp
- **E17** — batch_keys: lazy jax/jnp
- **E18** — make_stepper: bind jax/jnp/HI lazily at build time (closures capture)
- **E19** — packing.py duplicate `import numpy as np` dropped in merged module
- **E20** — soup.py tree-walk sys.path hacks (l0/complexity + stage2/lib) -> package-relative sim_cpu/sim_v1; module-level jax import removed; packing/core imports now same-module (merged)
- **E21** — _attach_gpu: lazy jnp; enable_x64 now same-module (was .core import)

### blobkit/soup/sim_v1.py
- **E10** — sys.path hack to l0/stage2/lib -> package-relative genome

### blobkit/worlds.py
- **R1** — REWRITE: tree-walking builders -> packaged-data registry (load/names/WORLDS/KICKS/GT_SET; BLOBKIT_DATA override)

## Data

| blobkit data | source | note |
|---|---|---|
| `data/stamp_A4_dx05.npz` | `probes/blobs/composite/data/stamp_A4_dx05.npz` | byte-identical copy (genome.load_stamp_A4) |
| `data/worlds/m0.json` | built:complexity/worlds.py:m0 | ground truth, id `gt_m0`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/m4.json` | built:complexity/worlds.py:m4 | ground truth, id `gt_m4`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/xv.json` | built:complexity/worlds.py:xv | ground truth, id `gt_xv`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/bf.json` | built:complexity/worlds.py:bf | ground truth, id `gt_bf`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/pred.json` | built:complexity/worlds.py:pred | ground truth, id `gt_pred`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/coex.json` | built:complexity/worlds.py:coex | ground truth, id `gt_coex`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/mv3.json` | built:complexity/worlds.py:mv3 | ground truth, id `gt_mv3`; built 2026-08-27 by tools/extract_worlds.py via the live tree builders (worlds.py + machinev3/lib.py + stage3 encounter jobs), genome_json round-trip — verified identical to the 2026-02-25 freeze `gpu/data/gt_worlds.json` |
| `data/worlds/ds3_014.json` | `probes/blobs/l0/complexity/genomes_v2/ds3_014.json` | byte-decoded canonical JSON, id `ds3_014` |
| `data/worlds/ds3_017.json` | `probes/blobs/l0/complexity/genomes_v2/ds3_017.json` | byte-decoded canonical JSON, id `ds3_017` |
| `data/worlds/ds6_000.json` | `probes/blobs/l0/complexity/genomes_v2/ds6_000.json` | byte-decoded canonical JSON, id `ds6_000` |
| `data/worlds/g0_jit_11.json` | `probes/blobs/l0/deepsearch/deploy/seeds/g0_jit_11.json` | byte-decoded canonical JSON, id `g0_jit_11` |
| `data/worlds/engine_10748.json` | `probes/blobs/l0/stage3/engine_10748.json` | byte-decoded canonical JSON, id `engine_10748` |
| `data/worlds/rail_111_17.json` | `probes/blobs/l0/deepsearch/seeds/rail_111_17.json` | byte-decoded canonical JSON, id `rail_111_17` |
| `data/worlds/s2_128_26.json` | `probes/blobs/l0/deepsearch/seeds/s2_128_26.json` | byte-decoded canonical JSON, id `s2_128_26` |
| `data/worlds/s2_118_41.json` | `probes/blobs/l0/deepsearch/seeds/s2_118_41.json` | byte-decoded canonical JSON, id `s2_118_41` |
| `data/worlds/_extraction.json` | tools/extract_worlds.py | extraction receipt (source per world + KICKS at extraction time) |

Champion source notes: `ds3_014/ds3_017/ds6_000` are the complexity-battery
validation copies (`l0/complexity/genomes_v2/`), byte-identical to the
deepsearch deploy seeds except the deploy copies carry an extra `vtags` key
(deepsearch bookkeeping, not part of the certified genome). `g0_jit_11` exists
only under `l0/deepsearch/deploy/seeds/`. `s2_128_26.json` equals the
`s2_128_26_uni` genome inside `l0/stage2/merged_results.json` up to the `id`
field (seed file id `s2_128_26`, merged-results id `u`); machinev3's mv3 build
consumes the merged-results copy and is captured here as the built `mv3` world,
so both conventions are preserved.

`KICKS` (mv3 engine act kicked 0.5 px — its certified launch convention) is
carried verbatim into `blobkit.worlds.KICKS`.

## Promotion rule (future certified components)

A component enters blobkit only when ALL of:
1. **Certified upstream**: it has a lock/scorecard in the source tree (hash
   table or gate transcript) — blobkit packages certainties, not experiments.
2. **Verbatim + plumbing-only edits**: copies differ from source only by
   import/path edits, each marked `[blobkit edit E#]` inline and logged here
   with the exact old->new intent. Any numerics change = a NEW module name
   (metrics_v3, sim_cpu_v3, ...), never an in-place edit.
3. **Data extracted, not tree-walked**: no module may read outside the
   package dir (importlib/data/ + env overrides only).
4. **Parity-gated**: before the version bump, rerun VERIFY.md's battery —
   numerics parity vs the locked reference outputs (bitwise for simulators,
   field-by-field for metrics/funnel), fresh-venv install, lazy-GPU import.
5. **Lock table updated**: `_locks.json` regenerated, `verify_locks()` green,
   version bumped (patch = data-only additions, minor = new modules).

## Known non-goals (0.1.0)

- `soup/sim_gpu.py` merges blobgpu core+packing+soup; `anchors.py` (bond-anchor
  drivers) was NOT promoted (probe-grade, reads tree data).
- stage-3 `assays.py` V4 additions (a2_cross etc.) not promoted — they were
  certified for the stage-3 encounter screen only; promote separately if needed.
- funnel/sampler (G0 screens) not in scope for this brief; the V3 gate ran the
  tree funnel against packaged genomes instead.
