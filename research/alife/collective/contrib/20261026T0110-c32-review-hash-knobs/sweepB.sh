#!/bin/bash
python sweep_run.py mu001 20000 '{"mu": 0.001}' 5 6 7
python sweep_run.py sig05 20000 '{"sigma": 0.05}' 5 6 7
python sweep_run.py mu05 20000 '{"mu": 0.05}' 5 6 7
python sweep_run.py sig02n 20000 '{"sigma": 0.02, "n0": 2000}' 5 6 7
