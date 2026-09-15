# Measurements from the fresh simulations

Values below are recomputed from the saved arrays and measurement records. See [the report](REPORT.md) for protocol and interpretation.

## Random-start characterization

| World | Seed | Organisms at end | Moving fraction | C9 | Occupancy by activator | Extension flags |
|---|---:|---:|---:|---:|---|---|
| `bf` | 11001 | 12 | 0.9990 | 0.5194 | 2.4% | none |
| `bf` | 11002 | 12 | 0.9988 | 0.3359 | 2.4% | none |
| `ds6_000` | 11001 | 146 | 0.8091 | 0.6135 | 16.9%, 24.3% | none |
| `ds6_000` | 11002 | 148 | 0.8158 | 0.6082 | 17.2%, 24.1% | none |
| `m0` | 11001 | 12 | 0.0000 | 0.0000 | 1.9% | none |
| `m0` | 11002 | 12 | 0.0000 | 0.0000 | 1.9% | none |
| `m4` | 11001 | 12 | 1.0000 | 0.3715 | 2.5% | none |
| `m4` | 11002 | 12 | 0.9996 | 0.4317 | 2.4% | none |
| `mv3` | 11001 | 8 | 0.5390 | 0.5778 | 0.8%, 0.6%, 0.0% | none |
| `mv3` | 11002 | 8 | 0.5293 | 0.6158 | 0.8%, 0.5%, 0.0% | none |
| `p4g2_044` | 11001 | 30 | 0.9082 | 0.0000 | 1.9%, 29.5%, 85.1%, 46.6% | a_mem |
| `p4g2_044` | 11002 | 37 | 0.8424 | 0.0000 | 13.8%, 14.6%, 77.0%, 41.2% | a_mem, b_org |
| `xv` | 11001 | 12 | 0.0894 | 0.1271 | 1.2%, 1.2% | none |
| `xv` | 11002 | 12 | 0.1128 | 0.2023 | 1.2%, 1.2% | none |

## Native sensor continuations

Mean raw RMS at 50 tu, across fields and 13 probe nodes. Three future noise seeds per preparation. Baseline drift compares each continuation with its own initial readings; independent difference compares baseline noise realizations. Pulse effects compare treatment with the same-noise baseline. These raw units do not support a difficulty ranking across worlds.

| Preparation | Baseline drift | Independent difference | Pulse 0.05 effect | Pulse 0.3 effect |
|---|---:|---:|---:|---:|
| `bf_s11001` | 0.61291 | 0.0057348 | 0.083989 | 0.48968 |
| `bf_s11002` | 0.63911 | 0.0034225 | 0.035124 | 0.63419 |
| `ds6_000_s11001` | 0.34929 | 0.0022588 | 0.032612 | 0.21928 |
| `ds6_000_s11002` | 0.29407 | 0.03546 | 0.19906 | 0.34383 |
| `m0_s11001` | 0.0014928 | 0.001657 | 0.033138 | 0.57611 |
| `m0_s11002` | 0.003405 | 0.0015029 | 0.030866 | 0.57611 |
| `m4_s11001` | 0.67808 | 0.0035266 | 0.072251 | 0.28278 |
| `m4_s11002` | 0.65161 | 0.0019496 | 0.010025 | 0.20916 |
| `mv3_s11001` | 0.38871 | 0.0008277 | 0.020781 | 0.045844 |
| `mv3_s11002` | 0.3955 | 0.0013474 | 0.0074028 | 0.07241 |
| `p4g2_044_s11001` | 0.59324 | 0.00071637 | 0.011983 | 0.10041 |
| `p4g2_044_s11002` | 0.087035 | 0.00060539 | 0.0010578 | 0.0097284 |
| `xv_pair_coupled_s12001` | 0.49519 | 0.002897 | 0.017808 | 0.34633 |
| `xv_pair_coupled_s12002` | 0.50388 | 0.0061951 | 0.059466 | 0.39252 |
| `xv_s11001` | 0.30007 | 0.0067244 | 0.18322 | 0.41158 |
| `xv_s11002` | 0.37595 | 0.0047442 | 0.15369 | 0.40062 |
