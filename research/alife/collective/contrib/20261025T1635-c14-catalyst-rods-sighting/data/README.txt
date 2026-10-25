Screens (scr.py, 128^2, steps of dt 0.05; overrides of the defaults kc 0.05, phi_b -0.8, F 0 (no fuel) at first):
o1 kc 0.02 | o2 kc 0.03 phi_b -0.9 | o3 kc 0.015 phi_b -0.7  (no fuel: slow unbounded growth)
f1 kc 0.04 F 0.01 | f2 kc 0.04 F 0.005 | f3 kc 0.06 F 0.01 Du 0.3  (fuel bounds growth; g 0.005: dense churning emulsion)
h1 g 0.05 F 0.005 | h2 g 0.05 F 0.003 nK 0.6 | h3 g 0.03 F 0.004 phi_b -0.9  (slow decline / extinction)
Published defaults: kc 0.04, F 0.007, g 0.05 (pack/seed0).
