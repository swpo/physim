"""BFF primordial soup (Aguera y Arcas et al. 2024, arXiv:2406.19108), numba.

Soup of N tapes of 64 bytes, uniformly random. Each epoch: a random permutation pairs tapes (A,B);
the 128-byte concatenation AB is executed as BFF code (instruction pointer, head0 and head1 start
at 0; heads wrap mod 128; '<' '>' move head0, '{' '}' move head1, '-' '+' change tape[head0],
'.' tape[head1] = tape[head0], ',' tape[head0] = tape[head1], '[' / ']' loop on tape[head0] with
nested matching; an unmatched bracket or 2^13 executed instructions ends the run; the run ends
when the instruction pointer leaves the tape); the tape is split back into A and B. Then every
byte mutates to a random byte with prob 0.00024. Every byte carries a tracer token (its origin:
initial byte or mutation), copied with it by '.' and ','; '+'/'-' keep the token.
Pairing and mutation use one serial RNG, execution is parallel and deterministic.
"""
import zlib, numpy as np
from numba import njit, prange

L = 64


@njit
def _exec(tape, tok, maxsteps):
    n = tape.shape[0]
    ip = 0; h0 = 0; h1 = 0; steps = 0
    while ip >= 0 and ip < n and steps < maxsteps:
        c = tape[ip]
        if c == 60:
            h0 = (h0 - 1) % n
        elif c == 62:
            h0 = (h0 + 1) % n
        elif c == 123:
            h1 = (h1 - 1) % n
        elif c == 125:
            h1 = (h1 + 1) % n
        elif c == 45:
            tape[h0] = (tape[h0] + 255) % 256
        elif c == 43:
            tape[h0] = (tape[h0] + 1) % 256
        elif c == 46:
            tape[h1] = tape[h0]; tok[h1] = tok[h0]
        elif c == 44:
            tape[h0] = tape[h1]; tok[h0] = tok[h1]
        elif c == 91:
            if tape[h0] == 0:
                d = 1; q = ip + 1
                while q < n:
                    if tape[q] == 91:
                        d += 1
                    elif tape[q] == 93:
                        d -= 1
                        if d == 0:
                            break
                    q += 1
                if q >= n:
                    return steps + 1
                ip = q
        elif c == 93:
            if tape[h0] != 0:
                d = 1; q = ip - 1
                while q >= 0:
                    if tape[q] == 93:
                        d += 1
                    elif tape[q] == 91:
                        d -= 1
                        if d == 0:
                            break
                    q -= 1
                if q < 0:
                    return steps + 1
                ip = q
        ip += 1; steps += 1
    return steps


@njit(parallel=True)
def epoch(soup, tok, perm, maxsteps, steps_out):
    npairs = perm.shape[0] // 2
    for i in prange(npairs):
        a = perm[2 * i]; b = perm[2 * i + 1]
        t = np.empty(2 * L, np.uint8); k = np.empty(2 * L, np.uint32)
        t[:L] = soup[a]; t[L:] = soup[b]; k[:L] = tok[a]; k[L:] = tok[b]
        steps_out[i] = _exec(t, k, maxsteps)
        soup[a] = t[:L]; soup[b] = t[L:]; tok[a] = k[:L]; tok[b] = k[L:]


class Soup:
    def __init__(self, seed, N=2 ** 17, mu=0.00024, maxsteps=2 ** 13):
        self.rng = np.random.default_rng(seed); self.N = N; self.mu = mu; self.maxsteps = maxsteps
        self.soup = self.rng.integers(0, 256, size=(N, L), dtype=np.uint8)
        self.tok = np.arange(N * L, dtype=np.uint32).reshape(N, L); self.next_tok = N * L
        self.steps = np.zeros(N // 2, np.int64); self.t = 0

    def step(self):
        perm = self.rng.permutation(self.N)
        epoch(self.soup, self.tok, perm, self.maxsteps, self.steps)
        m = self.rng.binomial(self.N * L, self.mu)
        if m:
            pos = self.rng.integers(0, self.N * L, size=m)
            self.soup.reshape(-1)[pos] = self.rng.integers(0, 256, size=m, dtype=np.uint8)
            self.tok.reshape(-1)[pos] = np.arange(self.next_tok, self.next_tok + m, dtype=np.uint32); self.next_tok += m
        self.t += 1

    def stats(self):
        raw = self.soup.tobytes(); n = len(raw)
        p = np.bincount(self.soup.reshape(-1), minlength=256) / n; p = p[p > 0]
        H0 = float(-(p * np.log2(p)).sum()); K = 8 * len(zlib.compress(raw, 6)) / n
        return dict(t=self.t, hoe=H0 - K, H0=H0, K=K, mean_steps=float(self.steps.mean()), uniq_tok=int(len(np.unique(self.tok))))
