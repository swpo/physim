cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N4_nl", "fam": "A4s", "N": 4, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N4_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N4_wn", "fam": "A4s", "N": 4, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N4_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N5_nl", "fam": "A4s", "N": 5, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N5_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N5_wn", "fam": "A4s", "N": 5, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N5_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N6_nl", "fam": "A4s", "N": 6, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N6_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N6_wn", "fam": "A4s", "N": 6, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N6_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N8_nl", "fam": "A4s", "N": 8, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N8_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N8_wn", "fam": "A4s", "N": 8, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N8_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N10_nl", "fam": "A4s", "N": 10, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N10_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N10_wn", "fam": "A4s", "N": 10, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N10_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N12_nl", "fam": "A4s", "N": 12, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N12_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A4s_N12_wn", "fam": "A4s", "N": 12, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A4s_N12_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N4_nl", "fam": "A5", "N": 4, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N4_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N4_wn", "fam": "A5", "N": 4, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N4_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N5_nl", "fam": "A5", "N": 5, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N5_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N5_wn", "fam": "A5", "N": 5, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N5_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N6_nl", "fam": "A5", "N": 6, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N6_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N6_wn", "fam": "A5", "N": 6, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N6_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N8_nl", "fam": "A5", "N": 8, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N8_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N8_wn", "fam": "A5", "N": 8, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N8_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N10_nl", "fam": "A5", "N": 10, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N10_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N10_wn", "fam": "A5", "N": 10, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N10_wn.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N12_nl", "fam": "A5", "N": 12, "T": 5000.0, "noise": 0.0, "seed": 0, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N12_nl.log 2>&1 &
nohup $PY runjob.py '{"kind": "ring", "name": "R1_A5_N12_wn", "fam": "A5", "N": 12, "T": 5000.0, "noise": 0.002, "seed": 1, "snap_times": [0, 2500, 5000]}' > logs/R1_A5_N12_wn.log 2>&1 &
echo all_launched