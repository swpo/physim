# Round 5, study `slots` (track 1): an object-centric bias on raw Flow-Lenia gliders

Round 4 (`../../round4/bias`) found that no block-wise bias with at most 4 numbers per block yields the object view
of the gliders world. Here the encoder is object-centric: K = 12 slots with a few numbers each, a deterministic
causal function of the level-0 history (fixed start, memory carried from tick to tick). Question: do objects emerge
from an objective plus an object-centric architecture, or does the tracker's hand-written logic
(`../../../vw1/vw/objects.py`) carry something the objective does not supply?

Code: `s5.py` (layout, grid), `ssim.py` (GPU simulation + tracker tables and label maps), `snets.py` (the slot
transducer, readouts, heads, objectives), `strain.py` (training, encoding, objective values), `scert.py` (CPU
certification workers: closure ceilings with the slot-set family, tracker agreement), `scombine.py` (pooling),
`job.sh`. Requests: `../../gpu/requests/r5-slots-*.json`. Results: `results/` (filled in when the jobs are done).
