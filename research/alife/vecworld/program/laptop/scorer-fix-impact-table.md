# PhySim fair-estimator impact: plugin (old) vs fair (new)

Date 2026-11-07. Fixed scorer: `blobround6_eval.py` 9deb1738 and `legacy_v1/blobround6_eval.py` d9277b60 (identical in residency-environments `physim-fair-energy` 4713d14 and wt-labworlds `physim-fair-energy-labworlds` 53223cb). Lab bundles were scored from wt-labworlds, Blobkit bundles from residency-environments (Python 3.12.12, numpy 2.5.2, macOS arm64). Pre-fix scorer: 3d8e3fb3 (current), dcd1ab23 (legacy). Rewards: `precision_reward(S, K=2.0)` from `physim/rewards.py` (unchanged by the fix).

Every row was re-scored from saved forecasts and stored truths with both estimators (data only, all bundle and forecast hashes verified). "S plugin (= recorded)" is the fixed scorer with `estimator="plugin"`; the last column says whether it equals grade.json / the recorded table bit for bit. Relative changes are (fair - plugin) / plugin. Family columns give the range of the per-family relative change of the case-mean energy.

## 1. Summary by world/bundle and row kind

| World / bundle | Row kind | Rows | m (forecast) / n (truth) | Zero spread | S plugin range | Rel. change of S: min / median / max | Marginal CRPS rel. change | Reward K=2 change (min..max) | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|
| fedvortex (lab, 66b6c134) | agent rollout | 2 | 64 / 2 | 1 | 0.1066 .. 349.8 | -0.60% / -0.30% / +0.00% | -0.94% .. +0.00% | +0.0000 .. +0.0013 | 2/2 |
| bf (38d159a8) | agent rollout | 35 | 64 / 2 | 6 | 0.006532 .. 4.262 | -2.99% / -0.03% / +0.00% | -2.60% .. +0.00% | +0.0000 .. +0.0066 | 33/35 (+2 ulp-level, x86_64 grades) |
| bf (38d159a8) | preflight agent probe | 5 | 64 / 2 | 5 | 0.497 .. 0.497 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 2/5 (+3 ulp-level, x86_64 grades) |
| bf (38d159a8) | pipeline check (scripted) | 27 | 64 / 2 | 27 | 0.497 .. 0.497 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 27/27 |
| bf (38d159a8) | reference demo (persistence, 4 members) | 4 | 4 / 2 | 4 | 0.497 .. 0.497 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 4/4 |
| bf (38d159a8) | preflight reference | 1 | 64 / 2 | 1 | 0.497 .. 0.497 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 1/1 |
| xv (440472fb) | agent rollout | 13 | 64 / 2 | 1 | 0.1013 .. 2.736 | -1.82% / -0.01% / +0.00% | -2.26% .. +0.00% | +0.0000 .. +0.0040 | 13/13 |
| xv (440472fb) | pipeline check (scripted) | 10 | 64 / 2 | 10 | 0.4279 .. 0.4279 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 10/10 |
| xv (440472fb) | reference demo (persistence, 4 members) | 3 | 4 / 2 | 3 | 0.4279 .. 0.4279 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 3/3 |
| p4g2_044 (0a1aa909) | agent rollout | 13 | 64 / 2 | 3 | 0.02667 .. 6.705 | -1.71% / -0.01% / +0.00% | -1.77% .. +0.00% | +0.0000 .. +0.0013 | 12/13 (+1 ulp-level, x86_64 grades) |
| p4g2_044 (0a1aa909) | preflight agent probe | 1 | 64 / 2 | 1 | 0.873 .. 0.873 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 0/1 (+1 ulp-level, x86_64 grades) |
| p4g2_044 (0a1aa909) | pipeline check (scripted) | 7 | 64 / 2 | 7 | 0.873 .. 0.873 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 7/7 |
| p4g2_044 (0a1aa909) | reference demo (persistence, 4 members) | 3 | 4 / 2 | 3 | 0.873 .. 0.873 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 3/3 |
| p4g2_044 (0a1aa909) | preflight reference | 1 | 4 / 2 | 1 | 0.873 .. 0.873 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 1/1 |
| worked p4g2_044, legacy (0c133190) | agent rollout | 24 | 64 / 2 | 4 | 0.5255 .. 4.23 | -1.86% / -0.02% / +0.00% | -1.69% .. +0.00% | +0.0000 .. +0.0040 | 24/24 |
| worked p4g2_044, legacy (0c133190) | pipeline check (scripted) | 8 | 64 / 2 | 8 | 0.8271 .. 1.085 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 8/8 |
| worked p4g2_044, legacy (0c133190) | reference demo (persistence, 4 members) | 3 | 4 / 2 | 3 | 0.8271 .. 0.8271 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 3/3 |
| bf legacy (7a28b7b8) | agent rollout | 1 | 64 / 2 | 0 | 0.4968 .. 0.4968 | -0.00% / -0.00% / -0.00% | -0.00% .. -0.00% | +0.0000 .. +0.0000 | 1/1 |
| bf legacy (7a28b7b8) | pipeline check (scripted) | 1 | 64 / 2 | 1 | 0.46 .. 0.46 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 1/1 |
| bf legacy (7a28b7b8) | reference demo (persistence, 4 members) | 1 | 4 / 2 | 1 | 0.46 .. 0.46 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 1/1 |
| xv legacy (8e711a8a) | agent rollout | 1 | 64 / 2 | 0 | 0.1842 .. 0.1842 | -0.00% / -0.00% / -0.00% | -0.01% .. -0.01% | +0.0000 .. +0.0000 | 1/1 |
| xv legacy (8e711a8a) | reference demo (persistence, 4 members) | 1 | 4 / 2 | 1 | 0.4299 .. 0.4299 | +0.00% / +0.00% / +0.00% | +0.00% .. +0.00% | +0.0000 .. +0.0000 | 1/1 |
| bf (38d159a8) | control: controls_bf_centered_v2 | 5 | 4 / 2 | 1 | 0.002212 .. 0.497 | -20.23% / -0.25% / +0.00% | -20.11% .. +0.00% | +0.0000 .. +0.0008 | 5/5 |
| xv (440472fb) | control: controls_xv_centered_v2 | 5 | 4 / 2 | 1 | 0.002068 .. 0.536 | -16.39% / -0.24% / +0.00% | -17.89% .. +0.00% | +0.0000 .. +0.0005 | 5/5 |
| p4g2_044 (0a1aa909) | control: controls_p4g2_044_centered_v2 | 5 | 4 / 2 | 1 | 0.001357 .. 2.136 | -24.33% / -0.01% / +0.00% | -19.76% .. +0.00% | +0.0000 .. +0.0002 | 5/5 |
| bf legacy (7a28b7b8) | control: controls_bf_legacy | 5 | 4 / 2 | 1 | 0.001958 .. 0.5317 | -20.63% / -0.17% / +0.00% | -20.53% .. +0.00% | +0.0000 .. +0.0009 | 5/5 |
| xv legacy (8e711a8a) | control: controls_xv_legacy | 5 | 4 / 2 | 1 | 0.002709 .. 0.6227 | -13.25% / -0.16% / +0.00% | -15.79% .. +0.00% | +0.0000 .. +0.0005 | 5/5 |
| bf (38d159a8) | calibration: reward_calibration_bf | 3 | 4,16,64 / 2 | 0 | 0.001793 .. 0.002248 | -20.70% / -5.79% / -1.52% | -20.79% .. -1.51% | +0.0000 .. +0.0000 | 3/3 |
| xv (440472fb) | calibration: reward_calibration_xv | 3 | 4,16,64 / 2 | 0 | 0.001681 .. 0.002141 | -16.84% / -5.48% / -1.41% | -17.69% .. -1.45% | +0.0000 .. +0.0000 | 3/3 |
| p4g2_044 (0a1aa909) | calibration: reward_calibration_p4g2_044 | 3 | 4,16,64 / 2 | 0 | 0.001252 .. 0.001377 | -19.89% / -6.04% / -1.57% | -17.05% .. -1.51% | +0.0000 .. +0.0000 | 3/3 |
| worked p4g2_044, legacy (0c133190) | control: worked_example_predictor_sanity | 13 | 4 / 2 | 4 | 0.001775 .. 1.085 | -55.77% / -0.03% / +0.00% | -52.77% .. +0.00% | +0.0000 .. +0.1771 | 13/13 |
| worked p4g2_044, legacy (0c133190) | calibration: worked_example_predictor_sanity | 3 | 1,2,4 / 2 | 0 | 0.001775 .. 0.002284 | -23.95% / -19.43% / -14.91% | - .. - | +0.0000 .. +0.0000 | 3/3 |
| worked p4g2_044, legacy (0c133190) | reference: worked_example_native_validation | 3 | 1,3,6 / 2 | 0 | 0.001589 .. 1.085 | -17.05% / +0.00% / +0.00% | - .. - | +0.0000 .. +0.0000 | 3/3 |

## 2. Agent rollouts (all runs with saved forecasts)

### fedvortex (lab, 66b6c134)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | labworld-runs | qwen/qwen3.5-9b | 64/2 | 15/15 | 349.83276 | 349.83276 | 0 | +0.00% | +0.0%..+0.0% | 0.28156 | 0.28156 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 1 | labworld-runs | openai/gpt-6-astra | 64/2 | 15/15 | 0.10660618 | 0.10596575 | -6.4e-04 | -0.60% | -0.9%..-0.4% | 0.0022391 | 0.0022179 | -0.94% | 0.4861 | 0.4874 | +0.0013 | yes |

