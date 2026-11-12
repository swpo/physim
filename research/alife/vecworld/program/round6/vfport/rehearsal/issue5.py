"""issue5 -- rehearsal/issue4.py for the round-5 RUNBOOK_MAC.md: the same issuer (one `sh -c '<text>'` per command,
the text taken from the runbook on disk in the clone, a literal record), with the pilot's names of round 5: the
pilot folder and run label `physim2-pilot-r5` (round 4: `physim2-pilot-20261110`). Nothing else differs; read
issue4.py for the substitutions, the actions that are not runbook commands, and the refusals. Cloud rehearsal only
(PHYSIM2_DEV_MACHINE=cloud-container; rehearsal/ is on the never-list of RUNBOOK_MAC.md, rule 8).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import issue4 as I  # noqa: E402

I.PILOT = "physim2-pilot-r5"
I.LABELS["1b-mkdir"] = [f'mkdir -m 700 "$HOME/{I.PILOT}" &&', "PILOT-FOLDER-MADE"]
I.LABELS["4a-copy-delete"] = [f"{I.PILOT}-results/\" && test -s"]
I.RM = f'rm -rf "$HOME/{I.PILOT}/store" "$HOME/{I.PILOT}/scratch"'

if __name__ == "__main__":
    I.main()
