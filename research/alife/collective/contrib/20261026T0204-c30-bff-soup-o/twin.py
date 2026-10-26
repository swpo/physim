"""In-world neutral twin for a BFF replicator soup.
1. Re-run the seeded soup (same seed, deterministic) to epoch E0 and snapshot it.
2. Measure, over the next M epochs of the REAL soup, how interactions end: exact copy A->B (B'==A, A'==A),
   exact copy B->A, error copy (the overwritten half within 1-4 bytes of the copier), or other.
3. Neutral twin: from the E0 snapshot, each epoch pairs tapes at random and, with the measured
   probabilities, copies A onto B or B onto A exactly, or with k random byte changes (k drawn from the
   measured error sizes), or leaves both; then the same background mutation (0.00024 per byte).
   No code is executed, so no kind has an advantage; drift and innovation rates match the real soup.
4. Census both every 50 epochs (tapes with >= 3 copies) from E0 to E1.
python twin.py SEED N E0 M E1 OUTDIR"""
import sys, os, json, gzip, time, numpy as np
from numba import njit, prange
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from seeded import planted
from bff import Soup, _exec, L


@njit(parallel=True)
def classify_epoch(soup, tok, perm, maxsteps, cls, dist):
    npairs = perm.shape[0] // 2
    for i in prange(npairs):
        a = perm[2 * i]; b = perm[2 * i + 1]
        A = soup[a].copy(); B = soup[b].copy()
        t = np.empty(2 * L, np.uint8); k = np.empty(2 * L, np.uint32)
        t[:L] = A; t[L:] = B; k[:L] = tok[a]; k[L:] = tok[b]
        _exec(t, k, maxsteps)
        dA = 0; dB = 0; dBA = 0; dAB = 0
        for j in range(L):
            dA += t[j] != A[j]; dB += t[L + j] != B[j]
            dAB += t[L + j] != A[j]; dBA += t[j] != B[j]
        if dAB == 0 and dA == 0:
            cls[i] = 1; dist[i] = 0
        elif dBA == 0 and dB == 0:
            cls[i] = 2; dist[i] = 0
        elif dAB <= 4 and dA <= 4:
            cls[i] = 3; dist[i] = dAB
        elif dBA <= 4 and dB <= 4:
            cls[i] = 4; dist[i] = dBA
        else:
            cls[i] = 0; dist[i] = 0
        soup[a] = t[:L]; soup[b] = t[L:]; tok[a] = k[:L]; tok[b] = k[L:]


def census(soup, e):
    v = np.ascontiguousarray(soup).view(np.dtype((np.void, 64))).reshape(-1)
    u, c = np.unique(v, return_counts=True); keep = c >= 3
    return {"t": e, "n": int(len(soup)), "census": {bytes(x).hex(): int(k) for x, k in zip(u[keep], c[keep])}}


if __name__ == "__main__":
    seed, N, E0, M, E1, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    P = planted(); S = Soup(seed, N=N); S.soup[:32] = P
    for e in range(E0): S.step()
    snap = S.soup.copy()
    counts = np.zeros(5); dists = []
    for e in range(M):           # measurement epochs: the real dynamics, classified
        perm = S.rng.permutation(N); cls = np.zeros(N // 2, np.int64); dist = np.zeros(N // 2, np.int64)
        classify_epoch(S.soup, S.tok, perm, S.maxsteps, cls, dist)
        counts += np.bincount(cls, minlength=5); dists += dist[(cls == 3) | (cls == 4)].tolist()
        m = S.rng.binomial(N * L, S.mu)
        if m:
            pos = S.rng.integers(0, N * L, size=m); S.soup.reshape(-1)[pos] = S.rng.integers(0, 256, size=m, dtype=np.uint8)
    pr = counts / counts.sum(); dd = np.bincount(np.array(dists, int), minlength=5)[1:]; dd = dd / max(1, dd.sum())
    rates = dict(other=pr[0], exact_AB=pr[1], exact_BA=pr[2], error_AB=pr[3], error_BA=pr[4], error_size_dist=dd.tolist())
    print("rates", {k: (round(v, 4) if not isinstance(v, list) else np.round(v, 3).tolist()) for k, v in rates.items()}, flush=True)
    # neutral twin from the snapshot
    rng = np.random.default_rng(10_000 + seed); soup = snap.copy(); cens = [census(soup, E0)]
    cum = np.cumsum(pr); t0 = time.time()
    for e in range(E0 + 1, E1 + 1):
        perm = rng.permutation(N); A = perm[0::2]; B = perm[1::2]; u = rng.random(N // 2)
        c = np.searchsorted(cum, u, side="right")           # 0 other, 1 exAB, 2 exBA, 3 errAB, 4 errBA
        src = np.where((c == 1) | (c == 3), A, B); dst = np.where((c == 1) | (c == 3), B, A); doit = c > 0
        soup[dst[doit]] = soup[src[doit]]
        err = dst[(c == 3) | (c == 4)]
        if len(err):
            ks = rng.choice(np.arange(1, 5), size=len(err), p=dd if dd.sum() > 0 else None)
            for kk in range(1, 5):
                rows = err[ks == kk]
                for _ in range(kk):
                    soup[rows, rng.integers(0, L, size=len(rows))] = rng.integers(0, 256, size=len(rows), dtype=np.uint8)
        m = rng.binomial(N * L, 0.00024)
        if m:
            pos = rng.integers(0, N * L, size=m); soup.reshape(-1)[pos] = rng.integers(0, 256, size=m, dtype=np.uint8)
        if e % 50 == 0: cens.append(census(soup, e))
    json.dump(dict(rates=rates, E0=E0, census=cens), gzip.open(f"{out}/twin_census_s{seed}.json.gz", "wt"))
    print("twin done", round(time.time() - t0), "s", flush=True)