### bf (38d159a8)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | bf-case-study-20261006 | anthropic/claude-opus-5.5 | 64/2 | 15/15 | 0.01144735 | 0.011366086 | -8.1e-05 | -0.71% | -1.2%..-0.5% | 0.0024255 | 0.0024065 | -0.78% | 0.9706 | 0.9722 | +0.0015 | ulp (x86_64 grade) |
| 10 | bf-case-study-20261006 | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.12910478 | 0.12677527 | -0.00233 | -1.80% | -3.6%..-0.5% | 0.020567 | 0.020239 | -1.59% | 0.4445 | 0.4485 | +0.0040 | yes |
| 11 | bf-case-study-20261006 | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.23273192 | 0.23273192 | 0 | +0.00% | +0.0%..+0.0% | 0.041147 | 0.041147 | +0.00% | 0.3166 | 0.3166 | +0.0000 | ulp (x86_64 grade) |
| 12 | bf-case-study-20261006 | openai/gpt-6-astra | 64/2 | 15/15 | 0.0065317333 | 0.0064840894 | -4.8e-05 | -0.73% | -1.3%..-0.4% | 0.0010402 | 0.0010319 | -0.80% | 1.0000 | 1.0000 | +0.0000 | yes |
| 14 | bf-case-study-20261006 | openai/gpt-6-luna | 64/2 | 15/15 | 0.15898078 | 0.15893962 | -4.1e-05 | -0.03% | -1.3%..-0.0% | 0.033487 | 0.033479 | -0.02% | 0.3993 | 0.3994 | +0.0001 | yes |
| 15 | bf-case-study-20261006 | openai/gpt-6.1-sol | 64/2 | 15/15 | 0.0089691619 | 0.0089432953 | -2.6e-05 | -0.29% | -1.8%..-0.1% | 0.0012924 | 0.0012873 | -0.40% | 1.0000 | 1.0000 | +0.0000 | yes |
| 16 | bf-case-study-20261006 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.4446408 | 0.4412826 | -0.00336 | -0.76% | -0.9%..-0.5% | 0.16405 | 0.16256 | -0.91% | 0.1760 | 0.1776 | +0.0016 | yes |
| 17 | bf-case-study-20261006 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.61282268 | 0.61278973 | -3.3e-05 | -0.01% | -0.0%..-0.0% | 0.3438 | 0.3438 | -0.00% | 0.1063 | 0.1063 | +0.0000 | yes |
| 18 | bf-case-study-20261006 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.35415656 | 0.35348875 | -6.7e-04 | -0.19% | -0.3%..-0.1% | 0.15499 | 0.1549 | -0.06% | 0.2254 | 0.2258 | +0.0004 | yes |
| 19 | bf-case-study-20261006 | x-ai/grok-4.6 | 64/2 | 15/15 | 1.857569 | 1.857569 | 0 | +0.00% | +0.0%..+0.0% | 0.34238 | 0.34238 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 3 | bf-case-study-20261006-preflight | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.49700867 | 0.49700867 | 0 | +0.00% | +0.0%..+0.0% | 0.10592 | 0.10592 | +0.00% | 0.1518 | 0.1518 | +0.0000 | yes |
| 4 | bf-case-study-20261006-preflight | openai/gpt-6-luna | 64/2 | 15/15 | 0.49700867 | 0.49700867 | 0 | +0.00% | +0.0%..+0.0% | 0.10592 | 0.10592 | +0.00% | 0.1518 | 0.1518 | +0.0000 | yes |
| 5 | bf-case-study-20261006-preflight | anthropic/claude-opus-5.5 | 64/2 | 15/15 | 0.49700867 | 0.49700867 | 0 | +0.00% | +0.0%..+0.0% | 0.10592 | 0.10592 | +0.00% | 0.1518 | 0.1518 | +0.0000 | ulp (x86_64 grade) |
| 6 | bf-case-study-20261006-preflight | anthropic/claude-opus-5.5 | 64/2 | 15/15 | 0.49700867 | 0.49700867 | 0 | +0.00% | +0.0%..+0.0% | 0.10592 | 0.10592 | +0.00% | 0.1518 | 0.1518 | +0.0000 | ulp (x86_64 grade) |
| 7 | bf-case-study-20261006-preflight | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.49700867 | 0.49700867 | 0 | +0.00% | +0.0%..+0.0% | 0.10592 | 0.10592 | +0.00% | 0.1518 | 0.1518 | +0.0000 | ulp (x86_64 grade) |
| 28 | evaluation-campaign-20260916 | deepseek/deepseek-v4.1-flash | 64/2 | 15/15 | 0.11178392 | 0.11176156 | -2.2e-05 | -0.02% | -1.1%..-0.0% | 0.022109 | 0.022102 | -0.03% | 0.4758 | 0.4759 | +0.0000 | yes |
| 29 | evaluation-campaign-20260916 | openai/gpt-5.6-luna | 64/2 | 15/15 | 0.33197218 | 0.33194129 | -3.1e-05 | -0.01% | -0.0%..-0.0% | 0.084969 | 0.08496 | -0.01% | 0.2394 | 0.2395 | +0.0000 | yes |
| 32 | evaluation-campaign-20260916 | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.18746106 | 0.18744162 | -1.9e-05 | -0.01% | -0.3%..-0.0% | 0.047014 | 0.047008 | -0.01% | 0.3635 | 0.3636 | +0.0000 | yes |
| 34 | evaluation-campaign-20260916 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.60279092 | 0.6025832 | -2.1e-04 | -0.03% | -0.0%..-0.0% | 0.15104 | 0.15066 | -0.25% | 0.1099 | 0.1100 | +0.0001 | yes |
| 37 | evaluation-campaign-20260916 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.23515859 | 0.23181953 | -0.00334 | -1.42% | -3.6%..-0.7% | 0.040708 | 0.040266 | -1.09% | 0.3143 | 0.3174 | +0.0031 | yes |
| 40 | evaluation-campaign-20260916 | x-ai/grok-4.6 | 64/2 | 15/15 | 0.28935444 | 0.28934678 | -7.7e-06 | -0.00% | -0.0%..-0.0% | 0.092312 | 0.092309 | -0.00% | 0.2693 | 0.2693 | +0.0000 | yes |
| 43 | evaluation-campaign-20260916 | z-ai/glm-5.3-flash | 64/2 | 15/15 | 0.15269884 | 0.15235635 | -3.4e-04 | -0.22% | -2.1%..-0.1% | 0.033301 | 0.033266 | -0.11% | 0.4081 | 0.4086 | +0.0005 | yes |
| 58 | evaluation-campaign-20260918-interface-v2 | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.22214017 | 0.21550808 | -0.00663 | -2.99% | -3.6%..-1.5% | 0.023025 | 0.022426 | -2.60% | 0.3267 | 0.3333 | +0.0066 | yes |
| 61 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-luna | 64/2 | 14/15 | 0.19042852 (valid-case mean; primary None, INVALID_PREDICTIONS) | 0.18854699 | -0.00188 | -0.99% | -2.4%..+0.0% | 0.032189 | 0.032008 | -0.56% | 0.0000 | 0.0000 | +0.0000 | yes (cases; primary None) |
| 64 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.1574103 | 0.1574103 | 0 | +0.00% | +0.0%..+0.0% | 0.031324 | 0.031324 | +0.00% | 0.4015 | 0.4015 | +0.0000 | yes |
| 67 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.38651955 | 0.38123644 | -0.00528 | -1.37% | -1.5%..-0.8% | 0.13451 | 0.13244 | -1.53% | 0.2064 | 0.2094 | +0.0030 | yes |
| 70 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.1741051 | 0.17403832 | -6.7e-05 | -0.04% | -1.6%..-0.0% | 0.038658 | 0.038649 | -0.02% | 0.3796 | 0.3797 | +0.0001 | yes |
| 73 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.7-flash | 64/2 | 15/15 | 0.51343702 | 0.51343041 | -6.6e-06 | -0.00% | -0.0%..-0.0% | 0.17526 | 0.17526 | -0.00% | 0.1448 | 0.1448 | +0.0000 | yes |
| 74 | evaluation-campaign-20260918-interface-v2 | x-ai/grok-4.6 | 64/2 | 15/15 | 0.16408039 | 0.16408039 | 0 | +0.00% | +0.0%..+0.0% | 0.032799 | 0.032799 | +0.00% | 0.3925 | 0.3925 | +0.0000 | yes |
| 77 | evaluation-campaign-20260918-interface-v2 | z-ai/glm-5.3-flash | 64/2 | 15/15 | 0.16159286 | 0.16151505 | -7.8e-05 | -0.05% | -0.3%..-0.0% | 0.033518 | 0.033506 | -0.04% | 0.3958 | 0.3959 | +0.0001 | yes |
| 83 | evaluation-campaign-20260919-prime-agent-bf | openai/gpt-5.6-luna | 64/2 | 15/15 | 0.14425155 | 0.14422794 | -2.4e-05 | -0.02% | -0.8%..-0.0% | 0.035376 | 0.035372 | -0.01% | 0.4204 | 0.4205 | +0.0000 | yes |
| 84 | evaluation-campaign-20260919-prime-agent-bf | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.3025852 | 0.3025852 | 0 | +0.00% | +0.0%..+0.0% | 0.053307 | 0.053307 | +0.00% | 0.2596 | 0.2596 | +0.0000 | yes |
| 85 | evaluation-campaign-20260919-prime-agent-bf | qwen/qwen3.5-35b-a3b | 64/2 | 11/15 | 1.9834172 (valid-case mean; primary None, INVALID_PREDICTIONS) | 1.9821092 | -0.00131 | -0.07% | -0.1%..-0.1% | 0.12204 | 0.12191 | -0.10% | 0.0000 | 0.0000 | +0.0000 | yes (cases; primary None) |
| 86 | evaluation-campaign-20260919-prime-agent-bf | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.96222144 | 0.96215466 | -6.7e-05 | -0.01% | -1.7%..-0.0% | 0.066095 | 0.066086 | -0.01% | 0.0084 | 0.0084 | +0.0000 | yes |
| 87 | evaluation-campaign-20260919-prime-agent-bf | x-ai/grok-4.6 | 64/2 | 15/15 | 0.15773178 | 0.15769438 | -3.7e-05 | -0.02% | -1.5%..-0.0% | 0.034885 | 0.034874 | -0.03% | 0.4010 | 0.4011 | +0.0001 | yes |
| 81 | evaluation-campaign-20260919-prime-agent-bf-retries | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.15904388 | 0.15804715 | -1.0e-03 | -0.63% | -2.0%..-0.3% | 0.034975 | 0.034696 | -0.80% | 0.3992 | 0.4006 | +0.0014 | yes |
| 82 | evaluation-campaign-20260919-prime-agent-bf-retries | z-ai/glm-5.3-flash | 64/2 | 15/15 | 0.10119301 | 0.1004596 | -7.3e-04 | -0.72% | -2.5%..-0.3% | 0.02119 | 0.021091 | -0.47% | 0.4974 | 0.4990 | +0.0016 | yes |
| 118 | residency-environments-pr22 | Qwen/Qwen3.5-122B-A10B | 64/2 | 15/15 | 0.36365998 | 0.3635932 | -6.7e-05 | -0.02% | -0.0%..-0.0% | 0.063084 | 0.063075 | -0.01% | 0.2197 | 0.2197 | +0.0000 | yes |
| 119 | residency-environments-pr22 | Qwen/Qwen3.5-9B | 64/2 | 15/15 | 2.267973 | 2.267973 | 0 | +0.00% | +0.0%..+0.0% | 0.44875 | 0.44875 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 120 | residency-environments-pr22 | Qwen/Qwen3.5-122B-A10B | 64/2 | 15/15 | 4.2616223 | 4.2615089 | -1.1e-04 | -0.00% | -0.0%..-0.0% | 0.38034 | 0.38033 | -0.00% | 0.0000 | 0.0000 | +0.0000 | yes |

