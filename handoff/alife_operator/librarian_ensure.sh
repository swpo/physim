#!/bin/bash
# Start the librarian loop if it is not running (container restarts kill it). Prints its state.
if ps -eo args | grep -q "^/bin/bash research/alife/collective/sync.sh"; then
  echo "librarian running"
else
  cd /home/user/librarian && nohup setsid research/alife/collective/sync.sh 180 /home/user/labenv/bin/python >> /home/user/librarian.log 2>&1 < /dev/null &
  sleep 2
  ps -eo args | grep -q "^/bin/bash research/alife/collective/sync.sh" && echo "librarian restarted" || echo "librarian FAILED to start"
fi
tail -n 2 /home/user/librarian.log
