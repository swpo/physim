#!/bin/bash
# (c32) four arms per seed: shared/separate food x world step DT 0.1/0.05, c26's counter, t=0-300
s=$1
for dt in 0.1 0.05; do for sep in 0 1; do
  WORLD_P="{\"DT\": $dt, \"SEP\": $sep}" python runle_dt.py world_dt.py $s 300 arms/s${s}_dt${dt}_sep${sep}
done; done