### xv (440472fb)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 31 | evaluation-campaign-20260916 | openai/gpt-5.6-luna | 64/2 | 15/15 | 0.1758104 | 0.17579139 | -1.9e-05 | -0.01% | -0.7%..-0.0% | 0.029643 | 0.02964 | -0.01% | 0.3775 | 0.3775 | +0.0000 | yes |
| 33 | evaluation-campaign-20260916 | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.1383296 | 0.1383186 | -1.1e-05 | -0.01% | -0.4%..-0.0% | 0.024552 | 0.024547 | -0.02% | 0.4295 | 0.4296 | +0.0000 | yes |
| 36 | evaluation-campaign-20260916 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.39937383 | 0.39332856 | -0.00605 | -1.51% | -1.8%..-1.4% | 0.14298 | 0.14072 | -1.58% | 0.1993 | 0.2026 | +0.0033 | yes |
| 39 | evaluation-campaign-20260916 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.22818387 | 0.2240324 | -0.00415 | -1.82% | -3.6%..-1.4% | 0.061678 | 0.060282 | -2.26% | 0.3209 | 0.3248 | +0.0040 | yes |
| 42 | evaluation-campaign-20260916 | x-ai/grok-4.6 | 64/2 | 15/15 | 0.17264718 | 0.17162695 | -0.00102 | -0.59% | -1.6%..-0.2% | 0.029693 | 0.029336 | -1.20% | 0.3814 | 0.3827 | +0.0013 | yes |
| 45 | evaluation-campaign-20260916 | z-ai/glm-5.3-flash | 64/2 | 15/15 | 0.10132486 | 0.0996387 | -0.00169 | -1.66% | -4.3%..-0.1% | 0.017543 | 0.017285 | -1.47% | 0.4971 | 0.5008 | +0.0036 | yes |
| 60 | evaluation-campaign-20260918-interface-v2 | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.15903602 | 0.15750379 | -0.00153 | -0.96% | -3.3%..-0.3% | 0.028506 | 0.02808 | -1.49% | 0.3993 | 0.4014 | +0.0021 | yes |
| 63 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-luna | 64/2 | 15/15 | 0.30257177 | 0.30255566 | -1.6e-05 | -0.01% | -1.1%..-0.0% | 0.045566 | 0.045563 | -0.01% | 0.2596 | 0.2596 | +0.0000 | yes |
| 66 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-terra | 64/2 | 15/15 | 0.19805246 | 0.19805246 | 0 | +0.00% | +0.0%..+0.0% | 0.040451 | 0.040451 | +0.00% | 0.3516 | 0.3516 | +0.0000 | yes |
| 69 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 0.55562178 | 0.55548341 | -1.4e-04 | -0.02% | -0.0%..-0.0% | 0.1655 | 0.16541 | -0.05% | 0.1276 | 0.1277 | +0.0001 | yes |
| 72 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 2.7357377 | 2.7356685 | -6.9e-05 | -0.00% | -0.0%..-0.0% | 0.37502 | 0.37497 | -0.01% | 0.0000 | 0.0000 | +0.0000 | yes |
| 76 | evaluation-campaign-20260918-interface-v2 | x-ai/grok-4.6 | 64/2 | 15/15 | 0.17602561 | 0.17602146 | -4.2e-06 | -0.00% | -0.2%..-0.0% | 0.032094 | 0.032092 | -0.01% | 0.3772 | 0.3772 | +0.0000 | yes |
| 79 | evaluation-campaign-20260918-interface-v2 | z-ai/glm-5.3-flash | 64/2 | 15/15 | 0.28511443 | 0.28509103 | -2.3e-05 | -0.01% | -0.7%..-0.0% | 0.17999 | 0.17999 | -0.00% | 0.2725 | 0.2725 | +0.0000 | yes |

### p4g2_044 (0a1aa909)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | evaluation-campaign-20260916 | openai/gpt-5.6-luna | 64/2 | 19/19 | 1.7643549 | 1.7643516 | -3.3e-06 | -0.00% | -1.1%..-0.0% | 0.35946 | 0.35946 | -0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 35 | evaluation-campaign-20260916 | qwen/qwen3.5-35b-a3b | 64/2 | 19/19 | 0.88609942 | 0.88510647 | -9.9e-04 | -0.11% | -0.9%..-0.0% | 0.30556 | 0.30512 | -0.15% | 0.0263 | 0.0265 | +0.0002 | yes |
| 38 | evaluation-campaign-20260916 | qwen/qwen3.5-397b-a17b | 64/2 | 19/19 | 0.80926467 | 0.80922251 | -4.2e-05 | -0.01% | -0.3%..-0.0% | 0.24056 | 0.24054 | -0.01% | 0.0460 | 0.0460 | +0.0000 | yes |
| 41 | evaluation-campaign-20260916 | x-ai/grok-4.6 | 64/2 | 19/19 | 5.4341882 | 5.4341576 | -3.1e-05 | -0.00% | -3.1%..-0.0% | 0.97257 | 0.97255 | -0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 44 | evaluation-campaign-20260916 | z-ai/glm-5.3-flash | 64/2 | 19/19 | 0.61492686 | 0.61492686 | 0 | +0.00% | +0.0%..+0.0% | 0.13202 | 0.13202 | +0.00% | 0.1056 | 0.1056 | +0.0000 | yes |
| 59 | evaluation-campaign-20260918-interface-v2 | anthropic/claude-sonnet-5 | 64/2 | 19/19 | 3.1981291 | 3.1434102 | -0.0547 | -1.71% | -3.6%..-0.1% | 0.56221 | 0.55225 | -1.77% | 0.0000 | 0.0000 | +0.0000 | yes |
| 62 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-luna | 64/2 | 19/19 | 0.6582296 | 0.65804679 | -1.8e-04 | -0.03% | -0.6%..+0.0% | 0.16463 | 0.1643 | -0.20% | 0.0908 | 0.0909 | +0.0001 | yes |
| 65 | evaluation-campaign-20260918-interface-v2 | openai/gpt-5.6-terra | 64/2 | 19/19 | 0.63428209 | 0.63366024 | -6.2e-04 | -0.10% | -1.0%..+0.0% | 0.12821 | 0.12811 | -0.08% | 0.0989 | 0.0991 | +0.0002 | yes |
| 68 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-35b-a3b | 64/2 | 19/19 | 0.71289202 | 0.71282833 | -6.4e-05 | -0.01% | -0.4%..-0.0% | 0.2994 | 0.29938 | -0.01% | 0.0735 | 0.0735 | +0.0000 | yes |
| 71 | evaluation-campaign-20260918-interface-v2 | qwen/qwen3.5-397b-a17b | 64/2 | 19/19 | 0.64189116 | 0.64189116 | 0 | +0.00% | +0.0%..+0.0% | 0.14303 | 0.14303 | +0.00% | 0.0963 | 0.0963 | +0.0000 | yes |
| 75 | evaluation-campaign-20260918-interface-v2 | x-ai/grok-4.6 | 64/2 | 19/19 | 6.7052293 | 6.7052261 | -3.2e-06 | -0.00% | -1.6%..+0.0% | 6.4422 | 6.4422 | -0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 78 | evaluation-campaign-20260918-interface-v2 | z-ai/glm-5.3-flash | 64/2 | 19/19 | 0.53079209 | 0.53079209 | 0 | +0.00% | +0.0%..+0.0% | 0.15118 | 0.15118 | +0.00% | 0.1375 | 0.1375 | +0.0000 | yes |
| 91 | p4-astra-20261007 | openai/gpt-6-astra | 64/2 | 19/19 | 0.026673256 | 0.026510454 | -1.6e-04 | -0.61% | -1.8%..-0.3% | 0.0061968 | 0.0061658 | -0.50% | 0.7870 | 0.7883 | +0.0013 | ulp (x86_64 grade) |
| 90 | p4-astra-20261007-preflight | openai/gpt-6-astra | 64/2 | 19/19 | 0.87299057 | 0.87299057 | 0 | +0.00% | +0.0%..+0.0% | 0.25218 | 0.25218 | +0.00% | 0.0295 | 0.0295 | +0.0000 | ulp (x86_64 grade) |

