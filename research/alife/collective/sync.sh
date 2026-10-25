#!/bin/bash
# Librarian loop: import new contributions from worker branches, rebuild the state of the field,
# push the lab branch. Prints one event line per import, status change and score change.
#   research/alife/collective/sync.sh [interval_seconds] [python]
set -u
INTERVAL=${1:-180}
PY=${2:-python}
REPO=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
LAB_BRANCH=claude/fisim-agent-world-research-hepmlz
cd "$REPO" || exit 1
declare -A warned
while true; do
  if [ -e research/alife/collective/STOP_LIBRARIAN ]; then echo "LIBRARIAN stopped"; exit 0; fi
  git fetch -q --prune origin '+refs/heads/claude/alife-c-*:refs/remotes/origin/claude/alife-c-*' 2>/dev/null
  out=$(cd research/alife && PYTHONDONTWRITEBYTECODE=1 $PY collective/build.py --import-branches 2>&1)
  echo "$out" | grep -E "^(IMPORT|STATUS)|Traceback|Error" | sed "s/^/$(date -u +%H:%M) /"
  score=$(echo "$out" | grep "^SCORE" | sed 's/ contributions=.*//')
  if [ "$score" != "${last_score:-}" ]; then echo "$(date -u +%H:%M) $score"; last_score=$score; fi
  git add research/alife/collective/contrib research/alife/collective/imported.json \
          research/alife/collective/STATE.md research/alife/collective/QUEUE.md \
          research/alife/collective/ledger.json research/alife/collective/progress.json \
          research/alife/collective/progress.png 2>/dev/null
  if ! git diff --cached --quiet; then
    n=$(echo "$out" | grep -c "^IMPORT")
    git commit -q -m "collective: import $n contributions, rebuild state" \
      -m "$(printf 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BZceC7G6m7DgM6KpXjnWXj')"
    for i in 1 2 3 4; do git push -q origin "$LAB_BRANCH" 2>/dev/null && break; sleep $((2 ** i)); done \
      || echo "$(date -u +%H:%M) PUSH failed"
  fi
  # agents silent for a long time (their newest contribution on their branch)
  for ref in $(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/claude/alife-c-*'); do
    head=$(git rev-parse "$ref")
    age=$(( ($(date +%s) - $(git log -1 --format=%ct "$ref")) / 60 ))
    w=${ref##*alife-c-}
    if [ "$age" -ge 50 ] && [ "${warned[$w]:-}" != "$head" ]; then
      echo "$(date -u +%H:%M) QUIET $w ${age}min"; warned[$w]=$head
    fi
  done
  sleep "$INTERVAL"
done
