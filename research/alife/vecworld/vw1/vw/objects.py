"""vw.objects -- a blob tracker on a periodic field level, as a pure JAX CoarseGrain.

BlobTracker(shape=(C, H, W), K, m_min, sigma, threshold) turns a field x (C, H, W) on the torus into K
object slots with persistent identities. It is a transducer (x, m) -> (y, m'): the memory m is a
deterministic function of the field's history, the readout y is a slice of m. One compiled JAX program:
no host callbacks, jit- and vmap-able, fixed shapes. Matching is discrete, so the coarse-graining is
declared differentiable=False (certificates.fisher refuses worlds that observe it); opaque=False.

Rules (the declared rules of the VW-0 host tracker integrate/lenia_world.Tracker, same tie-breaking):
  bodies    S = x[0] + x[1] + ... (channels added in order); B = gaussian_blur(S, sigma) with the
            normalised kernel and the summation order of scipy.ndimage.gaussian_filter(mode='wrap',
            truncate) (bit-identical to it); bodies are the 8-connected components of B > threshold on
            the torus whose mass sum(S) is >= m_min. Components are numbered by the smallest raster
            index (row * W + col) of their pixels (= the order of periodic_label + mass filter).
  features  per slot (NF = 12): present, mass, frac (mass fraction in channel frac_channel; 0 if C = 1),
            periodic centroid embedded on the torus E*cos, E*sin of 2 pi cx / W and of 2 pi cy / H
            (E = H / 2 pi; centroid = circular mean of S), radius of gyration rg = sqrt(tr),
            nematic q1 = (sxx - syy) / tr, q2 = 2 sxy / tr (second moments of S about the centroid,
            min-image; tr = max(sxx + syy, 1e-12)), velocity vx, vy (px per tick).
  matching  O[s, j] = pixels of component j that carried slot s in the previous slot map (present
            slots only). Greedy by decreasing overlap over the pairs with O > 0, ties by (s, j)
            lexicographic (stable sort); a pair is taken when slot and component are both free.
  fallback  a present slot with no overlap at all takes the nearest component that is free and
            overlaps no slot, if its torus distance to the predicted position (cy + vy, cx + vx) is
            < rg + fallback_px; slots in ascending order; components scanned in ascending index with
            strict < (the first minimum wins).
  fusion    a present, unmatched slot that overlaps a component (necessarily taken) is absorbed by the
            component it overlaps most (first maximum): event 'fused', slot emptied. The survivor gets
            event 'fusion' and velocity sum(m v) / sum(m) over [survivor, absorbed slots in ascending
            order] (previous masses and velocities; numpy's summation order).
  fission   a matched slot that also overlaps a component left free is a fission parent: event
            'fission', keeps its previous velocity ('fusion' takes precedence). The free component is a
            fission product: event 'fission', velocity of the slot overlapping it most (first maximum).
  birth     a free component that overlaps no slot: event 'birth', velocity 0. Fission products and
            births take free slots by decreasing mass (ties: component index), each the lowest free
            slot; free = not present at the previous tick (slots emptied this tick are not reused
            before the next tick); with no free slot the component stays untracked (slot map 0).
            New slots: age 0, uid = next_uid, then next_uid += 1.
  death     a present slot with no component and no fallback: event 'death', slot emptied.
  velocity  a continuing slot without event: min-image centroid displacement over the last tick.
  events    none 0, birth 1, fission 2, fusion 3, fused -1, death -2 (event of the last tick).

Memory (float64), the host tracker's layout followed by an overflow block:
    [slot map H*W (slot + 1, 0 = none) | slot table K x NS (NF features, cy, cx, age, event, uid) |
     globals 5 (next_uid, births, deaths, fusions, fissions; cumulative) |
     overflow 4 (ticks with more than max_raw raw components, ticks with more than max_kept kept
     components, peak raw count, peak kept count)].
Fixed shapes: at most max_raw components of B > threshold are measured (before the mass filter) and
at most max_kept bodies are matched (after it); components beyond a cap are untracked, and the tick is
counted in the overflow block (never silently). Readout y = slot table[:, :NF] (K * NF numbers).

Floating point. Sums over pixels use scatter-add in raster order (= numpy.bincount); products that
numpy rounds before adding are materialised behind lax.optimization_barrier so XLA cannot contract them
into fused multiply-adds, and divisions by constants are kept true divisions (_div). The field is read
behind a barrier, so the producer of x cannot be re-fused into the tracker. The blur, the masses,
overlaps and every discrete decision therefore agree with the numpy tracker bit for bit. Centroids can
differ in the last bit where numpy's arctan2 does: its AVX-512 kernel rounds differently from glibc's
atan2, which XLA's matches (with numpy's AVX-512 dispatch disabled the two trackers are bit-identical).
Distances in the fallback use jnp.hypot, not math.hypot; only an exact tie could be affected.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import jax
import jax.numpy as jnp
import numpy as np
from jax import lax

from .core import CoarseGrain

FEATURES = ("present", "mass", "frac_c1", "x_cos", "x_sin", "y_cos", "y_sin", "rg", "q1", "q2", "vx", "vy")
SLOT_EXTRA = ("cy", "cx", "age", "event", "uid")
GLOBALS = ("next_uid", "births", "deaths", "fusions", "fissions")
OVERFLOW = ("raw_overflow_ticks", "kept_overflow_ticks", "raw_peak", "kept_peak")
EVENTS = {"none": 0, "birth": 1, "fission": 2, "fusion": 3, "fused": -1, "death": -2}
NF, NS, NG, NO = len(FEATURES), len(FEATURES) + len(SLOT_EXTRA), len(GLOBALS), len(OVERFLOW)
_CY, _CX, _AGE, _EV, _UID = NF, NF + 1, NF + 2, NF + 3, NF + 4
_VX, _VY, _RG, _MASS = 10, 11, 7, 1

_bar = lax.optimization_barrier


def _div(a, c: float):
    """a / c rounded as IEEE division. XLA rewrites a division by a broadcast (a constant or a scalar)
    into a multiplication by its reciprocal, which rounds differently; an elementwise denominator
    (opaque zeros + c) keeps the true division, under jit, vmap and eager execution."""
    return a / (_bar(a * 0.0) + c)


def gaussian_kernel1d(sigma: float, truncate: float = 4.0) -> np.ndarray:
    """The normalised kernel of scipy.ndimage.gaussian_filter1d (order 0), built the same way."""
    radius = int(truncate * float(sigma) + 0.5)
    x = np.arange(-radius, radius + 1)
    phi = np.exp(-0.5 / (sigma * sigma) * x ** 2)
    return phi / phi.sum()


def gaussian_blur_wrap(S, sigma: float, truncate: float = 4.0):
    """scipy.ndimage.gaussian_filter(S, sigma, mode='wrap', truncate=truncate) for a 2-D array, bit for
    bit: axis 0 then axis 1; per output out = x0 w0, then out += (x[-j] + x[+j]) w_j for j = r .. 1 (the
    order of scipy's symmetric correlate1d), every product rounded before it is added."""
    w = gaussian_kernel1d(sigma, truncate)
    r = (len(w) - 1) // 2
    wc = [float(v) for v in w[r:]]

    if r > min(S.shape):
        raise ValueError("gaussian_blur_wrap: kernel radius larger than the grid")

    def axis(X, ax):
        n = X.shape[ax]
        Xp = jnp.concatenate([lax.slice_in_dim(X, n - r, n, axis=ax), X, lax.slice_in_dim(X, 0, r, axis=ax)], ax)

        def sl(o):                                                # X[(i + o) mod n]
            return lax.slice_in_dim(Xp, r + o, r + o + n, axis=ax)
        P = _bar(tuple([X * wc[0]] + [(sl(-j) + sl(j)) * wc[j] for j in range(r, 0, -1)]))
        out = P[0]
        for p in P[1:]:
            out = out + p
        return out
    return axis(axis(S, 0), 1)


def periodic_components(fg, min_steps: int = 8):
    """8-connected components of a boolean (H, W) mask on the torus. Returns (H*W,) int32: for a
    foreground pixel the smallest raster index of its component, H*W for background. Min-label
    propagation over the 3x3 neighbourhood with wrap (min_steps per round) plus one pointer jump per
    round, until a round changes nothing."""
    H, W = fg.shape
    HW = H * W
    dt = jnp.int16 if HW < 2 ** 15 else jnp.int32
    big = jnp.array(HW, dt)
    L0 = jnp.where(fg, jnp.arange(HW, dtype=dt).reshape(H, W), big)

    def nbmin(L):
        Lp = jnp.concatenate([L[:, -1:], L, L[:, :1]], 1)
        r = jnp.minimum(Lp[:, 1:-1], jnp.minimum(Lp[:, :-2], Lp[:, 2:]))
        rp = jnp.concatenate([r[-1:], r, r[:1]], 0)
        return jnp.where(fg, jnp.minimum(rp[1:-1], jnp.minimum(rp[:-2], rp[2:])), big)

    def body(c):
        L, _ = c
        N = L
        for _ in range(min_steps):
            N = nbmin(N)
        Nf = N.ravel()
        N = jnp.where(fg, Nf[jnp.minimum(Nf, HW - 1).astype(jnp.int32)].reshape(H, W), big)
        return N, jnp.any(N != L)
    L, _ = lax.while_loop(lambda c: c[1], body, (L0, jnp.array(True)))
    return L.ravel().astype(jnp.int32)


def numpy_sum(a, n):
    """numpy's float64 sum of the first n entries along the last axis (entries >= n must be 0):
    sequential from 0 for n < 8, eight interleaved accumulators (pairwise_sum's base case) for
    8 <= n <= 128."""
    L = a.shape[-1]
    seq = jnp.zeros(a.shape[:-1], a.dtype)
    for i in range(L):
        seq = seq + a[..., i]
    if L < 8:
        return seq
    Lp = -(-L // 8) * 8
    a = jnp.concatenate([a, jnp.zeros(a.shape[:-1] + (Lp - L,), a.dtype)], -1)
    i = jnp.arange(Lp)
    nb = (n - n % 8)[..., None]
    blk, tail = jnp.where(i < nb, a, 0.0), jnp.where(i >= nb, a, 0.0)
    r = blk[..., 0:8]
    for b in range(1, Lp // 8):
        r = r + blk[..., 8 * b:8 * b + 8]
    res = ((r[..., 0] + r[..., 1]) + (r[..., 2] + r[..., 3])) + ((r[..., 4] + r[..., 5]) + (r[..., 6] + r[..., 7]))
    for k in range(Lp):
        res = res + tail[..., k]
    return jnp.where(n < 8, seq, res)


@dataclass(frozen=True, eq=False)
class BlobTracker:
    """Blob tracker on a periodic field (rules in the module docstring). Use .coarse_grain()."""
    shape: tuple
    K: int
    m_min: float
    sigma: float
    threshold: float
    truncate: float = 4.0
    frac_channel: int = 1
    fallback_px: float = 4.0
    max_raw: int = 64
    max_kept: int = 32

    def __post_init__(self):
        object.__setattr__(self, "shape", tuple(int(s) for s in self.shape))
        if len(self.shape) != 3:
            raise ValueError("BlobTracker: shape must be (C, H, W)")
        if not 1 <= self.K <= 128:
            raise ValueError("BlobTracker: 1 <= K <= 128")
        if self.max_raw < 1 or self.max_kept < 1:
            raise ValueError("BlobTracker: caps must be >= 1")
        C, H, W = self.shape
        yy, xx = np.mgrid[0:H, 0:W]
        yy, xx = yy.ravel().astype(float), xx.ravel().astype(float)
        ty, tx = 2 * np.pi * yy / H, 2 * np.pi * xx / W          # the numpy tracker's tables
        object.__setattr__(self, "_tab", (yy, xx, np.sin(ty), np.cos(ty), np.sin(tx), np.cos(tx)))

    # ------------------------------------------------------------------ layout
    @property
    def HW(self) -> int:
        return self.shape[1] * self.shape[2]

    @property
    def n_m(self) -> int:
        """Memory length: H*W + K*NS + 5 globals + 4 overflow entries."""
        return self.HW + self.K * NS + NG + NO

    @property
    def n_m_host(self) -> int:
        """Length of the host tracker's memory (the same layout without the overflow block)."""
        return self.HW + self.K * NS + NG

    @property
    def n_out(self) -> int:
        return self.K * NF

    def names(self) -> list:
        return [f"slot{s}.{f}" for s in range(self.K) for f in FEATURES]

    def split(self, m) -> dict:
        """Views of a memory vector (or a batch, leading axes kept): map, table, globals, overflow."""
        HW, K = self.HW, self.K
        lead = m.shape[:-1]
        return {"map": m[..., :HW], "table": m[..., HW:HW + K * NS].reshape(lead + (K, NS)),
                "globals": m[..., HW + K * NS:HW + K * NS + NG], "overflow": m[..., HW + K * NS + NG:]}

    # ------------------------------------------------------------------ components
    def components(self, x) -> dict:
        """Bodies of one field x (C, H, W): raw-index map, per-component statistics (max_kept rows)."""
        C, H, W = self.shape
        HW, NR, NC = self.HW, self.max_raw, self.max_kept
        A = _bar(jnp.reshape(x, self.shape))        # the field as stored: no re-fusion with its producer
        S = A[0]
        for c in range(1, C):
            S = S + A[c]
        fg = gaussian_blur_wrap(S, self.sigma, self.truncate) > self.threshold
        L = periodic_components(fg)
        fgf = fg.ravel()
        root = fgf & (L == jnp.arange(HW, dtype=jnp.int32))
        rank = jnp.cumsum(root.astype(jnp.int32)) - 1
        n_raw = rank[-1] + 1
        raw = jnp.where(fgf, rank[jnp.minimum(L, HW - 1)], NR)
        raw = jnp.minimum(raw, NR)                                  # NR = background or beyond the cap
        yy, xx, sy, cy_, sx, cx_ = (jnp.asarray(t) for t in self._tab)
        s = S.ravel()
        f1 = A[self.frac_channel].ravel() if C > 1 else jnp.zeros_like(s)
        cols = jnp.stack([s, f1, _bar(s * sy), _bar(s * cy_), _bar(s * sx), _bar(s * cx_)], 1)
        R = jnp.zeros((NR + 1, 6), s.dtype).at[raw].add(cols)[:NR]  # per raw component, raster order
        mass = R[:, 0]
        valid = jnp.arange(NR) < n_raw
        msafe = jnp.where(valid, mass, 1.0)
        cy = _div(jnp.arctan2(R[:, 2], R[:, 3]) * H, 2 * np.pi) % H
        cx = _div(jnp.arctan2(R[:, 4], R[:, 5]) * W, 2 * np.pi) % W
        ri = jnp.minimum(raw, NR - 1)
        dy = (yy - cy[ri] + H / 2) % H - H / 2
        dx = (xx - cx[ri] + W / 2) % W - W / 2
        M2 = jnp.stack([_bar(_bar(s * dy) * dy), _bar(_bar(s * dx) * dx), _bar(_bar(s * dx) * dy)], 1)
        M2 = jnp.zeros((NR + 1, 3), s.dtype).at[raw].add(M2)[:NR]
        syy, sxx, sxy = M2[:, 0] / msafe, M2[:, 1] / msafe, M2[:, 2] / msafe
        keep = valid & (mass >= self.m_min)
        krank = jnp.cumsum(keep.astype(jnp.int32)) - 1
        n_kept = krank[-1] + 1
        kid = jnp.where(keep & (krank < NC), krank, NC)
        # kept component j -> raw component index (ascending raw index = ascending min raster index)
        k2r = jnp.full((NC + 1,), NR, jnp.int32).at[kid].set(jnp.arange(NR, dtype=jnp.int32))[:NC]
        kvalid = jnp.arange(NC) < jnp.minimum(n_kept, NC)
        g = jnp.minimum(k2r, NR - 1)
        tr = jnp.maximum(sxx + syy, 1e-12)
        lab = jnp.append(kid, NC)[raw]                              # kept index per pixel, NC = none
        return {"lab": lab, "raw": raw, "n_raw": n_raw, "n_kept": n_kept, "valid": kvalid, "k2r": g,
                "mass": mass[g], "f1": R[g, 1] / msafe[g], "cy": cy[g], "cx": cx[g],
                "rg": jnp.sqrt(tr[g]), "q1": ((sxx - syy) / tr)[g], "q2": (2 * sxy / tr)[g]}

    def _feat(self, c):
        """Feature rows (max_kept, NF - 2) of the components (velocity added by the caller)."""
        C, H, W = self.shape
        E = H / (2 * np.pi)
        thx, thy = _div(2 * np.pi * c["cx"], W), _div(2 * np.pi * c["cy"], H)
        one = jnp.ones_like(c["mass"])
        return jnp.stack([one, c["mass"], c["f1"], E * jnp.cos(thx), E * jnp.sin(thx), E * jnp.cos(thy),
                          E * jnp.sin(thy), c["rg"], c["q1"], c["q2"]], 1)

    # ------------------------------------------------------------------ one memory update
    def _update(self, prev, T, g, ovf, x):
        C, H, W = self.shape
        K, NC, HW = self.K, self.max_kept, self.HW
        c = self.components(x)
        lab, kvalid = c["lab"], c["valid"]
        active = T[:, 0] > 0.5
        # overlaps of the previous slot map with the kept components (present slots only)
        O = jnp.zeros(((K + 1) * (NC + 1),), jnp.int32).at[prev * (NC + 1) + jnp.where(lab < NC, lab + 1, 0)].add(1)
        O = jnp.where(active[:, None], O.reshape(K + 1, NC + 1)[1:, 1:], 0)
        rowsum, colsum = O.sum(1), O.sum(0)
        sidx, jidx = jnp.arange(K, dtype=jnp.int32), jnp.arange(NC, dtype=jnp.int32)

        def greedy(_, st):                       # = stable sort by decreasing overlap + first-come
            slot_of, assign = st
            Om = jnp.where((slot_of < 0)[:, None] & (assign < 0)[None, :], O, 0).ravel()
            k = jnp.argmax(Om)
            ok = Om[k] > 0
            s, j = (k // NC).astype(jnp.int32), (k % NC).astype(jnp.int32)
            return (jnp.where(ok & (sidx == s), j, slot_of), jnp.where(ok & (jidx == j), s, assign))
        slot_of, assign = lax.fori_loop(0, K, greedy, (jnp.full((K,), -1, jnp.int32), jnp.full((NC,), -1, jnp.int32)))

        def mi(d, L):
            return (d + L / 2) % L - L / 2

        def fallback(s, st):                     # nearest free, non-overlapping component
            slot_of, assign = st
            py, px = T[s, _CY] + T[s, _VY], T[s, _CX] + T[s, _VX]
            d = jnp.hypot(mi(c["cy"] - py, H), mi(c["cx"] - px, W))
            d = jnp.where(kvalid & (assign < 0) & (colsum == 0), d, jnp.inf)
            j = jnp.argmin(d).astype(jnp.int32)
            ok = active[s] & (slot_of[s] < 0) & (rowsum[s] == 0) & (d[j] < T[s, _RG] + self.fallback_px)
            return (jnp.where(ok & (sidx == s), j, slot_of), jnp.where(ok & (jidx == j), jnp.int32(s), assign))
        slot_of, assign = lax.fori_loop(0, K, fallback, (slot_of, assign))

        # absorbed (fused) slots and their survivors
        gone = active & (slot_of < 0)
        fused = gone & (rowsum > 0)
        target = jnp.where(fused, jnp.argmax(O, 1), -1)
        cont = slot_of >= 0
        P = cont[:, None] & (target[None, :] == slot_of[:, None]) & (target[None, :] >= 0)   # P[s, p]
        npar = P.sum(1)
        key = jnp.where(sidx[None, :] == sidx[:, None], -1, jnp.where(P, sidx[None, :], K + sidx[None, :]))
        order = jnp.argsort(key, axis=1)                  # [s, absorbed slots ascending, others]
        nn = 1 + npar
        live = jnp.arange(K)[None, :] < nn[:, None]
        mm = jnp.where(live, T[order, _MASS], 0.0)
        msum = numpy_sum(mm, nn)
        fvy = numpy_sum(_bar(mm * jnp.where(live, T[order, _VY], 0.0)), nn) / jnp.where(cont, msum, 1.0)
        fvx = numpy_sum(_bar(mm * jnp.where(live, T[order, _VX], 0.0)), nn) / jnp.where(cont, msum, 1.0)
        # continuing slots
        js = jnp.maximum(slot_of, 0)
        lost = ((assign < 0)[None, :] & (O > 0)).any(1)
        dy, dx = mi(c["cy"][js] - T[:, _CY], H), mi(c["cx"][js] - T[:, _CX], W)
        has_par = npar > 0
        ev_c = jnp.where(has_par, EVENTS["fusion"], jnp.where(lost, EVENTS["fission"], EVENTS["none"]))
        vy_c = jnp.where(has_par, fvy, jnp.where(lost, T[:, _VY], dy))
        vx_c = jnp.where(has_par, fvx, jnp.where(lost, T[:, _VX], dx))
        F = self._feat(c)
        row_c = jnp.concatenate([F[js], jnp.stack([vx_c, vy_c, c["cy"][js], c["cx"][js], T[:, _AGE] + 1,
                                                   ev_c.astype(T.dtype), T[:, _UID]], 1)], 1)
        # new components: fission products and births, by decreasing mass, lowest free slot
        newc = kvalid & (assign < 0)
        srt = jnp.argsort(jnp.where(newc, -c["mass"], jnp.inf))
        rank = jnp.zeros((NC,), jnp.int32).at[srt].set(jnp.arange(NC, dtype=jnp.int32))
        free = ~active
        n_free = free.sum()
        free_list = jnp.nonzero(free, size=K, fill_value=K)[0]
        placed = newc & (rank < n_free)
        slot_new = jnp.where(placed, free_list[jnp.minimum(rank, K - 1)], K)
        par = colsum > 0
        p = jnp.argmax(O, 0)
        ev_n = jnp.where(par, EVENTS["fission"], EVENTS["birth"])
        vy_n, vx_n = jnp.where(par, T[p, _VY], 0.0), jnp.where(par, T[p, _VX], 0.0)
        row_n = jnp.concatenate([F, jnp.stack([vx_n, vy_n, c["cy"], c["cx"], jnp.zeros(NC), ev_n.astype(T.dtype),
                                               g[0] + rank], 1)], 1)
        comp_of_new = jnp.full((K + 1,), -1, jnp.int32).at[slot_new].set(jidx.astype(jnp.int32))[:K]
        isnew = comp_of_new >= 0
        row_new = row_n[jnp.maximum(comp_of_new, 0)]
        row_gone = jnp.zeros((K, NS), T.dtype).at[:, _EV].set(jnp.where(fused, EVENTS["fused"], EVENTS["death"]))
        newT = jnp.where(cont[:, None], row_c, jnp.where(isnew[:, None], row_new,
                                                          jnp.where(gone[:, None], row_gone, 0.0)))
        n_new = placed.sum()
        births, fissions = (placed & ~par).sum(), (placed & par).sum()
        deaths, fusions = (gone & ~fused).sum(), fused.sum()
        g = g + jnp.stack([n_new, births, deaths, fusions, fissions]).astype(g.dtype)
        assign = jnp.where(placed, slot_new, assign)
        smap = jnp.where(lab < NC, jnp.append(assign, -1)[lab] + 1, 0)
        ovf = jnp.stack([ovf[0] + (c["n_raw"] > self.max_raw), ovf[1] + (c["n_kept"] > NC),
                         jnp.maximum(ovf[2], c["n_raw"]), jnp.maximum(ovf[3], c["n_kept"])]).astype(ovf.dtype)
        return jnp.concatenate([smap.astype(T.dtype), newT.ravel(), g, ovf])

    def init_memory(self, x):
        dt = jnp.result_type(float)
        return self._update(jnp.zeros((self.HW,), jnp.int32), jnp.zeros((self.K, NS), dt),
                            jnp.zeros((NG,), dt).at[0].set(1.0), jnp.zeros((NO,), dt), x)

    def update_memory(self, m, x):
        d = self.split(_bar(m))
        return self._update(d["map"].astype(jnp.int32), d["table"], d["globals"], d["overflow"], x)

    def phi(self, x, m, audit: bool = False):
        HW, K = self.HW, self.K
        y = m[HW:HW + K * NS].reshape(K, NS)[:, :NF].reshape(-1)
        return jnp.concatenate([y, m[HW + K * NS:HW + K * NS + NG]]) if audit else y

    def coarse_grain(self, name: Optional[str] = None, audit: bool = False) -> CoarseGrain:
        """The tracker as a CoarseGrain: output K*NF (+ 5 globals if audit), memory n_m numbers."""
        return CoarseGrain(phi=lambda x, m: self.phi(x, m, audit), init_memory=self.init_memory,
                           update_memory=self.update_memory, differentiable=False, opaque=False,
                           name=name or f"blobs{self.K}" + ("+audit" if audit else ""))


def blob_tracker(shape, K: int, m_min: float, sigma: float, threshold: float, name: Optional[str] = None,
                 audit: bool = False, **kw):
    """(CoarseGrain, BlobTracker) for a periodic field of the given (C, H, W) shape (rules: module doc)."""
    tr = BlobTracker(shape=tuple(shape), K=K, m_min=m_min, sigma=sigma, threshold=threshold, **kw)
    return tr.coarse_grain(name, audit), tr


__all__ = ["BlobTracker", "blob_tracker", "gaussian_blur_wrap", "gaussian_kernel1d", "periodic_components",
           "numpy_sum", "FEATURES", "SLOT_EXTRA", "GLOBALS", "OVERFLOW", "EVENTS", "NF", "NS"]
