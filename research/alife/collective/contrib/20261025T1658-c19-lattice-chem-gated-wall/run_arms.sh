#!/bin/bash
# c19: lattice-chem-gate at phi_AW 0.5: gate (gA 3), no gate, and the slow-A twin (no gate, A mobility 0.06 instead of 0.2).
# usage: run_arms.sh seed arm...
s=$1; shift
for arm in "$@"; do
  case $arm in gate) P='{"phi_AW":0.5,"gA":3}';; nogate) P='{"phi_AW":0.5}';; slowA) P='{"phi_AW":0.5,"pA":0.06}';; esac
  WORLD_P="$P" python -m labkit.run collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/world.py --out collective/contrib/20261025T1658-c19-lattice-chem-gated-wall/$arm/seed$s --seeds $s --no-movie
done
