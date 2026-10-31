import numpy as np, json
OUT = "/home/user/evalwork/pm_cips_eval/cips_accept"
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
T5 = list(range(0, 51, 5))
F = ("e", "p", "F", "s")
res = {}
for prog in ("p_d0", "Fm_d0"):
    a = np.load(f"{OUT}/det_{prog}_dt0.1.npz"); b = np.load(f"{OUT}/det_{prog}_dt0.05.npz")
    for lv in ("0.01", "0.03", "0.1"):
        z = np.load(f"{OUT}/noise_{lv}.npz")
        for win in (10, 50):
            row = {}
            for q, s in enumerate(("d0", "d1", "gl")):
                ti = [TIMES.index(t) for t in T5 if 0 < t <= win]
                tn = [T5.index(t) for t in T5 if 0 < t <= win]
                d = a[f"query{q}"][0][ti] - b[f"query{q}"][0][ti]
                sp = np.abs(z[f"m0_q{q}"][0][tn] - z[f"m1_q{q}"][0][tn]) / np.sqrt(2)
                row[s] = {f: round(float(np.sqrt((d[:, i] ** 2).mean()) / (np.sqrt((sp[:, i] ** 2).mean()) + 1e-15)), 2) for i, f in enumerate(F)}
            res[f"{prog}/L{lv}/{win}tu"] = row
            print(prog, lv, win, row)
json.dump(res, open(f"{OUT}/det_screen.json", "w"), indent=1)
