# BLOB2 round-4 FINAL (fable-5 complete after 2 resumes; sol done earlier)
# eval: physim -n 3, claude_code harness, docker runtime, skill-normalized scoring

## fable-5 (anthropic/claude-fable-5)
E1 (BLOB2-E1): rollouts 0.268 / 0.287 / 0.370  -> MEAN +0.308
E2 (BLOB2-E2): rollouts 0.159 / 0.248 / 0.454  -> MEAN +0.287

per-level means (across 3 rollouts):
E1: L1 0.28  L2 -0.00  L3F 0.26  L3E -0.02  L4 0.61  L4D 0.72
E2: L1 0.08  L2  0.20  L3F 0.00  L3S 0.47  L4 0.43  L4D 0.55

## reference rows
scripted actor:  E1 +0.238   E2 +0.233   (results/smoke_blob2_*.json)
gpt-5.6-sol:     E1 -0.42..-0.67   E2 -0.22..-0.67  (negative everywhere)

## reading
- fable > scripted baseline on BOTH worlds (+0.07 / +0.05): first positive-skill
  agent result on the clean-slate contract system.
- dose-leg tiers (L4/L4D) are fable's strength (L4D hits 0.99 in one rollout
  per world). L2 hidden-sensor nowcast: still ~zero on E1; PARTIAL skill on E2
  (0.28/0.28 in 2 of 3) — the open-headroom tier is being dented, not cracked.
- L3E negative-to-flat on E1; L1 modest positive both worlds.
- variance across rollouts is high (E2 0.16->0.45): n=3 is a floor, not a book.
- all 6 rollouts ok after resumes; earlier errors were transient pinference 5xx.
