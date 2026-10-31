"""Which vortex divides within 50 tu when fed (Y+ amp 3 for 25 tu at its centre) versus unfed (sham)."""
import json, sys
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
import design as D

s = D.load_state(f"{C.OUT}/prep/state_s31.pkl")
bs = {b["id"]: b for b in json.load(open(f"{C.OUT}/prep/bodies_s31.json"))}
ids = [int(x) for x in sys.argv[1].split(",")]
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 4200
out = {}
fr_sham = None
for i in ids:
    yx = [bs[i]["cy"], bs[i]["cx"]]
    devs = [D.device(0, yx), D.device(1, [bs[1]["cy"], bs[1]["cx"]])]
    res = {}
    for prog, actions in (("sham", []), ("feed", [dict(t=0, kind="inject", device=0, port=D.ACT["Y+"], amp=3.0, dur=25.0)])):
        if prog == "sham" and fr_sham is not None:
            fr = fr_sham
        else:
            fr, _ = D.capture(D.oracle(s, devs), actions, seed=seed)
            if prog == "sham":
                fr_sham = fr
        hist, ev = D.follow(fr, yx)
        res[prog] = dict(split_t=D.persistent_split(hist), n_end=hist[-1].get("n"), circ0=hist[0]["circ"],
                         circ25=next((h.get("circ") for h in hist if h["t"] == 25), None), circ50=hist[-1].get("circ"),
                         path=[(h["t"], round(h.get("cy", np.nan), 1), round(h.get("cx", np.nan), 1), h.get("n")) for h in hist[::5]])
    out[i] = res
    print(i, bs[i]["sign"], bs[i]["area"], "sham split", res["sham"]["split_t"], "n", res["sham"]["n_end"], "| feed split", res["feed"]["split_t"],
          "n", res["feed"]["n_end"], "circ0/25/50 sham", [round(x, 2) if x is not None else None for x in (res["sham"]["circ0"], res["sham"]["circ25"], res["sham"]["circ50"])],
          "feed", [round(x, 2) if x is not None else None for x in (res["feed"]["circ0"], res["feed"]["circ25"], res["feed"]["circ50"])], flush=True)
json.dump(out, open(f"{C.OUT}/mech/scan_feed_{sys.argv[1].replace(',', '_')}_{seed}.json", "w"), indent=0)