### worked p4g2_044, legacy (0c133190)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 129 | r6-worked-example/runs | deepseek_flash_v2 | 64/2 | 15/15 | 0.68655718 | 0.68655474 | -2.4e-06 | -0.00% | -0.0%..-0.0% | 0.15088 | 0.15088 | -0.00% | 0.0817 | 0.0817 | +0.0000 | yes |
| 130 | r6-worked-example/runs | glm47_flash_v4 | 64/2 | 15/15 | 0.67301817 | 0.6718812 | -0.00114 | -0.17% | -1.3%..-0.1% | 0.14307 | 0.14263 | -0.31% | 0.0860 | 0.0864 | +0.0004 | yes |
| 131 | r6-worked-example/runs | qwen27b_v2_budget090 | 64/2 | 15/15 | 1.7910203 | 1.7909959 | -2.4e-05 | -0.00% | -0.0%..-0.0% | 0.73983 | 0.73982 | -0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 132 | r6-worked-example/runs | qwen35b_a3b_v2_recovery | 64/2 | 15/15 | 0.80268334 | 0.80246501 | -2.2e-04 | -0.03% | -0.0%..-0.0% | 0.24351 | 0.24334 | -0.07% | 0.0477 | 0.0478 | +0.0001 | yes |
| 133 | r6-worked-example/runs | diagnostic_noncompliant | 64/2 | 15/15 | 0.86409446 | 0.8617276 | -0.00237 | -0.27% | -0.8%..-0.1% | 0.41124 | 0.41031 | -0.23% | 0.0317 | 0.0323 | +0.0006 | yes |
| 134 | r6-worked-example/runs | qwen9b_v4 | 64/2 | 15/15 | 2.294695 | 2.294695 | 0 | +0.00% | +0.0%..+0.0% | 3.1636 | 3.1636 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 135 | r6-worked-example/runtime_v5 | qwen36_35b_a3b_v5_delivery | 64/2 | 15/15 | 0.90165107 | 0.90141638 | -2.3e-04 | -0.03% | -0.1%..-0.0% | 0.35136 | 0.35119 | -0.05% | 0.0225 | 0.0225 | +0.0001 | yes |
| 137 | r6-worked-example/verifiers_highlimits_v1 | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.52547674 | 0.5254737 | -3.0e-06 | -0.00% | -0.0%..-0.0% | 0.13461 | 0.13461 | -0.00% | 0.1397 | 0.1397 | +0.0000 | yes |
| 138 | r6-worked-example/verifiers_highlimits_v1 | deepseek/deepseek-v4-pro | 64/2 | 15/15 | 0.55325805 | 0.55315882 | -9.9e-05 | -0.02% | -0.2%..-0.0% | 0.21478 | 0.21474 | -0.02% | 0.1285 | 0.1286 | +0.0000 | yes |
| 139 | r6-worked-example/verifiers_highlimits_v1 | Qwen/Qwen3.5-122B-A10B | 64/2 | 15/15 | 1.2927006 | 1.2922125 | -4.9e-04 | -0.04% | -0.7%..-0.0% | 0.38788 | 0.3877 | -0.05% | 0.0000 | 0.0000 | +0.0000 | yes |
| 140 | r6-worked-example/verifiers_highlimits_v1 | openai/gpt-5.6-terra | 64/2 | 15/15 | 4.2295687 | 4.2295687 | 0 | +0.00% | +0.0%..+0.0% | 0.77152 | 0.77152 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 141 | r6-worked-example/verifiers_highlimits_v1 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.54190516 | 0.53488635 | -0.00702 | -1.30% | -2.5%..-1.1% | 0.17496 | 0.17201 | -1.69% | 0.1330 | 0.1359 | +0.0028 | yes |
| 142 | r6-worked-example/verifiers_scaling_v1 | deepseek/deepseek-v4-pro | 64/2 | 15/15 | 0.68710308 | 0.68710234 | -7.4e-07 | -0.00% | -0.0%..-0.0% | 0.14847 | 0.14847 | -0.00% | 0.0815 | 0.0815 | +0.0000 | yes |
| 143 | r6-worked-example/verifiers_scaling_v1 | anthropic/claude-sonnet-5 | 64/2 | 15/15 | 0.83269374 | 0.83255515 | -1.4e-04 | -0.02% | -0.0%..-0.0% | 0.18086 | 0.18077 | -0.05% | 0.0398 | 0.0398 | +0.0000 | yes |
| 144 | r6-worked-example/verifiers_scaling_v1 | openai/gpt-5.6-terra | 64/2 | 9/15 | 0.57953936 (valid-case mean; primary None, INVALID_PREDICTIONS) | 0.57953936 | 0 | +0.00% | +0.0%..+0.0% | 0.086642 | 0.086642 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes (cases; primary None) |
| 145 | r6-worked-example/verifiers_scaling_v1 | Qwen/Qwen3.5-122B-A10B | 64/2 | 15/15 | 0.74852494 | 0.74714383 | -0.00138 | -0.18% | -0.6%..-0.1% | 0.21486 | 0.21434 | -0.25% | 0.0629 | 0.0633 | +0.0004 | yes |
| 146 | r6-worked-example/verifiers_scaling_v1 | qwen/qwen3.5-397b-a17b | 64/2 | 15/15 | 0.91861579 | 0.90166215 | -0.017 | -1.85% | -2.7%..-1.1% | 0.3772 | 0.37104 | -1.63% | 0.0184 | 0.0225 | +0.0040 | yes |
| 147 | r6-worked-example/verifiers_scaling_v1 | openai/gpt-5.6-sol | 64/2 | 15/15 | 3.1901887 | 3.1901887 | 0 | +0.00% | +0.0%..+0.0% | 0.61387 | 0.61387 | +0.00% | 0.0000 | 0.0000 | +0.0000 | yes |
| 150 | r6-worked-example/verifiers_v1 | deepseek/deepseek-v4-flash | 64/2 | 15/15 | 0.83490247 | 0.83489488 | -7.6e-06 | -0.00% | -0.0%..-0.0% | 0.34898 | 0.34897 | -0.00% | 0.0392 | 0.0392 | +0.0000 | yes |
| 151 | r6-worked-example/verifiers_v1 | z-ai/glm-4.7-flash | 64/2 | 15/15 | 1.0203487 | 1.0014113 | -0.0189 | -1.86% | -2.7%..-1.2% | 0.46101 | 0.45382 | -1.56% | 0.0000 | 0.0000 | +0.0000 | yes |
| 152 | r6-worked-example/verifiers_v1 | qwen/qwen3.6-27b | 64/2 | 15/15 | 0.77427644 | 0.77426694 | -9.5e-06 | -0.00% | -0.0%..-0.0% | 0.20383 | 0.20383 | -0.00% | 0.0556 | 0.0556 | +0.0000 | yes |
| 153 | r6-worked-example/verifiers_v1 | qwen/qwen3.6-35b-a3b | 64/2 | 15/15 | 0.67922326 | 0.67910123 | -1.2e-04 | -0.02% | -0.2%..-0.0% | 0.32967 | 0.32962 | -0.01% | 0.0840 | 0.0840 | +0.0000 | yes |
| 154 | r6-worked-example/verifiers_v1 | qwen/qwen3.5-35b-a3b | 64/2 | 15/15 | 1.1075051 | 1.107036 | -4.7e-04 | -0.04% | -0.1%..-0.0% | 0.5694 | 0.56923 | -0.03% | 0.0000 | 0.0000 | +0.0000 | yes |
| 155 | r6-worked-example/verifiers_v1 | Qwen/Qwen3.5-9B | 64/2 | 15/15 | 1.4799119 | 1.4680575 | -0.0119 | -0.80% | -1.0%..-0.6% | 0.53443 | 0.53001 | -0.83% | 0.0000 | 0.0000 | +0.0000 | yes |

### bf legacy (7a28b7b8)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 21 | eval-preparation-20260913/bf | deepseek/deepseek-v4-flash | 64/2 | 11/11 | 0.4967523 | 0.49674674 | -5.6e-06 | -0.00% | -0.0%..-0.0% | 0.089032 | 0.08903 | -0.00% | 0.1519 | 0.1519 | +0.0000 | yes |

### xv legacy (8e711a8a)

