#!/bin/bash
# cpairs_run.sh -- the paired trajectory bootstraps quoted in results/summary.json (local; numpy).
# usage: bash cpairs_run.sh FETCH_DIR     (FETCH_DIR: `git archive origin/gpu-jobs jobs/<job>/out/<world>/items` unpacked)
# A config is compared with hand windows on both sides of its effective dimension (see results/analysis.json:<world>.families_PR).
set -eu
F=$1
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=${PY:-python3}
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-005/out/vortex/items" "$HERE/results/pairs_vortex.json" \
  L0_clos_c1=hand_om_h0 L0_clos_c1=hand_sfa_c1 L0_clos_c1=hand_dab_h4 L0_clos_c1=hand_dab_h8 L0_local_c1=L0_clos_c1 \
  L0_local_c1=hand_dab_h4 L0_local_c1=hand_dab_h8 N0_clos_c1=L0_clos_c1 N0_clos_c1=hand_om_h0 N0_local_c1=hand_om_h0 \
  N0_clos_c1=hand_dab_h8 N0_clos_c1=hand_dab_h16 N0_local_c1=hand_dab_h8 N0_local_c1=hand_dab_h16 N8_clos_c1=hand_dab_h8 \
  N8_clos_c1=hand_dab_h16 N8_clos_c1=hand_om_h16 L8_clos_c1=hand_dab_h8 L8_clos_c1=hand_dab_h16 L8_local_c1=hand_dab_h16 \
  N8_local_c1=hand_dab_h16 L0_recon_c1=hand_Y_h0 L0_clos_c1=L0_recon_c1 N0_recon_c1=L0_recon_c1 U_clos_c1=hand_om_h0 \
  U_clos_c1=L0_clos_c1 U_local_c1=L0_local_c1 Uc_clos_c1=N8_clos_c1 hand_om_h0=hand_dab_h0 hand_sfa_c1=hand_om_h0 \
  N8_clos_c1=hand_om_h8 L8_clos_c1=hand_om_h8 N8_local_c1=hand_om_h8 N0_clos_c1=hand_om_h16 L0_clos_c1=hand_om_h16 N8_local_c1=hand_om_h16 \
  U_clos_c1=hand_a_h0
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-004/out/membrane/items" "$HERE/results/pairs_membrane.json" \
  L0_clos_c1=hand_K_h0 L0_clos_c1=hand_K_h4 L0_clos_c1=hand_K_h8 L0_clos_c1=hand_S_h4 N0_clos_c1=hand_K_h0 N0_clos_c1=hand_K_h8 \
  N0_clos_c1=hand_S_h4 N8_clos_c1=hand_K_h8 N8_clos_c1=hand_K_h16 N8_clos_c1=hand_S_h8 L8_clos_c1=hand_K_h8 L8_clos_c1=hand_K_h16 \
  L8_clos_c1=hand_S_h16 L0_local_c1=hand_K_h0 L0_local_c1=hand_K_h4 N0_local_c1=hand_K_h0 N0_local_c1=hand_K_h4 \
  N8_local_c1=hand_K_h8 L8_local_c1=hand_K_h8 L0_recon_c1=hand_K_h0 L0_recon_c1=hand_K_h4 N0_recon_c1=hand_K_h0 \
  U_clos_c1=hand_K_h0 U_clos_c1=hand_K_h4 U_local_c1=hand_K_h4 U_clos_c1=L0_clos_c1 L0_clos_c1=L0_local_c1 N0_clos_c1=L0_clos_c1 \
  hand_sfa_c1=hand_K_h0 hand_sfax_c1=hand_K_h4 N8_clos_c2=N8_clos_c1 N8_clos_c2=hand_fields \
  N0_clos_c1=hand_sfax_c1 N8_clos_c1=hand_sfax_c1 L0_clos_c1=hand_sfax_c1 L8_clos_c1=hand_sfax_c1 N8_local_c1=hand_sfax_c1 \
  L0_local_c1=hand_sfa_c1 L8_local_c1=hand_sfax_c1
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-004/out/gliders/items" "$HERE/results/pairs_gliders.json" \
  L0_clos_c1=hand_mass_h0 L0_clos_c1=hand_mass_h4 L0_local_c1=hand_mass_h0 L0_local_c1=hand_mass_h4 N0_local_c1=hand_mass_h0 \
  N0_local_c1=hand_mass_h4 N0_clos_c1=hand_mass_h0 N0_clos_c1=hand_mass_h4 N0_clos_c1=hand_mass_h8 N8_local_c1=hand_mass_h8 \
  N8_local_c1=hand_mass_h16 L8_local_c1=hand_mass_h8 L8_local_c1=hand_mass_h16 N8_clos_c1=hand_mass_h16 L8_clos_c1=hand_mass_h16 \
  L0_recon_c1=hand_mass_h0 N0_recon_c1=hand_mass_h0 U_clos_c1=hand_mass_h0 U_local_c1=hand_mass_h0 U_clos_c1=L0_clos_c1 \
  L0_local_c1=L0_clos_c1 N8_local_c1=hand_c0_h8 N8_clos_c1=hand_c0_h8 L8_local_c1=hand_c0_h8 N0_local_c1=hand_sfa_c1 \
  L0_local_c1=hand_sfa_c1 L0_clos_c1=hand_sfa_c1 N0_clos_c1=hand_msq_h4
