"""make_record -- turn the JSON lines that rehearsal/issue.py wrote into results/rehearsal_round2.json.

It reads the lines, a hand-written file of remarks (what, where, deviations, mismatches, what was left behind)
and, with --scan-store, the hidden side of the rehearsal's store, of which it prints and keeps COUNTS only: how
often the secret or the first ten characters of a hidden parameter of any instance occur in the record (the
same needles as tools/run_report.py). It starts nothing and removes nothing.

The record keeps, for every runbook command, the literal text that was issued and its complete output. Two
things are shortened, and said so in the file: the long paths of the rehearsal are written as <STUDY> and <HOME>
in a second, readable copy of each output (`output_short`); the literal output stays next to it.

usage: python3 -B rehearsal/make_record.py --jsonl RECORD.jsonl --remarks REMARKS.json --study STUDY --home HOME \
           [--scan-store STORE] --out results/rehearsal_round2.json
       python3 -B rehearsal/make_record.py --jsonl RECORD.jsonl --scan-store STORE --scan-only
"""
import argparse
import collections
import glob
import json
import os


def needles(store):
    out = []
    for f in sorted(glob.glob(os.path.join(store, "*", "hidden", "instance.json"))):
        inst = json.load(open(f))
        out.append(str(inst["secret_hex"]))
        out += [repr(float(v))[:10] for v in inst["theta"]]
    return out


def scan(text, store):
    nd = needles(store)
    return {"instances_in_the_store": len(glob.glob(os.path.join(store, "*", "hidden", "instance.json"))), "needles": len(nd),
            "total_hits": sum(text.count(n) for n in nd)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True)
    ap.add_argument("--remarks")
    ap.add_argument("--study")
    ap.add_argument("--home")
    ap.add_argument("--scan-store")
    ap.add_argument("--scan-only", action="store_true")
    ap.add_argument("--scan-result", help="a JSON file with the counts of an earlier --scan-only (the store is deleted by step 4)")
    ap.add_argument("--out")
    a = ap.parse_args()
    raw = open(a.jsonl).read()
    if a.scan_only:
        print(json.dumps(scan(raw, a.scan_store)))
        return
    entries = [json.loads(ln) for ln in raw.splitlines()]
    short = lambda s: s.replace(a.study, "<STUDY>").replace(a.home, "<HOME>") if isinstance(s, str) else s  # noqa: E731
    steps = []
    for e in entries:
        e = dict(e)
        if "output" in e:
            e["output_short"] = short(e["output"]).splitlines()
        steps.append(e)
    cmds = [e for e in entries if e["kind"] == "runbook command"]
    by_label = collections.Counter(e["label"] for e in cmds)
    remarks = json.load(open(a.remarks))
    out = dict(remarks)
    out["counts"] = {"entries": len(entries), "runbook_commands_issued": len(cmds), "by_label": dict(sorted(by_label.items())),
                     "status_commands_with_their_complete_output": by_label.get("2-status", 0) + by_label.get("1c-status", 0),
                     "exit_statuses_other_than_0": [[e["n"], e["label"], e["exit"]] for e in cmds if e["exit"] != 0]}
    if a.scan_result:
        out["hidden_values_in_this_record"] = json.load(open(a.scan_result))
    elif a.scan_store:
        out["hidden_values_in_this_record"] = scan(raw, a.scan_store)
    out["paths"] = {"<STUDY>": a.study, "<HOME>": a.home,
                    "note": "`text` and `output` are literal; `output_short` is the same output with the two long paths written as <STUDY> and <HOME>"}
    out["steps"] = steps
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out["counts"]))


if __name__ == "__main__":
    main()