| # | Campaign | Model | m/n | Cases | S plugin (= recorded) | S fair | ΔS | ΔS % | Family ΔS % (min..max) | CRPS plugin | CRPS fair | CRPS Δ% | Reward K=2 before | after | Δ | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 23 | eval-preparation-20260913/xv | deepseek/deepseek-v4-flash | 64/2 | 11/11 | 0.1841818 | 0.18417765 | -4.2e-06 | -0.00% | -0.2%..-0.0% | 0.032876 | 0.032873 | -0.01% | 0.3674 | 0.3674 | +0.0000 | yes |

## 3. Controls, references and reward calibration

Ratio = row / independent_native of the same table (worked example: / native_physics). m=1 rows cannot be scored with fair; for validate_native.py's m=1 zero/persistence forecasts the fair column shows the same deterministic forecast broadcast to 2 members (bit-identical to plugin).

| World / bundle | Table | Row | m/n | S plugin (= recorded) | S fair | ΔS % | Family ΔS % (min..max) | CRPS Δ% | Ratio to native, plugin → fair | Reward K=2 before → after | plugin = recorded |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bf (38d159a8) | controls_bf_centered_v2 | independent_native | 4/2 | 0.0022116586 | 0.0017642519 | -20.23% | -31.9%..-12.2% | -20.11% | 1 → 1 | 1.0000 → 1.0000 | yes |
| bf (38d159a8) | controls_bf_centered_v2 | ignore_actions | 4/2 | 0.20224134 | 0.20174187 | -0.25% | -17.8%..-0.1% | -0.26% | 91.44 → 114.3 | 0.3471 → 0.3476 | yes |
| bf (38d159a8) | controls_bf_centered_v2 | remove_feedback | 4/2 | 0.138328 | 0.13781379 | -0.37% | -0.7%..-0.2% | -0.43% | 62.54 → 78.11 | 0.4295 → 0.4304 | yes |
| bf (38d159a8) | controls_bf_centered_v2 | wrong_probe_geometry | 4/2 | 0.46785144 | 0.46743477 | -0.09% | -0.2%..-0.0% | -0.06% | 211.5 → 264.9 | 0.1649 → 0.1651 | yes |
| bf (38d159a8) | controls_bf_centered_v2 | initial_persistence | 4/2 | 0.49700867 | 0.49700867 | +0.00% | +0.0%..+0.0% | +0.00% | 224.7 → 281.7 | 0.1518 → 0.1518 | yes |
| xv (440472fb) | controls_xv_centered_v2 | independent_native | 4/2 | 0.0020677266 | 0.0017289108 | -16.39% | -32.1%..-9.6% | -17.89% | 1 → 1 | 1.0000 → 1.0000 | yes |
| xv (440472fb) | controls_xv_centered_v2 | ignore_actions | 4/2 | 0.16378195 | 0.1633898 | -0.24% | -16.4%..-0.1% | -0.24% | 79.21 → 94.5 | 0.3929 → 0.3934 | yes |
| xv (440472fb) | controls_xv_centered_v2 | remove_feedback | 4/2 | 0.16192127 | 0.16151674 | -0.25% | -0.5%..-0.1% | -0.21% | 78.31 → 93.42 | 0.3953 → 0.3959 | yes |
| xv (440472fb) | controls_xv_centered_v2 | wrong_probe_geometry | 4/2 | 0.53598621 | 0.53561477 | -0.07% | -0.2%..-0.0% | -0.05% | 259.2 → 309.8 | 0.1354 → 0.1356 | yes |
| xv (440472fb) | controls_xv_centered_v2 | initial_persistence | 4/2 | 0.42785204 | 0.42785204 | +0.00% | +0.0%..+0.0% | +0.00% | 206.9 → 247.5 | 0.1844 → 0.1844 | yes |
| p4g2_044 (0a1aa909) | controls_p4g2_044_centered_v2 | independent_native | 4/2 | 0.0013570942 | 0.0010268869 | -24.33% | -46.6%..-5.8% | -19.76% | 1 → 1 | 1.0000 → 1.0000 | yes |
| p4g2_044 (0a1aa909) | controls_p4g2_044_centered_v2 | ignore_actions | 4/2 | 0.64302636 | 0.64296805 | -0.01% | -23.5%..-0.0% | -0.02% | 473.8 → 626.1 | 0.0959 → 0.0959 | yes |
| p4g2_044 (0a1aa909) | controls_p4g2_044_centered_v2 | remove_feedback | 4/2 | 2.1358466 | 2.1358069 | -0.00% | -0.0%..-0.0% | -0.00% | 1574 → 2080 | 0.0000 → 0.0000 | yes |
| p4g2_044 (0a1aa909) | controls_p4g2_044_centered_v2 | wrong_probe_geometry | 4/2 | 0.44965974 | 0.44917082 | -0.11% | -0.9%..-0.0% | -0.05% | 331.3 → 437.4 | 0.1736 → 0.1738 | yes |
| p4g2_044 (0a1aa909) | controls_p4g2_044_centered_v2 | initial_persistence | 4/2 | 0.87299057 | 0.87299057 | +0.00% | +0.0%..+0.0% | +0.00% | 643.3 → 850.1 | 0.0295 → 0.0295 | yes |
| bf legacy (7a28b7b8) | controls_bf_legacy | independent_native | 4/2 | 0.0019580999 | 0.0015540477 | -20.63% | -31.9%..-12.5% | -20.53% | 1 → 1 | 1.0000 → 1.0000 | yes |
| bf legacy (7a28b7b8) | controls_bf_legacy | ignore_actions | 4/2 | 0.28897318 | 0.28848369 | -0.17% | -17.8%..-0.1% | -0.17% | 147.6 → 185.6 | 0.2696 → 0.2699 | yes |
| bf legacy (7a28b7b8) | controls_bf_legacy | remove_feedback | 4/2 | 0.11196677 | 0.11152461 | -0.39% | -0.9%..-0.2% | -0.46% | 57.18 → 71.76 | 0.4755 → 0.4763 | yes |
| bf legacy (7a28b7b8) | controls_bf_legacy | wrong_probe_geometry | 4/2 | 0.53169116 | 0.53126481 | -0.08% | -0.1%..-0.0% | -0.06% | 271.5 → 341.9 | 0.1372 → 0.1373 | yes |
| bf legacy (7a28b7b8) | controls_bf_legacy | initial_persistence | 4/2 | 0.46001066 | 0.46001066 | +0.00% | +0.0%..+0.0% | +0.00% | 234.9 → 296 | 0.1686 → 0.1686 | yes |
| xv legacy (8e711a8a) | controls_xv_legacy | independent_native | 4/2 | 0.0027087064 | 0.0023498983 | -13.25% | -26.8%..-5.3% | -15.79% | 1 → 1 | 1.0000 → 1.0000 | yes |
| xv legacy (8e711a8a) | controls_xv_legacy | ignore_actions | 4/2 | 0.18292061 | 0.1825399 | -0.21% | -16.4%..-0.1% | -0.20% | 67.53 → 77.68 | 0.3689 → 0.3693 | yes |
| xv legacy (8e711a8a) | controls_xv_legacy | remove_feedback | 4/2 | 0.23513966 | 0.23476209 | -0.16% | -0.5%..-0.0% | -0.17% | 86.81 → 99.9 | 0.3143 → 0.3147 | yes |
| xv legacy (8e711a8a) | controls_xv_legacy | wrong_probe_geometry | 4/2 | 0.62267504 | 0.62233575 | -0.05% | -0.1%..-0.0% | -0.04% | 229.9 → 264.8 | 0.1029 → 0.1030 | yes |
| xv legacy (8e711a8a) | controls_xv_legacy | initial_persistence | 4/2 | 0.42989783 | 0.42989783 | +0.00% | +0.0%..+0.0% | +0.00% | 158.7 → 182.9 | 0.1833 → 0.1833 | yes |
| bf (38d159a8) | reward_calibration_bf | native first 4 members | 4/2 | 0.0022478162 | 0.0017825397 | -20.70% | - | -20.79% | - | 1.0000 → 1.0000 | yes |
| bf (38d159a8) | reward_calibration_bf | native first 16 members | 16/2 | 0.0018936043 | 0.0017838761 | -5.79% | - | -5.79% | - | 1.0000 → 1.0000 | yes |
| bf (38d159a8) | reward_calibration_bf | native first 64 members | 64/2 | 0.0017934717 | 0.0017662886 | -1.52% | - | -1.51% | - | 1.0000 → 1.0000 | yes |
| xv (440472fb) | reward_calibration_xv | native first 4 members | 4/2 | 0.0021405654 | 0.0017799938 | -16.84% | - | -17.69% | - | 1.0000 → 1.0000 | yes |
| xv (440472fb) | reward_calibration_xv | native first 16 members | 16/2 | 0.0017033227 | 0.0016100163 | -5.48% | - | -5.62% | - | 1.0000 → 1.0000 | yes |
| xv (440472fb) | reward_calibration_xv | native first 64 members | 64/2 | 0.0016809985 | 0.0016573045 | -1.41% | - | -1.45% | - | 1.0000 → 1.0000 | yes |
| p4g2_044 (0a1aa909) | reward_calibration_p4g2_044 | native first 4 members | 4/2 | 0.0013766794 | 0.0011027988 | -19.89% | - | -17.05% | - | 1.0000 → 1.0000 | yes |
| p4g2_044 (0a1aa909) | reward_calibration_p4g2_044 | native first 16 members | 16/2 | 0.0013011027 | 0.0012224853 | -6.04% | - | -6.07% | - | 1.0000 → 1.0000 | yes |
| p4g2_044 (0a1aa909) | reward_calibration_p4g2_044 | native first 64 members | 64/2 | 0.0012524368 | 0.0012327505 | -1.57% | - | -1.51% | - | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | zero | 4/2 | 1.0845873 | 1.0845873 | +0.00% | +0.0%..+0.0% | +0.00% | 610.9 → 717.9 | 0.0000 → 0.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | initial_persistence | 4/2 | 0.82712099 | 0.82712099 | +0.00% | +0.0%..+0.0% | +0.00% | 465.9 → 547.5 | 0.0412 → 0.0412 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | frozen_initial_field | 4/2 | 0.82053744 | 0.82053744 | +0.00% | +0.0%..+0.0% | +0.00% | 462.1 → 543.1 | 0.0430 → 0.0430 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | physics_25pct | 4/2 | 0.61522774 | 0.61516156 | -0.01% | -0.0%..-0.0% | -0.01% | 346.5 → 407.2 | 0.1055 → 0.1055 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | physics_50pct | 4/2 | 0.40992202 | 0.40978964 | -0.03% | -0.1%..-0.0% | -0.02% | 230.9 → 271.3 | 0.1936 → 0.1937 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | physics_75pct | 4/2 | 0.20463214 | 0.20443358 | -0.10% | -0.2%..-0.0% | -0.07% | 115.3 → 135.3 | 0.3445 → 0.3447 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | native_physics | 4/2 | 0.0017754838 | 0.0015107391 | -14.91% | -23.7%..-13.1% | -14.77% | 1 → 1 | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | ignore_later_pulses | 4/2 | 0.10418304 | 0.1039311 | -0.24% | -23.7%..-0.1% | -0.51% | 58.68 → 68.79 | 0.4911 → 0.4916 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | ignore_probe_moves | 4/2 | 0.26539211 | 0.26520783 | -0.07% | -23.7%..-0.0% | -0.06% | 149.5 → 175.5 | 0.2881 → 0.2882 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | five_unit_time_grid | 4/2 | 0.082653506 | 0.082394104 | -0.31% | -23.7%..-0.1% | -0.31% | 46.55 → 54.54 | 0.5414 → 0.5421 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | spatially_flat | 4/2 | 0.33809315 | 0.33798493 | -0.03% | -0.0%..-0.0% | -0.02% | 190.4 → 223.7 | 0.2355 → 0.2356 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | ensemble_mean | 4/2 | 0.002177371 | 0.002177371 | +0.00% | +0.0%..+0.0% | +0.00% | 1.226 → 1.441 | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity | spread_x100 | 4/2 | 0.047472079 | 0.020997605 | -55.77% | -60.9%..-51.3% | -52.77% | 26.74 → 13.9 | 0.6618 → 0.8389 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity/native_member_prefix | native_physics first 1 members (note) | 1/2 | 0.0022837272 | n/a (m=1) | - | - | - | - | 1.0000 → - | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity/native_member_prefix | native_physics first 2 members | 2/2 | 0.0021672539 | 0.0016481413 | -23.95% | - | - | - | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_predictor_sanity/native_member_prefix | native_physics first 4 members | 4/2 | 0.0017754838 | 0.0015107391 | -14.91% | - | - | - | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_native_validation | historical_experiment_reference | 3,6/2 | 0.001588521 | 0.0013177292 | -17.05% | - | - | - | 1.0000 → 1.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_native_validation | zero (note) | 1/2 | 1.0845873 | 1.0845873 | +0.00% | - | - | - | 0.0000 → 0.0000 | yes |
| worked p4g2_044, legacy (0c133190) | worked_example_native_validation | initial_persistence (note) | 1/2 | 0.82712099 | 0.82712099 | +0.00% | - | - | - | 0.0412 → 0.0412 | yes |

