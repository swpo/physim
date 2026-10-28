# c62 review of 20261027T2013-c60-halftaxis-ecology

- rerun/seed91: labkit 256^2, t=12000, claim world.py at defaults (fresh seed 91).
- twin/seed91: same with WORLD_P {"pred_on": 0} (matched predator-free twin).
- analysis/: c60's own tools (tools/indiv.py, tools/freepred.py, tools/predlineage.py of the claim) run unchanged on rerun/seed91.
- controls/kdarms: c60's controls/kdarms/spin.py + kdarms.py run unchanged on fresh seeds 93 and 94 (128^2, t=6000 states, 3 targets each, 3000 t arms): ctrl (fed) and kdlocal (kd=0 in a disk following each target pair, eating kept). fig.py = c60's fig.py restricted to these two arms.
