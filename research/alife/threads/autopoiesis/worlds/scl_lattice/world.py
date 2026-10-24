"""Lattice SCL (substrate-catalyst-link) autopoiesis, after Varela, Maturana & Uribe (1974)
and McMullin & Varela (1997), vectorized as a numba random-sequential update.

Cells hold one of: hole (0), substrate S (1), catalyst K (2), link L (3).
Links carry up to 2 bonds to Moore neighbours (bitmask per cell, symmetric).

Per site update (H*W random picks per step):
  motion      S, K, free L hop into a hole; K and free L displace S (swap).
              Bonded L never moves. K and free L cannot cross bonded L.
  permeation  S facing a bonded L jumps over it into a hole beyond (p_perm): the membrane
              is permeable to substrate only.
  production  K + 2 S (Moore neighbours) -> K + L + hole (p_prod).
  bonding     L with < 2 bonds bonds to a neighbouring L with < 2 bonds, if the bond angle at
              both ends is >= MIN_SEP*45 deg and no diagonal bond is crossed. Extending a chain
              (partner already bonded) has p_ext, starting a new pair p_init.
  decay       L -> 2 S (needs a hole neighbour), bonds removed (p_dis); bonds also break (p_bb).
Mass (S=1, L=2) is conserved apart from catalyst.

Initial condition (IC="cell"): a planted ring of bonded links around one catalyst, as in the
classic SCL experiments. IC="random": catalysts and substrate scattered, no membranes.
"""
import numpy as np
import numba as nb