# follow-up job r5-bias2-007 (closure on spatially whitened latents: Lw / Nw), same items for both sides within the job
if [ -d "$F/jobs/r5-bias2-007/out/vortex/items" ]; then
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-007/out/vortex/items" "$HERE/results/pairs_vortex_w.json" \
  Lw0_clos_c1=L0_clos_c1 Nw0_clos_c1=N0_clos_c1 Lw8_clos_c1=L8_clos_c1 Nw8_clos_c1=N8_clos_c1 \
  Lw0_clos_c1=hand_om_h0 Nw0_clos_c1=hand_om_h0 Lw8_clos_c1=hand_om_h8 Nw8_clos_c1=hand_om_h8 Lw8_clos_c1=hand_om_h4 Nw8_clos_c1=hand_om_h4 \
  Lw8_clos_c1=hand_om_h16 Nw8_clos_c1=hand_om_h16 Lw0_clos_c1=hand_Y_h0 Nw0_clos_c1=hand_Y_h0 Lw0_clos_c1=hand_dab_h0 \
  L0_clos_c1=hand_om_h0 N0_clos_c1=hand_om_h0 N8_clos_c1=hand_om_h16 Lw0_clos_c1=hand_sfa_c1 L0_clos_c1=hand_sfa_c1
fi
if [ -d "$F/jobs/r5-bias2-007/out/membrane/items" ]; then
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-007/out/membrane/items" "$HERE/results/pairs_membrane_w.json" \
  Lw0_clos_c1=L0_clos_c1 Nw0_clos_c1=N0_clos_c1 Lw8_clos_c1=L8_clos_c1 Nw8_clos_c1=N8_clos_c1 \
  Lw0_clos_c1=hand_K_h0 Nw0_clos_c1=hand_K_h0 Lw0_clos_c1=hand_sfax_c1 Nw0_clos_c1=hand_sfax_c1 Lw8_clos_c1=hand_K_h8 Nw8_clos_c1=hand_K_h8 \
  Lw8_clos_c1=hand_K_h4 Nw8_clos_c1=hand_K_h4 Lw8_clos_c1=hand_sfax_c1 Nw8_clos_c1=hand_sfax_c1 Lw0_clos_c1=hand_phi_h0 \
  L0_clos_c1=hand_K_h0 N0_clos_c1=hand_K_h0 N0_clos_c1=hand_sfax_c1 N8_clos_c1=hand_sfax_c1
fi
if [ -d "$F/jobs/r5-bias2-007/out/gliders/items" ]; then
$PY -B "$HERE/cpair.py" "$F/jobs/r5-bias2-007/out/gliders/items" "$HERE/results/pairs_gliders_w.json" \
  Lw0_clos_c1=L0_clos_c1 Nw0_clos_c1=N0_clos_c1 Lw8_clos_c1=L8_clos_c1 Nw8_clos_c1=N8_clos_c1 \
  Lw0_clos_c1=hand_mass_h0 Nw0_clos_c1=hand_mass_h0 Lw8_clos_c1=hand_mass_h8 Nw8_clos_c1=hand_mass_h8 Lw8_clos_c1=hand_mass_h4 \
  Nw8_clos_c1=hand_mass_h4 Lw8_clos_c1=hand_mass_h16 Nw8_clos_c1=hand_mass_h16 L0_clos_c1=hand_mass_h0 N0_clos_c1=hand_mass_h0 \
  Lw0_clos_c1=hand_sfa_c1
fi
