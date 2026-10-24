"""Parse every creature record in Chakazul/Lenia Python/found/*.json into one list (chan_found.json).

git clone --depth 1 https://github.com/Chakazul/Lenia.git /tmp/lenia_ref
python parse_catalogue.py /tmp/lenia_ref/Python/found OUT.json
Indices in our NOTEBOOK/worlds refer to the order produced here (files sorted by name).
"""
import glob
import json
import sys

dec = json.JSONDecoder()
out = []
for f in sorted(glob.glob(sys.argv[1].rstrip("/") + "/*.json")):
    s = open(f).read()
    i = 0
    while True:
        j = s.find('{"', i)
        if j < 0:
            break
        try:
            o, e = dec.raw_decode(s, j)
        except Exception:
            i = j + 2
            continue
        if isinstance(o, dict) and "params" in o and "cells" in o and isinstance(o["params"], list):
            nc = len(o["cells"]) if isinstance(o["cells"], list) else 1
            p0 = o["params"][0]
            out.append(dict(file="found/" + f.split("/")[-1], code=o.get("code"), name=o.get("name"),
                            nk=len(o["params"]), nc=nc, R=p0.get("R"), T=p0.get("T"), params=o["params"],
                            cells=o["cells"], settings=o.get("settings")))
        i = e
json.dump(out, open(sys.argv[2], "w"))
print(len(out), "records")
