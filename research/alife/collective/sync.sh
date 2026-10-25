#!/bin/bash
# Librarian loop. Runs in its own detached worktree, so it never touches a working checkout:
#   git worktree add --detach /home/user/librarian origin/claude/fisim-agent-world-research-hepmlz
#   cd /home/user/librarian && nohup setsid research/alife/collective/sync.sh 180 /path/to/python \
#       >> /home/user/librarian.log 2>&1 < /dev/null & echo $! > /home/user/librarian.pid
# Each cycle: reset to the lab branch on origin, import new contributions from agent branches,
# rebuild the state of the field, and push when something changed (or every 30 minutes).
# Stop it by creating /home/user/librarian.stop.
set -u
INTERVAL=${1:-180}
PY=${2:-python}
LAB_BRANCH=claude/fisim-agent-world-research-hepmlz
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 1
last_commit=0
while true; do
  if [ -e /home/user/librarian.stop ]; then echo "$(date -u +%H:%M) LIBRARIAN stopped"; exit 0; fi
  if git fetch -q --prune origin "+refs/heads/$LAB_BRANCH:refs/remotes/origin/$LAB_BRANCH" \
       '+refs/heads/claude/alife-collective-*:refs/remotes/origin/claude/alife-collective-*' 2>/dev/null; then
    git reset -q --hard "origin/$LAB_BRANCH"
    out=$(cd research/alife && PYTHONDONTWRITEBYTECODE=1 $PY collective/build.py --import-branches 2>&1)
    events=$(echo "$out" | grep -E "^(IMPORT|STATUS|DEFER)|Traceback|Error")
    [ -n "$events" ] && echo "$events" | sed "s/^/$(date -u +%H:%M) /"
    now=$(date +%s)
    if [ -n "$events" ] || [ $((now - last_commit)) -ge 1800 ]; then
      git add research/alife/collective/contrib research/alife/collective/imported.json \
              research/alife/collective/STATE.md research/alife/collective/QUEUE.md \
              research/alife/collective/ledger.json research/alife/collective/progress.json \
              research/alife/collective/progress.png 2>/dev/null
      if ! git diff --cached --quiet; then
        n=$(echo "$out" | grep -c "^IMPORT")
        git commit -q -m "collective: import $n contributions, rebuild state" \
          -m "$(printf 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BZceC7G6m7DgM6KpXjnWXj')"
        if git push -q origin "HEAD:$LAB_BRANCH" 2>/dev/null; then
          last_commit=$now
          echo "$(date -u +%H:%M) $(echo "$out" | grep '^SCORE')"
        else
          echo "$(date -u +%H:%M) PUSH rejected; redoing next cycle"
        fi
      fi
    fi
  else
    echo "$(date -u +%H:%M) FETCH failed"
  fi
  sleep "$INTERVAL"
done
