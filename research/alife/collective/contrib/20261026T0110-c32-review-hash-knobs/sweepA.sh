#!/bin/bash
# (c32) every arm of c30's knobs finding on seeds 5-7, 20000 steps (same parameters as c30's runs/)
python sweep_run.py base 20000 '{}' 5 6 7
python sweep_run.py crowd03n 20000 '{"crowd": 0.3, "n0": 2000}' 5 6 7
python sweep_run.py resalt2k 20000 '{"resalt": 2000}' 5 6 7
