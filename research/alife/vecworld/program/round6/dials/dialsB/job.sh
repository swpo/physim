#!/usr/bin/env bash
# job.sh -- stage 0 of the membrane carrier (study B of ../PLAN.md) as ONE CPU job. DECLARED.md is the
# specification. Phases: presmoke -> speed guard -> scans V and C (and the alignment check) -> ranges.json with its hash -> the gate
# (8 seeds x 2 arms) -> analysis. Everything in $OUT and on stdout is public. Pilot values, never an exam.
#   S0_SIZE=full|tiny   S0_NPROC=<parallel processes>   S0_LIMIT_S=<deadline of the script, seconds>
set -u -o pipefail
cd "$(dirname "$0")"
export OUT="${OUT:-$PWD/out}"
mkdir -p "$OUT"
export S0_SIZE="${S0_SIZE:-full}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 JAX_PLATFORMS=cpu
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="${PY:-python}"
NPROC="${S0_NPROC:-$(nproc)}"
LIMIT_S="${S0_LIMIT_S:-10800}"
T_START=$(date +%s)
left() { echo $(( LIMIT_S - ($(date +%s) - T_START) )); }
say() { echo "$(date -u +%H:%M:%S) job: $*" | tee -a "$OUT/progress.txt"; }
die() { say "FAILED: $1 (exit $2)"; for f in "$OUT"/log_*.txt; do echo "--- $f"; tail -n 25 "$f"; done; exit "$2"; }
phase() {  # phase NAME CMDFILE: run the commands of CMDFILE, NPROC at a time, inside the deadline
  local name="$1" file="$2" t
  t=$(left); [ "$t" -gt 60 ] || die "deadline reached before $name" 5
  say "$name: $(wc -l < "$file") processes, $NPROC at a time, $t s left"
  timeout "$t" xargs -d '\n' -P "$NPROC" -I CMD sh -c CMD < "$file" || die "$name" 4
}

say "start size=$S0_SIZE nproc=$NPROC limit=${LIMIT_S}s"
$PY -B -c "import sys, jax, numpy, scipy; print('versions: python', sys.version.split()[0], 'jax', jax.__version__, 'numpy', numpy.__version__, 'scipy', scipy.__version__)" || die "imports" 2

# 1. presmoke: every stage once at full array shapes, short counts
timeout 1800 $PY -B s0.py presmoke > "$OUT/log_presmoke.txt" 2>&1 || die "presmoke" 2
tail -n 3 "$OUT/log_presmoke.txt"

# 2. speed guard: the measured rate must project the whole job inside 2.5 hours (DECLARED.md 2.7)
$PY -B - "$NPROC" <<'EOF' || die "speed guard: the job cannot finish in time" 3
import json, os, sys
r = json.load(open(os.path.join(os.environ["OUT"], "presmoke.json")))
nproc = min(int(sys.argv[1]), 16)
rate, n = r["steady_rate_member_ticks_per_s"], r["planned_member_ticks"]["total"]
proj = 1.15 * n / (rate * nproc * 0.5) + 600 + r["wall_s"]          # half efficiency per process when all cores are busy
print(f"speed guard: steady rate {rate:.0f} member-ticks/s per process, planned {n} member-ticks, {nproc} processes: "
      f"projected {proj:.0f} s (limit 9000 s; full size only)")
sys.exit(0 if (proj < 9000 or os.environ["S0_SIZE"] != "full") else 1)
EOF

# 3. the scans
if [ "$S0_SIZE" = full ]; then NV=7; NC=7; else NV=1; NC=1; fi
: > "$OUT/cmds_scan.txt"
for p in $(seq 0 $((NV - 1))); do echo "$PY -B s0.py scanV $p $NV > $OUT/log_scanV_$p.txt 2>&1" >> "$OUT/cmds_scan.txt"; done
for p in $(seq 0 $((NC - 1))); do echo "$PY -B s0.py scanC $p $NC > $OUT/log_scanC_$p.txt 2>&1" >> "$OUT/cmds_scan.txt"; done
# with them, not fatal: the gate's code path on the designer's pilot seed 5 against his own file
echo "$PY -B s0.py align > $OUT/log_align.txt 2>&1 || echo align-failed-not-fatal >> $OUT/progress.txt" >> "$OUT/cmds_scan.txt"
phase scans "$OUT/cmds_scan.txt"

# 4. the ranges, hashed before any gate run starts
$PY -B s0.py ranges > "$OUT/log_ranges.txt" 2>&1 || die "ranges" 4
say "ranges.sha256: $(cat "$OUT/ranges.sha256")"

# 5. the gate
if [ "$S0_SIZE" = full ]; then SEEDS="31 32 33 34 35 36 37 38"; else SEEDS="91 92"; fi
: > "$OUT/cmds_gate.txt"
for s in $SEEDS; do for a in main control; do
  echo "$PY -B s0.py gate $s $a > $OUT/log_gate_${s}_$a.txt 2>&1" >> "$OUT/cmds_gate.txt"
done; done
phase gate "$OUT/cmds_gate.txt"

# 6. the analysis
$PY -B s0.py analyse > "$OUT/log_analyse.txt" 2>&1 || die "analyse" 4
tail -n 2 "$OUT/log_analyse.txt"
rm -rf "$OUT/presmoke"
say "done in $(( $(date +%s) - T_START )) s; \$OUT is $(du -sm "$OUT" | cut -f1) MB"
exit 0
