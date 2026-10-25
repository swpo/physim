for s in "$@"; do for m in 8 15; do python invade.py $s 20000 $m 40000 census/inv${m}_s$s.json; done; done