## 4. Zero-spread pipeline checks and reference demos

| World / bundle | Row kind | Runs | m | Distinct S values (plugin = fair, bit for bit) | Marginal CRPS (plugin = fair) | plugin = recorded |
|---|---|---|---|---|---|---|
| bf (38d159a8) | pipeline check (scripted) | 27 | 64 | 0.49700866885207146 | 0.105917 | 27/27 |
| bf (38d159a8) | preflight agent probe | 5 | 64 | 0.49700866885207146 | 0.105917 | 2/5 (+3 ulp-level, x86_64 grades) |
| bf (38d159a8) | preflight reference | 1 | 64 | 0.49700866885207146 | 0.105917 | 1/1 |
| bf (38d159a8) | reference demo (persistence, 4 members) | 4 | 4 | 0.4970086688520715 | 0.105917 | 4/4 |
| xv (440472fb) | pipeline check (scripted) | 10 | 64 | 0.42785203746391254 | 0.0707525 | 10/10 |
| xv (440472fb) | reference demo (persistence, 4 members) | 3 | 4 | 0.4278520374639126 | 0.0707525 | 3/3 |
| p4g2_044 (0a1aa909) | pipeline check (scripted) | 7 | 64 | 0.8729905732429272 | 0.252185 | 7/7 |
| p4g2_044 (0a1aa909) | preflight agent probe | 1 | 64 | 0.8729905732429272 | 0.252185 | 0/1 (+1 ulp-level, x86_64 grades) |
| p4g2_044 (0a1aa909) | preflight reference | 1 | 4 | 0.8729905732429272 | 0.252185 | 1/1 |
| p4g2_044 (0a1aa909) | reference demo (persistence, 4 members) | 3 | 4 | 0.8729905732429272 | 0.252185 | 3/3 |
| worked p4g2_044, legacy (0c133190) | pipeline check (scripted) | 8 | 64 | 0.8271209896216252, 1.0845872705112614 | 0.256564, 0.563055 | 8/8 |
| worked p4g2_044, legacy (0c133190) | reference demo (persistence, 4 members) | 3 | 4 | 0.8271209896216252 | 0.256564 | 3/3 |
| bf legacy (7a28b7b8) | pipeline check (scripted) | 1 | 64 | 0.46001066377541483 | 0.0998629 | 1/1 |
| bf legacy (7a28b7b8) | reference demo (persistence, 4 members) | 1 | 4 | 0.46001066377541483 | 0.0998629 | 1/1 |
| xv legacy (8e711a8a) | reference demo (persistence, 4 members) | 1 | 4 | 0.4298978335198635 | 0.0729276 | 1/1 |

## 5. Partial items

| Item | Bundle | m | Cases scored | S plugin | S fair | Δ% | Provenance |
|---|---|---|---|---|---|---|---|
| 008_terra_cloud_migration (terra-cloud-migration/659dd54a) | 38d159a8 | 64 | 3/15 | 0.4554985 | 0.4554985 | +0.00% | no grade.json and no forecast manifest: forecasts unverified, nothing recorded to reproduce |
| 013_luna_attempt1 (openai--gpt-6-luna-bf-r1-attempt1/4fea4ff1) | 38d159a8 | 64 | 5/15 | 0.1759614 | 0.17592251 | -0.02% | no grade.json and no forecast manifest: forecasts unverified, nothing recorded to reproduce |
| 117_multiworld_docker (multiworld-docker/fcf78f00) | 38d159a8 | 64 | 3/15 | 0.4554985 | 0.4554985 | +0.00% | no grade.json and no forecast manifest: forecasts unverified, nothing recorded to reproduce |

Eval-calibration scratch suite (`/private/tmp/.../6b9df37f.../eval-calibration/out/suite`, fedvortex kit bundle 66b6c134, true-solver variants). Plugin reproduces every recorded per-case, per-group value of all 35 surviving variants; 5 variants are already purged (estimates in section 9).

| Variant | m | S plugin (= recorded) | S fair | Δ% |
|---|---|---|---|---|
| adv0 | 8 | 5.044396 | 5.041828 | -0.05% |
| astra_coef | 8 | 5.551519 | 5.548012 | -0.06% |
| astra_coef_eat | 8 | 5.584738 | 5.581262 | -0.06% |
| astra_coef_rec02 | 8 | 0.648359 | 0.6439995 | -0.67% |
| astra_coef_rec02_eat | 8 | 0.5283071 | 0.5240022 | -0.81% |
| e_x0.9 | 4 | 1.186242 | 1.17676 | -0.80% |
| e_x0.98 | 4 | 0.214097 | 0.204815 | -4.34% |
| e_x1.02 | 4 | 0.2103523 | 0.2011567 | -4.37% |
| e_x1.1 | 4 | 1.007413 | 0.9983533 | -0.90% |
| hyper0 | 8 | 0.06883074 | 0.06448804 | -6.31% |
| hyper_x0.9 | 4 | 0.04304435 | 0.0338117 | -21.45% |
| hyper_x1.1 | 4 | 0.04320296 | 0.03396083 | -21.39% |
| kF_x0.2 | 8 | 5.526736 | 5.523248 | -0.06% |
| kF_x0.9 | 4 | 0.6893898 | 0.6803817 | -1.31% |
| kF_x0.98 | 4 | 0.1394269 | 0.1302359 | -6.59% |
| kF_x1.02 | 4 | 0.1367425 | 0.1274585 | -6.79% |
| kF_x1.1 | 4 | 0.6841263 | 0.6746578 | -1.38% |
| kY_x0.9 | 4 | 0.731209 | 0.7219795 | -1.26% |
| kY_x0.98 | 4 | 0.1430641 | 0.1338294 | -6.45% |
| kY_x1.02 | 4 | 0.1390555 | 0.1298149 | -6.65% |
| kY_x1.1 | 4 | 0.6733252 | 0.6640685 | -1.37% |
| k_x0.9 | 4 | 3.195058 | 3.186425 | -0.27% |
| k_x0.98 | 4 | 0.6248102 | 0.6156852 | -1.46% |
| k_x1.02 | 4 | 0.6221505 | 0.6127879 | -1.50% |
| k_x1.1 | 4 | 3.224206 | 3.214325 | -0.31% |
| mu_x0.9 | 4 | 3.090144 | 3.079958 | -0.33% |
| mu_x0.98 | 4 | 0.5693837 | 0.5599751 | -1.65% |
| mu_x1.02 | 4 | 0.5592865 | 0.550206 | -1.62% |
| mu_x1.1 | 4 | 2.741265 | 2.732766 | -0.31% |
| nu_x0.9 | 4 | 0.2940524 | 0.2848969 | -3.11% |
| nu_x0.98 | 4 | 0.07296442 | 0.06374512 | -12.64% |
| nu_x1.02 | 4 | 0.07439274 | 0.06513637 | -12.44% |
| nu_x1.1 | 4 | 0.2965059 | 0.2871641 | -3.15% |
| wi_x0.9 | 4 | 1.871526 | 1.861898 | -0.51% |
| wi_x1.1 | 4 | 1.734303 | 1.725365 | -0.52% |

