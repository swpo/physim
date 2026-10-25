#!/bin/bash
# c19: ringless (chis=0) twins of c15's nematic fuel-cell with uniformly lowered fuel diffusivity, on the claim's seeds.
# usage: run_twins.sh Df seed...
Df=$1; shift
for s in "$@"; do WORLD_P="{\"chis\":0,\"Df\":$Df}" python -m labkit.run collective/contrib/20261025T1412-c15-nematic-fuelcell-claim/world.py --out collective/contrib/20261025T1619-c19-fuelcell-slowd-twins/chis0_Df$Df/seed$s --seeds $s --no-movie; done
