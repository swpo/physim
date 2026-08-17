#!/bin/bash
cd /Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.0_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.0,"init_c":"uniform","_seed":0}' > assay_selA_lam0.0_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.0_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.0,"init_c":"uniform","_seed":1}' > assay_selA_lam0.0_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.0_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.0,"init_c":"uniform","_seed":2}' > assay_selA_lam0.0_s2.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.001_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.001,"init_c":"uniform","_seed":0}' > assay_selA_lam0.001_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.001_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.001,"init_c":"uniform","_seed":1}' > assay_selA_lam0.001_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.001_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.001,"init_c":"uniform","_seed":2}' > assay_selA_lam0.001_s2.log 2>&1 &
wait
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.002_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.002,"init_c":"uniform","_seed":0}' > assay_selA_lam0.002_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.002_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.002,"init_c":"uniform","_seed":1}' > assay_selA_lam0.002_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.002_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.002,"init_c":"uniform","_seed":2}' > assay_selA_lam0.002_s2.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.004_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.004,"init_c":"uniform","_seed":0}' > assay_selA_lam0.004_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.004_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.004,"init_c":"uniform","_seed":1}' > assay_selA_lam0.004_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.004_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.004,"init_c":"uniform","_seed":2}' > assay_selA_lam0.004_s2.log 2>&1 &
wait
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.008_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.008,"init_c":"uniform","_seed":0}' > assay_selA_lam0.008_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.008_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.008,"init_c":"uniform","_seed":1}' > assay_selA_lam0.008_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py selA_lam0.008_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"mu":0.01,"lam_c":0.008,"init_c":"uniform","_seed":2}' > assay_selA_lam0.008_s2.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.001_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.001,"init_c":"top","_seed":0}' > assay_mutB_mu0.001_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.001_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.001,"init_c":"top","_seed":1}' > assay_mutB_mu0.001_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.001_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.001,"init_c":"top","_seed":2}' > assay_mutB_mu0.001_s2.log 2>&1 &
wait
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.003_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.003,"init_c":"top","_seed":0}' > assay_mutB_mu0.003_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.003_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.003,"init_c":"top","_seed":1}' > assay_mutB_mu0.003_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.003_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.003,"init_c":"top","_seed":2}' > assay_mutB_mu0.003_s2.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.01_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.01,"init_c":"top","_seed":0}' > assay_mutB_mu0.01_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.01_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.01,"init_c":"top","_seed":1}' > assay_mutB_mu0.01_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.01_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.01,"init_c":"top","_seed":2}' > assay_mutB_mu0.01_s2.log 2>&1 &
wait
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.03_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.03,"init_c":"top","_seed":0}' > assay_mutB_mu0.03_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.03_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.03,"init_c":"top","_seed":1}' > assay_mutB_mu0.03_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.03_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.03,"init_c":"top","_seed":2}' > assay_mutB_mu0.03_s2.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.1_s0 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.1,"init_c":"top","_seed":0}' > assay_mutB_mu0.1_s0.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.1_s1 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.1,"init_c":"top","_seed":1}' > assay_mutB_mu0.1_s1.log 2>&1 &
MPLBACKEND=Agg $PY assay_rates.py mutB_mu0.1_s2 '{"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":30000,"lam_c":0.002,"mu":0.1,"init_c":"top","_seed":2}' > assay_mutB_mu0.1_s2.log 2>&1 &
wait
wait
echo ASSAYS_DONE