## 6. Theory check

- Energy, per case and group (9954 groups in the runs plus every ensemble row): fair - plugin = -0.5/(m-1) x (mean of RMS(x_i - x_j) over all m*m ordered pairs), with the pair mean computed independently of the scorer. Max abs error 4.50e-15, max rel error 4.44e-10. The scorer's own `_mean_rms_distance(pred, pred)` matches the independent pair mean to 7.1e-15. Per case (2544 case scores): fair - plugin = -0.5/(m-1) x mean over groups of the pair mean, max abs error 5.6e-15.
- Marginal CRPS, per coordinate: fair - plugin = -0.5/(m-1) x time-mean of the all-pairs mean |x_i - x_j|; max abs error 8.28e-15.
- Run level: fair primary = plugin primary - mean over cases of mean over groups of 0.5/(m-1) x pair mean, so every relative change is set by the forecast spread. For a correctly specified ensemble E[S_plugin] = S_fair (m+1)/m: the Blobkit native calibration gives fair/plugin = 0.793/0.942/0.985 at m=4/16/64 (bf) against 0.800/0.941/0.985 predicted.
- Nonnegativity: min fair primary 0.00648409; min fair case energy 0.000214; min fair group energy for a single truth draw 2.68e-08 (>= 0 everywhere, so `precision_reward` never sees a negative energy). Single-truth-draw fair CRPS reaches -1.3e-16 only where forecast and truth coincide exactly (float rounding of 0).

## 7. Rankings

