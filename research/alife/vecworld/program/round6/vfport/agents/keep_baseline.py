"""keep_baseline -- the reference policy "null": the agent that changes nothing.

A box starts with the null policy in submission/ (predict.py and pool.npz: samples from episodes simulated at
prior draws; no laboratory data, no use of the history or of the test program). This script, run by the
scripted harness, leaves it exactly as it is, asks the laboratory to validate it once (the check an agent would
make), and ends WITHOUT a submit: the run then ends like a run whose time is up, and what is in submission/ at
that moment is collected and graded. Its score is the row "null" of the reference table and, item by item, what
a failed item of any other predictor is scored with.

It spends no laboratory tick and changes no file but its own log in the working directory.
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import physim2  # noqa: E402

lab = physim2.Lab()
rep = lab.validate("submission")
usage = lab.usage()
json.dump({"validate": rep, "usage": usage, "files": sorted(os.listdir("submission"))}, open("agent_log_null.json", "w"), indent=1)
print(json.dumps({"validate": {k: rep.get(k) for k in ("ok", "as_graded", "files")}, "ticks_used": usage.get("ticks_used")}))
