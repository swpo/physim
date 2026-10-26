"""Functional kinds in a BFF census: a tape's signature lists, for each of its 64 positions, the byte if
the instruction pointer executes it and it is a BFF instruction or zero, "no-op" if executed otherwise,
"not executed" else (run on one fixed random food tape); tapes that differ only in bytes that are
never executed, or are executed as no-ops, are one functional kind.
python functional.py CENSUS OUT.json"""
import sys, os, json, gzip, numpy as np
from numba import njit, prange
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from o_measure import census_shadow


@njit
def _trace(tape, maxsteps, visited):
    n = tape.shape[0]; ip = 0; h0 = 0; h1 = 0; steps = 0
    while ip >= 0 and ip < n and steps < maxsteps:
        if ip < 64: visited[ip] = True
        c = tape[ip]
        if c == 60: h0 = (h0 - 1) % n
        elif c == 62: h0 = (h0 + 1) % n
        elif c == 123: h1 = (h1 - 1) % n
        elif c == 125: h1 = (h1 + 1) % n
        elif c == 45: tape[h0] = (tape[h0] + 255) % 256
        elif c == 43: tape[h0] = (tape[h0] + 1) % 256
        elif c == 46: tape[h1] = tape[h0]
        elif c == 44: tape[h0] = tape[h1]
        elif c == 91:
            if tape[h0] == 0:
                d = 1; q = ip + 1
                while q < n:
                    if tape[q] == 91: d += 1
                    elif tape[q] == 93:
                        d -= 1
                        if d == 0: break
                    q += 1
                if q >= n: return steps + 1
                ip = q
        elif c == 93:
            if tape[h0] != 0:
                d = 1; q = ip - 1
                while q >= 0:
                    if tape[q] == 93: d += 1
                    elif tape[q] == 91:
                        d -= 1
                        if d == 0: break
                    q -= 1
                if q < 0: return steps + 1
                ip = q
        ip += 1; steps += 1
    return steps


@njit(parallel=True)
def traces(tapes, food, out_vis, out_ok):
    for i in prange(tapes.shape[0]):
        t = np.empty(128, np.uint8); t[:64] = tapes[i]; t[64:] = food
        vis = np.zeros(64, np.bool_); _trace(t, 8192, vis)
        out_vis[i] = vis; ok = True
        for j in range(64):
            if t[64 + j] != tapes[i, j]: ok = False
        out_ok[i] = ok


def signatures(hexs, seed=0):
    tapes = np.array([np.frombuffer(bytes.fromhex(h), np.uint8) for h in hexs])
    food = np.random.default_rng(seed).integers(0, 256, 64).astype(np.uint8)
    vis = np.zeros((len(hexs), 64), np.bool_); ok = np.zeros(len(hexs), np.bool_)
    traces(tapes, food, vis, ok)
    ins = np.isin(tapes, np.frombuffer(b"<>{}-+.,[]\x00", np.uint8))
    code = np.where(vis & ins, tapes, np.where(vis, 1, 2)).astype(np.uint8)   # executed instruction or zero / executed no-op / not executed
    sig = [bytes(c.tolist()).hex() for c in code]
    return sig, ok, vis.sum(1)


if __name__ == "__main__":
    cens = json.load(gzip.open(sys.argv[1], "rt"))
    if isinstance(cens, dict): cens = cens["census"]
    allk = sorted({g for c in cens for g in c["census"]})
    sig, ok, nvis = signatures(allk); m = dict(zip(allk, sig)); okd = dict(zip(allk, ok.tolist())); nv = dict(zip(allk, nvis.tolist()))
    rows = []
    for c in cens:
        r = {}
        for g, n in c["census"].items(): r[m[g]] = r.get(m[g], 0) + n
        rows.append({"t": c["t"], "census": r, "replicating_share": sum(n for g, n in c["census"].items() if okd[g]) / c["n"],
                     "mean_executed": float(np.average([nv[g] for g in c["census"]], weights=list(c["census"].values()))) if c["census"] else 0})
    json.dump(rows, gzip.open(sys.argv[2], "wt"))
    fk = {g for r in rows for g in r["census"]}
    print("tape kinds", len(allk), "functional kinds", len(fk), "replicating share first/last", round(rows[0]["replicating_share"], 3), round(rows[-1]["replicating_share"], 3),
          "executed bytes first/last", round(rows[0]["mean_executed"], 1), round(rows[-1]["mean_executed"], 1))