- **agents/bf**: 2 pair(s) change order:
  - openai/gpt-5.6-terra [bf-case-study-20261006#11] vs qwen/qwen3.5-397b-a17b [evaluation-campaign-20260916#37]: plugin 0.2327319 vs 0.2351586; fair 0.2327319 vs 0.2318195
  - openai/gpt-6-luna [bf-case-study-20261006#14] vs anthropic/claude-sonnet-5 [evaluation-campaign-20260919-prime-agent-bf-retries#81]: plugin 0.1589808 vs 0.1590439; fair 0.1589396 vs 0.1580471
- **calibration_member_count/bf**: 1 pair(s) change order:
  - native first 4 members vs native first 16 members: plugin 0.002247816 vs 0.001893604; fair 0.00178254 vs 0.001783876
- **calibration_member_count/xv**: 1 pair(s) change order:
  - native first 16 members vs native first 64 members: plugin 0.001703323 vs 0.001680999; fair 0.001610016 vs 0.001657305
- **calibration_member_count/p4g2_044**: 3 pair(s) change order:
  - native first 4 members vs native first 16 members: plugin 0.001376679 vs 0.001301103; fair 0.001102799 vs 0.001222485
  - native first 4 members vs native first 64 members: plugin 0.001376679 vs 0.001252437; fair 0.001102799 vs 0.001232751
  - native first 16 members vs native first 64 members: plugin 0.001301103 vs 0.001252437; fair 0.001222485 vs 0.001232751
- No order change in: agents/fedvortex, agents/bf legacy, agents/xv legacy, agents/p4, agents/xv, agents/worked-p4 (legacy), agents_vs_controls/bf legacy, agents_vs_controls/worked-p4 (legacy), agents_vs_controls/xv legacy, agents_vs_controls/fedvortex, agents_vs_controls/xv, agents_vs_controls/bf, agents_vs_controls/p4, controls/controls_bf_centered_v2, controls/controls_xv_centered_v2, controls/controls_p4g2_044_centered_v2, controls/controls_bf_legacy, controls/controls_xv_legacy, controls/worked_example_predictor_sanity, controls/worked_example_native_validation.
- Both agent flips are between runs from different campaigns on the same bf bundle and truths, separated by under 1.1%; neither is inside one campaign or one write-up table. The calibration flips are the intended effect: plugin made 4 > 16 > 64 members by construction.

## 8. Rewards, calibration and documented thresholds

- **precision_reward K=2 (README; rewards.py; S=0.01 -> reward 1, S>=1 -> 0)** (assumed old estimator: no): Mapping is estimator-agnostic. Its K came from the integer calibration rule below, which still gives K=2 with fair. Fair S stays >= 0 (min fair primary over all runs 0.00648409; min single-truth-draw fair group energy 2.68e-08), so precision_reward never sees a negative energy.
- **Integer K rule: largest integer K with 10**-K >= 2*max native 64-member suite energy (outputs/reward-calibration-20260926/calibration.json = docs/data/reward-calibration.json)** (assumed old estimator: yes): Unchanged (K=2). The worst native suite energy falls 1.5% (0.0017935 -> 0.0017663); both are well inside (0.001, 0.005].
- **Fractional K = -log10(max native suite energy) (scripts/calibrate_reward.py at HEAD; docs/data/bf-case-study-20261006.json reward_precision)** (assumed old estimator: yes): Moves 2.7463 -> 2.7529. Case-study rewards change by at most 0.0021 (see derived_tables).
- **Calibration ensembles at 4/16/64 members (calibration.json mean_energy)** (assumed old estimator: yes): Plugin made them fall monotonically with m (bias 1/m); fair makes them agree within noise (bf 0.001783/0.001784/0.001766). The member-count order flips, as it should.
- **Control ratios control/independent_native (Blobkit checks.json control_scores; LABWORLDS "ratio = control / independent native"; acceptance "every control separating from an independent native ensemble beyond the native-vs-native band")** (assumed old estimator: yes): The 4-member independent_native falls 13-24% while controls with large errors move <0.4%, so every ratio rises by 1.15-1.32x (e.g. bf persistence 224.7 -> 281.7). Separations only grow; no control falls into a band. Lab-world ratio tables cannot be recomputed (samples gone) but follow the same rule.
- **Worked-example sanity checks (20-fold native vs zero/persistence, strict physics ladder, targeted ablations, excessive spread penalized)** (assumed old estimator: yes): All pass under fair, same as plugin (monotonic ladder cases 15/15 both). spread_x100 drops 55.8% but stays 13.9x worse than native.
- **eval_calibration_20261103/REPORT.md: S floor 0.0356 for the 64-member true simulator, 1.46 decades persistence-to-floor, ratios to the true simulator** (assumed old estimator: yes): Floor about 0.0351 with fair (-1.5%), 1.47 decades; Astra 0.10661 -> 0.10597 (-0.6%), so Astra/native ratios rise by about 0.9%. Qualitative conclusions unchanged.
- **LABWORLDS.md fed-vortex calibration: "PhySim's calibration rule gives K=1 for this suite"** (assumed old estimator: yes): Unchanged: 2*0.0351 = 0.070 still needs K=1 (K=2 would need S <= 0.005).
- **evaluation-campaign-20260916 baselines.json (1/(1+S) mapping; 4-member native controls vs 64-member agents)** (assumed old estimator: yes): Biased in favour of agents under plugin (4-member native read 20% high); fair fixes this, but the 1/(1+S) mean reward moves only in the 4th decimal (0.99812 -> 0.99850).

bf case study (docs/data/bf-case-study-20261006.json, K=2.7463 retrospective):

| Model | S plugin (= doc) | S fair | Δ% | Reward doc (K=2.7463) | fair, K=2.7463 | fair, K refit 2.7529 | K=2: plugin → fair |
|---|---|---|---|---|---|---|---|
| qwen/qwen3.5-35b-a3b | 0.61282268 | 0.61278973 | -0.01% | 0.0774 | 0.0774 | 0.0773 | 0.1063 → 0.1063 |
| qwen/qwen3.5-397b-a17b | 0.35415656 | 0.35348875 | -0.19% | 0.1641 | 0.1644 | 0.1641 | 0.2254 → 0.2258 |
| openai/gpt-6-luna | 0.15898078 | 0.15893962 | -0.03% | 0.2908 | 0.2909 | 0.2902 | 0.3993 → 0.3994 |
| x-ai/grok-4.6 | 1.857569 | 1.857569 | +0.00% | 0.0000 | 0.0000 | 0.0000 | 0.0000 → 0.0000 |
| openai/gpt-5.6-terra | 0.23273192 (ulp vs doc) | 0.23273192 | +0.00% | 0.2305 | 0.2305 | 0.2300 | 0.3166 → 0.3166 |
| anthropic/claude-sonnet-5 | 0.12910478 | 0.12677527 | -1.80% | 0.3237 | 0.3266 | 0.3258 | 0.4445 → 0.4485 |
| anthropic/claude-opus-5.5 | 0.01144735 | 0.011366086 | -0.71% | 0.7069 | 0.7080 | 0.7063 | 0.9706 → 0.9722 |
| openai/gpt-6-astra | 0.0065317333 | 0.0064840894 | -0.73% | 0.7956 | 0.7968 | 0.7948 | 1.0000 → 1.0000 |
| openai/gpt-6.1-sol | 0.0089691619 | 0.0089432953 | -0.29% | 0.7455 | 0.7459 | 0.7441 | 1.0000 → 1.0000 |

## 9. Not rescorable

| Item | Why | m / n | Expected size of the bias |
|---|---|---|---|
| labworlds/reports (round2, worlds_round, battery, curation, converge) | Only prose and ratio tables of plug-in scores are committed; the ensembles were cloud-session files (/home/user, /tmp/claude-0) that are not on this Mac; no spread term is stored. | 8 (round2 suite controls and reference), 4 (worlds_round 16 native slices), 64 (native reference) | plugin - fair = 0.5*E|X-X'|/m per score. For a native (correctly specified) ensemble E[S_plugin] = S_fair*(m+1)/m, so native scores fall by 1/(m+1): -11.1% at m=8, -20% at m=4, -1.5% at m=64. Zero-spread controls (initial persistence) do not move. Ratios control/native rise by about (m+1)/m for zero-spread or high-error controls: round2 fed vortices persistence/native 15.9 -> about 17.9 (m=8); worlds_round ratios to 4-member slices (11.8, 13.5, 23.6, ...) -> about 1.25x (persistence 23.6 -> about 29.5). Native-vs-native bands and the dt-halved nulls compare equal-size ensembles and are unbiased in expectation either way, so every documented separation gets larger, none smaller. |
| labworlds/runs_out_tables | Committed score/ratio tables only; no forecast samples; curation/dnull stores a few mean member distances, not per-group self terms. | small ensembles (sizes per file) | same rule as above: native-type ensembles -1/(m+1); deterministic controls 0. |
| labworlds/kit_readme_native_rewards | README gives reward ranges only (true simulator 0.38-0.71, rods 0.17-0.21); the 64-member native forecasts were graded in the cloud session. | 64 / 2 | S_fair ~ S_plugin*64/65 (-1.54%), so each native reward in (0, 1) rises by log10(65/64)/2 = +0.0034 at K=2. 0.38-0.71 -> about 0.383-0.713; rods 0.17-0.21 -> about 0.173-0.213; naive predictor (zero spread) unchanged at ~0. |
| reference/fedvortex_64member_true_simulator | S=0.0353 (worlds_round) and S=0.0356 (eval-calibration brief, bundle 66b6c134) are stored as numbers only; the 64-member native forecasts in the old /tmp scratchpad were purged. | 64 / 2 | -1.54% (perfect-forecaster rule, confirmed on the Blobkit 64-member calibration: -1.52%, -1.41%, -1.57%) Expected fair: worlds_round 0.0353 -> 0.03476, eval_calibration 0.0356 -> 0.03505. Reward K=2 0.7243 -> 0.7276. |
| scratch/eval-calibration purged variants (base, noise0, noise0.1, noise0.3, noise3) | cNNN.npz forecasts already removed by the macOS /tmp purge; only <variant>.json and *_fields.npy remain. | 8 / 2 | plugin - fair = 0.5*E|X-X'|/m. base: S*8/9 gives 0.0346, and the brief's measured half-pair distance 0.03494/8 gives the same 0.0346. noise0 has zero member spread (unchanged). noise x0.1/x0.3/x3: half-pair .00349/.01048/.10492 divided by 8. Expected fair: base 0.038958 -> 0.03463, noise0 0.049527 -> 0.04953, noise0.1 0.046669 -> 0.04623, noise0.3 0.042401 -> 0.04109, noise3 0.063923 -> 0.05081. |
| v1/pre-r6-BLOB-E1-traces | Different, older scorer (P1/P2/P3 CRPS accuracies in info.physim.detail), not blobround6_eval; no forecast samples saved. | n/a | not applicable / unknown |
| v1/physim_r6--Qwen--Qwen3.5-2B--bash | Only config.toml; no trace, grade or samples. | n/a | n/a |
| r6-worked/swarm_collective-runtime-copies (30 grade.json) | Copies without .npz; every primary equals the original run under probes/blobs/agentenv/round6/worked_example/rollout, which was re-scored here. | 64 / 2 | as the originals (rows 129-159) |
| reference/checks_json/labworld (9 lab bundles) | Only the score is stored (no samples in the kit); regenerating needs make_oracle (world code, scorer-hash pinned). | 4 / 2 (initial persistence) | 0: PersistencePredictor broadcasts identical members, so the self term is exactly 0 and fair == plugin bit for bit (confirmed on all 15 Blobkit reference-demo grades and 91 zero-spread runs here). |

## 10. Findings

- plugin reproduces every recorded number bit for bit on 158 of 165 re-scored runs (all macOS arm64 and unrecorded-platform grades), all 10 ensemble tables (5 control tables, 3 reward calibrations, worked-example predictor_sanity incl. the m=1/2/4 native prefix, worked-example native validation) and all 35 surviving eval-calibration scratch variants.
- MISMATCH (explained): the 7 runs graded on Linux x86_64 (bf-case-study-20261006 opus-5.5 and terra; preflight opus-cloud-controller2, opus-cloud-migration-v2, terra-cloud-migration-v2; p4-astra attempt and astra-cloud probe) differ from grade.json in the last bits: group energies up to 3.5e-15 relative, primary up to 2.2e-16 relative (e.g. 0.49700866885207157 recorded vs 0.49700866885207146). The pre-fix scorer 3d8e3fb3 on this Mac gives exactly the fixed plugin numbers for all 7, so this is x86_64-vs-arm64 floating-point reduction order, not the estimator change. Marginal CRPS matches bit for bit on all 7.
- The 3 INVALID_PREDICTIONS runs (luna bf interface-v2 14/15, qwen35b prime-agent-bf 11/15, a worked-example verifiers_scaling run 9/15) keep primary None and reward 0; their valid cases reproduce exactly and are reported as valid-case means.
- 91 runs have zero member spread; for all of them fair equals plugin bit for bit for the energy score and the marginal CRPS.
- m=1 is used by worked_example/p4g2_044/validate_native.py (zero and persistence with n_samples=1) and predictor_sanity/evaluate.py (native_member_prefix m=1). Under the default fair estimator these 45 calls raise EvaluationError; the scripts need estimator="plugin" or a 2-member broadcast (which reproduces the plugin value exactly) before they are re-run.
- Bundle pin hazard (from the inventory, still true): every existing bundle pins scoring_source_sha256 3d8e3fb3 (or dcd1ab23 legacy), and the fixed files hash 9deb1738.../d9277b60..., so Bundle()/open_bundle()/LabBundle refuse every existing bundle until resealed or the check accepts the old hash. This re-score went around it by reading bundles as data.
- Ranking changes: 2 agent-vs-agent order flips on bf, both between different campaigns and both within 1.1% (terra bf-case-study #11 0.232732 zero spread vs qwen397b campaign-20260916 #37 0.235159 -> 0.231820; luna bf-case-study recovery #14 0.158981 -> 0.158940 vs sonnet-5 prime-agent-bf-retries #81 0.159044 -> 0.158047). No flip inside any single campaign, none between an agent and a control on any bundle, none among controls in any table or among the 13 worked-example predictors. The reward-calibration member-count order (4 > 16 > 64 under plugin) is no longer monotone under fair, as expected for an unbiased estimator.
- Rewards (precision_reward, K=2): agents rise by at most +0.0066 (sonnet-5 bf interface-v2, S 0.22214 -> 0.21551); no agent, control or reference row crosses S=1 or S=0.01 (checked: none cross), so no reward leaves 0 or reaches 1 because of the estimator. Controls: 4-member independent_native and native references stay at reward 1.0 (S < 0.01 either way); ignore_actions/remove_feedback/wrong_probe_geometry rise by <= 0.0009; zero-spread persistence/zero controls are unchanged. The one large reward change is the worked-example spread_x100 sanity control (4 members with 100x the native spread): S 0.04747 -> 0.02100, reward 0.662 -> 0.839, because its plug-in score was dominated by the self-pair bias; the "excessive spread is penalized" check still passes (13.9x native instead of 26.7x).
- Agents vs controls: no order changes, but every Blobkit control-table ratio to the 4-member independent_native grows by 1.15-1.32x (bf persistence/native 224.7 -> 281.7, ignore_actions 91.4 -> 114.3); the only ratio that shrinks is the worked-example spread_x100 (26.7 -> 13.9x native_physics). The deterministic worked-example ensemble_mean goes from 1.23x to 1.44x the 4-member native_physics. Agent-to-native-reference distances therefore widen slightly (e.g. bf Astra 0.00653 vs 64-member native 0.00179 -> 0.00648 vs 0.00177).

Files: `impact.json` (all rows, per-case values, rankings, derived tables), `out/runs/*.json` (per run, per case and group: plugin, fair, theory error, per-truth-draw fair values), `out/ensembles/*.json`, `out/partial/*.json`, `out/prefix_check/*.json` (pre-fix scorer on the 7 x86_64-graded runs), `scripts/` (rescore_both.py, rescore_controls.py, score_partial.py, score_scratch_suite.py, run_all.py, run_ensembles.sh, aggregate.py, write_outputs.py, materialize_icloud.py).
