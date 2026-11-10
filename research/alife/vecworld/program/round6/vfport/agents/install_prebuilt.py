"""install_prebuilt -- an evaluator-only reference enters the exam through the agent's route.

The designer's ceiling C is a ridge trained on simulations at the TRUE hidden parameters, so it cannot be built
in an agent's box. The evaluator builds its submission on the worker (tools/prove.py, agentenv's
reference_agent.py --policy C --no-submit) and this script, run by the scripted harness, only copies the
files that were uploaded next to it into submission/ and submits. No hidden value is on its command line.
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.getcwd())
import physim2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs("submission", exist_ok=True)
for nm in sorted(os.listdir(HERE)):
    if nm != os.path.basename(__file__) and os.path.isfile(os.path.join(HERE, nm)):
        shutil.copy(os.path.join(HERE, nm), os.path.join("submission", nm))
lab = physim2.Lab()
rep = lab.submit("submission")
json.dump({"submit": rep, "usage": lab.usage()}, open("agent_log_prebuilt.json", "w"), indent=1)
print(json.dumps({"submit": {k: rep.get(k) for k in ("ok", "accepted", "finalized", "files")}}))
