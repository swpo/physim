#!/usr/bin/env bash
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for spec in 'base_0|{"dyn_noise":0}' 'phys_0.01|{"dyn_noise":0.01,"noise_fields":["q1","q2"],"cons_fields":["phi"],"mult_fields":["s","c"]}'; do
  tag=${spec%%|*}; P=${spec#*|}
  SECONDS=0; env WORLD_P="$P" .labenv/bin/python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/b128_${tag}_s2 --seeds 2 --frames 100 --size 128 128 --no-movie > /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/log_${tag}_s2.txt 2>&1; echo "sim wall $SECONDS s"
  tail -2 /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/log_${tag}_s2.txt
  .labenv/bin/python /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/measure.py /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/b128_${tag}_s2 >> /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/log_${tag}_s2.txt 2>&1
  tail -1 /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni_review/packs/log_${tag}_s2.txt
done
echo RUN2 DONE
