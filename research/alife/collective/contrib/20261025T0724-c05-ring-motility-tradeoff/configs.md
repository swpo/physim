Configs (WORLD_P overrides on world.py in this directory, whose defaults are mu=2.2, sig=12, chi=1.5, a=4, drive=slip, mask=phi2, Ks=0, noise IC):
- mu0c0 {"mu":0,"chi":0}; mu0c2 {"mu":0,"chi":2}  (static cells, phase_membrane-equivalent)
- c1.5m22 {} (defaults); c1.5a3m22 {"a":3}
- c2a3m22 {"chi":2,"a":3}; c2a35m22 {"chi":2,"a":3.5}; c2a3m25 {"mu":2.5,"chi":2,"a":3}; c2a3m22F8 {"chi":2,"a":3,"F":0.008}
- c2m20s8 {"mu":2.0,"sig":8,"chi":2}; c2dL01m22 {"chi":2,"dL":0.01}
- c3a3m22 {"chi":3,"a":3}; c3a3m18 {"mu":1.8,"chi":3,"a":3}
- ks_* : "Ks":0.05 (saturating link synthesis) with chi 1.5/2, mu 1.8/2.2, a 3.5
- sp10 {"chi":2,"a":3,"noise_mean":-0.1}; sp15 {"chi":2,"a":3,"noise_mean":-0.15}; sp10c15 / sp15c15 {"a":3.5,"noise_mean":-0.1/-0.15}
- s1_* : the same config on seed 1.
Measurement: python swimtrack.py world.py <out> <seed> 8000 (segments between births and splits/merges/deaths, phi>1/2 labels every 25 steps).
"ring" = mean L in the cell's own wall band (0.3<phi<0.7, within 3 px of the body) / mean L in its deep core (phi>0.9, >=3 px inside), median over the segment.
"swim-divide" = a segment born by a split that moves >= 3 body lengths (net displacement / 2 R_eq) and ends in a split with >= 2 daughters that persist >= 500 t (or split again) without merging.
