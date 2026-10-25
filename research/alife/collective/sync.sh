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
C=research/alife/collective
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 1
GITDIR=$(git rev-parse --git-dir)
last_commit=0
log() { echo "$(date -u +%H:%M) $*"; }
while true; do
  if [ -e /home/user/librarian.stop ]; then log "LIBRARIAN stopped"; exit 0; fi
  find "$GITDIR" -maxdepth 1 -name index.lock -mmin +5 -delete 2>/dev/null  # only this loop uses the worktree
  if ! timeout 120 git fetch -q origin "+refs/heads/$LAB_BRANCH:refs/remotes/origin/$LAB_BRANCH"; then
    log "FETCH of the lab branch failed"; sleep "$INTERVAL"; continue
  fi
  for b in $(timeout 60 git ls-remote --heads origin 'claude/alife-collective-*' | awk '{print $2}' | sed 's#refs/heads/##'); do
    timeout 120 git fetch -q origin "+refs/heads/$b:refs/remotes/origin/$b" || log "FETCH $b failed"
  done
  if ! { git reset -q --hard "origin/$LAB_BRANCH" && git clean -fdq -- "$C"; }; then
    log "RESET failed"; sleep "$INTERVAL"; continue
  fi
  out=$(cd research/alife && PYTHONDONTWRITEBYTECODE=1 timeout 900 $PY collective/build.py --import-branches 2>&1)
  events=$(echo "$out" | grep -E "^(IMPORT|STATUS|DEFER|BRANCH)|Traceback|Error")
  [ -n "$events" ] && echo "$events" | sed "s/^/$(date -u +%H:%M) /"
  now=$(date +%s)
  if [ -n "$events" ] || [ $((now - last_commit)) -ge 1800 ]; then
    git add -A -- "$C/contrib" $(cd "$C" && ls -d imported.json STATE.md QUEUE.md ledger.json progress.json progress.png 2>/dev/null | sed "s#^#$C/#")
    if ! git diff --cached --quiet; then
      n=$(echo "$out" | grep -c "^IMPORT")
      if git commit -q -m "collective: import $n contributions, rebuild state" \
           -m "$(printf 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01BZceC7G6m7DgM6KpXjnWXj')"; then
        if timeout 120 git push -q origin "HEAD:$LAB_BRANCH"; then
          last_commit=$now
          log "$(echo "$out" | grep '^SCORE')"
        else
          log "PUSH rejected; redoing next cycle"
        fi
      else
        log "COMMIT failed"
      fi
    fi
  fi
  sleep "$INTERVAL"
done