META = {
    "name": "scl-lattice",
    "family": "autopoiesis",
    "parent": None,
    "mutation": "reference lattice SCL (McMullin-Varela rules: bond angle >= 90 deg, no crossing, splicing)",
    "size": (64, 64),
    "steps_per_frame": 10,
    "dt": 1.0,
    "channels": ["S", "K", "L free", "L bonded"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(p_move=1.0, p_perm=0.5, p_prod=0.05, p_ext=0.05, p_init=0.002, p_join=0.9, p_splice=1.0, p_dis=0.0002, p_disf=0.005, p_bb=0.0,
         MIN_SEP=3, inhibit=0, s_density=0.7, n_cat=1, ring_r=9, IC="cell")

DY = np.array([-1, -1, 0, 1, 1, 1, 0, -1], np.int64)   # direction d: 0=N,1=NE,2=E,...,7=NW (clockwise)
DX = np.array([0, 1, 1, 1, 0, -1, -1, -1], np.int64)


@nb.njit(cache=True)
def _nb(y, x, d, H, W):
    return (y + DY[d]) % H, (x + DX[d]) % W


@nb.njit(cache=True)
def _nbonds(b):
    n = 0
    for d in range(8):
        if (b >> d) & 1:
            n += 1
    return n


@nb.njit(cache=True)
def _angle_ok(b, d, min_sep):
    # every existing bond direction e must be >= min_sep steps away from d (circular)
    for e in range(8):
        if (b >> e) & 1:
            s = abs(e - d)
            s = min(s, 8 - s)
            if s < min_sep:
                return False
    return True


@nb.njit(cache=True)
def _crosses(B, y, x, d, H, W):
    # diagonal bond from (y,x) in direction d crosses the other diagonal of the same 2x2 square
    if d % 2 == 0:
        return False
    ya, xa = _nb(y, x, (d - 1) % 8, H, W)   # the two orthogonal neighbours spanning the square
    yb, xb = _nb(y, x, (d + 1) % 8, H, W)
    # direction from a to b
    for e in range(8):
        if (ya + DY[e]) % H == yb and (xa + DX[e]) % W == xb:
            return (B[ya, xa] >> e) & 1 == 1
    return False


@nb.njit(cache=True)
def _clear_bonds(B, y, x, H, W):
    b = B[y, x]
    for d in range(8):
        if (b >> d) & 1:
            ny, nx = _nb(y, x, d, H, W)
            B[ny, nx] &= ~np.uint8(1 << ((d + 4) % 8))
    B[y, x] = 0


@nb.njit(cache=True)
def _try_bond(T, B, y, x, d, H, W, p_ext, p_init, p_join, min_sep):
    ny, nx = _nb(y, x, d, H, W)
    if T[ny, nx] != 3 or (B[y, x] >> d) & 1:
        return
    b0, b1 = B[y, x], B[ny, nx]
    n0, n1 = _nbonds(b0), _nbonds(b1)
    if n0 >= 2 or n1 >= 2:
        return
    p = p_join if (n0 == 1 and n1 == 1) else (p_ext if (n0 + n1) > 0 else p_init)
    if np.random.random() >= p:
        return
    if not _angle_ok(b0, d, min_sep) or not _angle_ok(b1, (d + 4) % 8, min_sep):
        return
    if _crosses(B, y, x, d, H, W):
        return
    B[y, x] |= np.uint8(1 << d)
    B[ny, nx] |= np.uint8(1 << ((d + 4) % 8))


@nb.njit(cache=True)
def _try_splice(T, B, y, x, H, W, p_splice, min_sep):
    # a free link touching two chain ends bonds to both at once (gap repair)
    ends = np.empty(8, np.int64)
    m = 0
    for d in range(8):
        ny, nx = _nb(y, x, d, H, W)
        if T[ny, nx] == 3 and _nbonds(B[ny, nx]) == 1:
            ends[m] = d
            m += 1
    if m < 2 or np.random.random() >= p_splice:
        return
    for i in range(m):
        for j in range(i + 1, m):
            d1, d2 = ends[i], ends[j]
            s = abs(d1 - d2)
            s = min(s, 8 - s)
            if s < min_sep:
                continue
            y1, x1 = _nb(y, x, d1, H, W)
            y2, x2 = _nb(y, x, d2, H, W)
            if not _angle_ok(B[y1, x1], (d1 + 4) % 8, min_sep) or not _angle_ok(B[y2, x2], (d2 + 4) % 8, min_sep):
                continue
            if _crosses(B, y, x, d1, H, W) or _crosses(B, y, x, d2, H, W):
                continue
            B[y, x] |= np.uint8((1 << d1) | (1 << d2))
            B[y1, x1] |= np.uint8(1 << ((d1 + 4) % 8))
            B[y2, x2] |= np.uint8(1 << ((d2 + 4) % 8))
            return


@nb.njit(cache=True)
def _near_chain(T, B, y, x, H, W):
    # chain-based bond inhibition (McMullin): a free link touching a doubly bonded link
    # may only splice, not initiate or extend
    for d in range(8):
        ny, nx = _nb(y, x, d, H, W)
        if T[ny, nx] == 3 and _nbonds(B[ny, nx]) == 2:
            return True
    return False


@nb.njit(cache=True)
def _sweep(T, B, p_move, p_perm, p_prod, p_ext, p_init, p_join, p_splice, p_dis, p_disf, p_bb, min_sep, inhibit):
    H, W = T.shape
    for _ in range(H * W):
        y = np.random.randint(H)
        x = np.random.randint(W)
        t = T[y, x]
        if t == 0:
            continue
        if t == 3:
            # decay
            if np.random.random() < (p_dis if B[y, x] != 0 else p_disf):
                d = np.random.randint(8)
                ny, nx = _nb(y, x, d, H, W)
                if T[ny, nx] == 0:
                    _clear_bonds(B, y, x, H, W)
                    T[y, x] = 1
                    T[ny, nx] = 1
                    continue
            if p_bb > 0 and B[y, x] != 0 and np.random.random() < p_bb:
                _clear_bonds(B, y, x, H, W)
            # bonding attempt with a random Moore neighbour
            if B[y, x] == 0 and p_splice > 0:
                _try_splice(T, B, y, x, H, W, p_splice, min_sep)
            if (B[y, x] == 0 or np.random.random() < 0.5) and not (inhibit and B[y, x] == 0 and _near_chain(T, B, y, x, H, W)):
                d = np.random.randint(8)
                _try_bond(T, B, y, x, d, H, W, p_ext, p_init, p_join, min_sep)
            if B[y, x] != 0:
                continue  # bonded links are immobile
        if t == 2:
            # production: two random Moore neighbours that are substrate
            d1 = np.random.randint(8)
            d2 = np.random.randint(8)
            if d1 != d2 and np.random.random() < p_prod:
                y1, x1 = _nb(y, x, d1, H, W)
                y2, x2 = _nb(y, x, d2, H, W)
                if T[y1, x1] == 1 and T[y2, x2] == 1:
                    T[y1, x1] = 3
                    B[y1, x1] = 0
                    T[y2, x2] = 0
        # motion (von Neumann)
        if np.random.random() < p_move:
            d = 2 * np.random.randint(4)
            ny, nx = _nb(y, x, d, H, W)
            u = T[ny, nx]
            if u == 0:
                T[ny, nx] = t
                T[y, x] = 0
            elif u == 1 and t >= 2:
                T[ny, nx] = t
                T[y, x] = 1
            elif t == 1 and u == 3 and B[ny, nx] != 0 and np.random.random() < p_perm:
                fy, fx = _nb(ny, nx, d, H, W)
                if T[fy, fx] == 0:
                    T[fy, fx] = 1
                    T[y, x] = 0


@nb.njit(cache=True)
def _seed(s):
    np.random.seed(s)


def init(seed, size):
    H, W = size
    rng = np.random.default_rng(seed)
    T = np.where(rng.random((H, W)) < P["s_density"], 1, 0).astype(np.int8)
    B = np.zeros((H, W), np.uint8)
    if P["IC"] == "cell":
        cy, cx = H // 2, W // 2
        _plant_ring(T, B, cy, cx, P["ring_r"])
        for k in range(P["n_cat"]):
            T[cy + (k % 2) * 2 - (P["n_cat"] > 1), cx + (k // 2) * 2] = 2
    else:
        idx = rng.choice(H * W, P["n_cat"], replace=False)
        T.flat[idx] = 2
    _seed(int(seed) * 7919 + 13)
    return {"T": T, "B": B, "t": 0}


def _plant_ring(T, B, cy, cx, r):
    # walk an 8-connected digital circle and bond consecutive cells
    ang = np.linspace(0, 2 * np.pi, 400, endpoint=False)
    pts = []
    for a in ang:
        p = (int(round(cy + r * np.sin(a))), int(round(cx + r * np.cos(a))))
        if not pts or p != pts[-1]:
            pts.append(p)
    if pts[0] == pts[-1]:
        pts.pop()
    # drop points that make the path non-simple (keep only those with step in Moore nbhd)
    clean = [pts[0]]
    for p in pts[1:]:
        if max(abs(p[0] - clean[-1][0]), abs(p[1] - clean[-1][1])) == 1:
            if len(clean) >= 2 and max(abs(p[0] - clean[-2][0]), abs(p[1] - clean[-2][1])) == 1:
                clean[-1] = p
            else:
                clean.append(p)
    H, W = T.shape
    for (y, x) in clean:
        T[y % H, x % W] = 3
    n = len(clean)
    for i in range(n):
        (y0, x0), (y1, x1) = clean[i], clean[(i + 1) % n]
        for d in range(8):
            if y0 + DY[d] == y1 and x0 + DX[d] == x1:
                B[y0 % H, x0 % W] |= np.uint8(1 << d)
                B[y1 % H, x1 % W] |= np.uint8(1 << ((d + 4) % 8))
    # clear inside of ring of substrate partially so there is room
    return T, B


def step(s):
    _sweep(s["T"], s["B"], P["p_move"], P["p_perm"], P["p_prod"], P["p_ext"], P["p_init"],
           P["p_join"], P["p_splice"], P["p_dis"], P["p_disf"], P["p_bb"], P["MIN_SEP"], P["inhibit"])
    s["t"] += 1
    return s


def fields(s):
    T, B = s["T"], s["B"]
    bonded = (T == 3) & (B != 0)
    return np.stack([(T == 1) * 0.35, (T == 2) * 1.0, ((T == 3) & ~bonded) * 1.0, bonded * 1.0]).astype(np.float32)


def matter(F):
    # an individual = membrane (bonded links) plus whatever it encloses
    from scipy import ndimage
    m = ndimage.gaussian_filter(F[3], 0.7, mode="wrap") > 0.15
    filled = ndimage.binary_fill_holes(m)
    return (filled.astype(np.float32) + F[3] + F[1]).astype(np.float32)


def damage(state, mask):
    """labkit centres its disk on the individual's centroid, which for a membrane-bounded cell
    hits only the interior. We keep the disk radius but move its centre onto the membrane
    along +x (fixed direction), then erase everything inside (cells -> holes, bonds cut)."""
    T, B = state["T"], state["B"]
    H, W = T.shape
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return state
    cy, cx = ys.mean(), xs.mean()
    r = np.sqrt(len(ys) / np.pi)
    row = int(round(cy)) % H
    bonded = (T[row] == 3) & (B[row] != 0)
    xb = [((x - cx) % W) for x in np.nonzero(bonded)[0] if ((x - cx) % W) < W / 2]
    off = max(xb) if xb else 2 * r
    ccx = cx + off
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - ccx + W / 2) % W - W / 2
    hole = dy ** 2 + dx ** 2 <= (1.3 * r) ** 2
    for y, x in zip(*np.nonzero(hole & (T == 3))):
        _clear_bonds(B, y, x, H, W)
    T[hole] = 0
    B[hole] = 0
    state["damage_erased"] = int(hole.sum())
    return state


def stats(s):
    T, B = s["T"], s["B"]
    bonded = (T == 3) & (B != 0)
    lab, n = ndimage_label(~bonded)
    sizes = np.bincount(lab.ravel())[1:]
    encl = int(sizes.sum() - sizes.max()) if n > 1 else 0  # area not connected to the big outside
    return {"K": int((T == 2).sum()), "Lfree": int(((T == 3) & ~bonded).sum()), "Lb": int(bonded.sum()),
            "encl": encl, "nencl": int(n - 1)}


def ndimage_label(m):
    from scipy import ndimage
    return ndimage.label(m)  # 4-connected background: 8-connected bonded chains close it
