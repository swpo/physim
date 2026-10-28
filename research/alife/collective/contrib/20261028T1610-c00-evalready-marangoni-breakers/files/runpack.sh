#!/usr/bin/env bash
# runpack.sh TAG SEED FRAMES SIZE 'WORLD_P json'  -> packs/TAG_sSEED/ + claim_measures.json
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni
OUT=$D/packs/$1_s$2
mkdir -p $D/packs
WORLD_P="$5" .labenv/bin/python -m labkit.run $D/mg_noise.py --out $OUT --seeds $2 --frames $3 --size $4 $4 --no-movie > $D/packs/log_$1_s$2.txt 2>&1
.labenv/bin/python $D/measure.py $OUT >> $D/packs/log_$1_s$2.txt 2>&1
tail -1 $D/packs/log_$1_s$2.txt
