"""SCL-divide: lattice SCL plus membrane mechanics that allow growth and fission.

New operators relative to scl_lattice (the parent):
  pore block   K cannot step into a site touching >= 2 chain ends (a gap in the membrane).
  fluctuation  a bonded link may hop into a neighbouring hole if all its bonds stay valid
               (bond-fluctuation polymer move): the membrane is flexible, and it can only
               move into holes, so a crowded interior pushes it outward (osmotic swelling).
  insertion    a free link touching both ends of a bond A-B replaces it by A-L-B (growth).
  reconnection two antiparallel membrane segments A-A', B-B' that touch (A~B, A'~B') rewire to
               A-B, A'-B': one loop pinches into two (fission), two loops fuse into one.
  K replication  K + adjacent free L -> 2 K (p_krep); K -> S decay (p_kdec).

Original header follows.
Lattice SCL (substrate-catalyst-link) autopoiesis, after Varela, Maturana & Uribe (1974)
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
    "name": "scl-divide",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/scl_lattice",
    "mutation": "flexible membrane (bond-fluctuation moves), link insertion, segment reconnection (fission/fusion), K pore block, K replication",
    "size": (64, 64),
    "steps_per_frame": 10,
    "dt": 1.0,
    "channels": ["S", "K", "L free", "L bonded"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(p_move=1.0, p_perm=0.5, p_prod=0.05, p_ext=0.05, p_init=0.002, p_join=0.9, p_splice=1.0, p_dis=0.0005, p_disf=0.0005, p_bb=0.0,
         MIN_SEP=2, p_flu=0.5, p_ins=0.2, p_rec=0.5, p_krep=0.0, p_kdec=0.0, pore=1, swapS=1, minloop=16, s_density=0.7, n_cat=1, ring_r=9, IC="cell")

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
def _dir_to(y0, x0, y1, x1, H, W):
    for e in range(8):
        if (y0 + DY[e]) % H == y1 and (x0 + DX[e]) % W == x1:
            return e
    return -1


@nb.njit(cache=True)
def _n_ends(T, B, y, x, H, W):
    n = 0
    for d in range(8):
        ny, nx = _nb(y, x, d, H, W)
        if T[ny, nx] == 3 and _nbonds(B[ny, nx]) == 1:
            n += 1
    return n


@nb.njit(cache=True)
def _bonds_valid(T, B, y, x, H, W, min_sep):
    # check angle at (y,x), angle at each partner, no crossings, for all bonds of (y,x)
    b = B[y, x]
    for d in range(8):
        if (b >> d) & 1:
            ny, nx = _nb(y, x, d, H, W)
            if T[ny, nx] != 3:
                return False
            if _crosses(B, y, x, d, H, W):
                return False
            pb = B[ny, nx]
            back = (d + 4) % 8
            for e in range(8):
                if e != back and (pb >> e) & 1:
                    s = abs(e - back)
                    s = min(s, 8 - s)
                    if s < min_sep:
                        return False
            for e in range(8):
                if e != d and (b >> e) & 1:
                    s = abs(e - d)
                    s = min(s, 8 - s)
                    if s < min_sep:
                        return False
    return True


@nb.njit(cache=True)
def _fluctuate(T, B, y, x, H, W, min_sep, swapS):
    """bonded link hops to a von Neumann neighbour hole, keeping all partners Moore-adjacent."""
    d = 2 * np.random.randint(4)
    ty, tx = _nb(y, x, d, H, W)
    u = T[ty, tx]
    if u != 0 and not (u == 1 and swapS):
        return
    b = B[y, x]
    py = np.empty(2, np.int64)
    px = np.empty(2, np.int64)
    m = 0
    for e in range(8):
        if (b >> e) & 1:
            py[m], px[m] = _nb(y, x, e, H, W)
            m += 1
    nd = np.empty(2, np.int64)
    for i in range(m):
        nd[i] = _dir_to(ty, tx, py[i], px[i], H, W)
        if nd[i] < 0:
            return
    # move
    _clear_bonds(B, y, x, H, W)
    T[ty, tx] = 3
    T[y, x] = u
    for i in range(m):
        B[ty, tx] |= np.uint8(1 << nd[i])
        B[py[i], px[i]] |= np.uint8(1 << ((nd[i] + 4) % 8))
    if not _bonds_valid(T, B, ty, tx, H, W, min_sep):
        # revert
        _clear_bonds(B, ty, tx, H, W)
        T[y, x] = 3
        T[ty, tx] = u
        for i in range(m):
            e = _dir_to(y, x, py[i], px[i], H, W)
            B[y, x] |= np.uint8(1 << e)
            B[py[i], px[i]] |= np.uint8(1 << ((e + 4) % 8))


@nb.njit(cache=True)
def _insert(T, B, y, x, H, W, p_ins, min_sep):
    """free link at (y,x) touching both ends of a bond A-B: A-B -> A-L-B."""
    if np.random.random() >= p_ins:
        return
    d = np.random.randint(8)
    ay, ax = _nb(y, x, d, H, W)
    if T[ay, ax] != 3:
        return
    ba = B[ay, ax]
    for e in range(8):
        if (ba >> e) & 1:
            by, bx = _nb(ay, ax, e, H, W)
            d2 = _dir_to(y, x, by, bx, H, W)
            if d2 < 0 or d2 == d:
                continue
            # rewire
            B[ay, ax] &= ~np.uint8(1 << e)
            B[by, bx] &= ~np.uint8(1 << ((e + 4) % 8))
            B[y, x] = np.uint8((1 << d) | (1 << d2))
            B[ay, ax] |= np.uint8(1 << ((d + 4) % 8))
            B[by, bx] |= np.uint8(1 << ((d2 + 4) % 8))
            if _bonds_valid(T, B, y, x, H, W, min_sep):
                return
            # revert
            B[ay, ax] &= ~np.uint8(1 << ((d + 4) % 8))
            B[by, bx] &= ~np.uint8(1 << ((d2 + 4) % 8))
            B[y, x] = 0
            B[ay, ax] |= np.uint8(1 << e)
            B[by, bx] |= np.uint8(1 << ((e + 4) % 8))
            return


@nb.njit(cache=True)
def _chain_dist(B, y0, x0, y1, x1, nmax, H, W):
    """walk the chain from (y0,x0) in both directions up to nmax steps; return steps to (y1,x1) or -1"""
    for first in range(8):
        if not (B[y0, x0] >> first) & 1:
            continue
        py, px = y0, x0
        cy, cx = _nb(y0, x0, first, H, W)
        for k in range(1, nmax + 1):
            if cy == y1 and cx == x1:
                return k
            if cy == y0 and cx == x0:
                break
            moved = False
            for e in range(8):
                if (B[cy, cx] >> e) & 1:
                    ny, nx = _nb(cy, cx, e, H, W)
                    if not (ny == py and nx == px):
                        py, px, cy, cx = cy, cx, ny, nx
                        moved = True
                        break
            if not moved:
                break
    return -1


@nb.njit(cache=True)
def _reconnect(T, B, y, x, H, W, min_sep, minloop):
    """A=(y,x) bonded to A'; neighbour B (not bonded to A) bonded to B' with A'~B'.
    Rewire A-A', B-B' -> A-B, A'-B'."""
    d = np.random.randint(8)
    by, bx = _nb(y, x, d, H, W)
    if T[by, bx] != 3 or (B[y, x] >> d) & 1 or _nbonds(B[by, bx]) != 2 or _nbonds(B[y, x]) != 2:
        return
    if _chain_dist(B, y, x, by, bx, minloop, H, W) >= 0:
        return  # would pinch off a loop smaller than minloop links
    ba, bb = B[y, x], B[by, bx]
    for e in range(8):
        if not (ba >> e) & 1:
            continue
        a2y, a2x = _nb(y, x, e, H, W)
        for f in range(8):
            if not (bb >> f) & 1:
                continue
            b2y, b2x = _nb(by, bx, f, H, W)
            if (b2y == y and b2x == x) or (a2y == by and a2x == bx) or (a2y == b2y and a2x == b2x):
                continue
            g = _dir_to(a2y, a2x, b2y, b2x, H, W)
            if g < 0 or (B[a2y, a2x] >> g) & 1:
                continue
            # rewire
            B[y, x] &= ~np.uint8(1 << e); B[a2y, a2x] &= ~np.uint8(1 << ((e + 4) % 8))
            B[by, bx] &= ~np.uint8(1 << f); B[b2y, b2x] &= ~np.uint8(1 << ((f + 4) % 8))
            B[y, x] |= np.uint8(1 << d); B[by, bx] |= np.uint8(1 << ((d + 4) % 8))
            B[a2y, a2x] |= np.uint8(1 << g); B[b2y, b2x] |= np.uint8(1 << ((g + 4) % 8))
            if _bonds_valid(T, B, y, x, H, W, min_sep) and _bonds_valid(T, B, a2y, a2x, H, W, min_sep):
                return
            B[y, x] &= ~np.uint8(1 << d); B[by, bx] &= ~np.uint8(1 << ((d + 4) % 8))
            B[a2y, a2x] &= ~np.uint8(1 << g); B[b2y, b2x] &= ~np.uint8(1 << ((g + 4) % 8))
            B[y, x] |= np.uint8(1 << e); B[a2y, a2x] |= np.uint8(1 << ((e + 4) % 8))
            B[by, bx] |= np.uint8(1 << f); B[b2y, b2x] |= np.uint8(1 << ((f + 4) % 8))
            return


@nb.njit(cache=True)
def _sweep(T, B, p_move, p_perm, p_prod, p_ext, p_init, p_join, p_splice, p_dis, p_disf, p_bb, min_sep, p_flu, p_ins, p_rec, p_krep, p_kdec, pore, swapS, minloop):
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
            if B[y, x] == 0 or np.random.random() < 0.5:
                d = np.random.randint(8)
                _try_bond(T, B, y, x, d, H, W, p_ext, p_init, p_join, min_sep)
            if B[y, x] == 0 and p_ins > 0:
                _insert(T, B, y, x, H, W, p_ins, min_sep)
            if B[y, x] != 0:
                if p_rec > 0 and np.random.random() < p_rec:
                    _reconnect(T, B, y, x, H, W, min_sep, minloop)
                if _nbonds(B[y, x]) == 2 and np.random.random() < p_flu:
                    _fluctuate(T, B, y, x, H, W, min_sep, swapS)
                continue  # bonded links move only by fluctuation
        if t == 2:
            if p_kdec > 0 and np.random.random() < p_kdec:
                T[y, x] = 1
                continue
            if p_krep > 0 and np.random.random() < p_krep:
                d = np.random.randint(8)
                ny, nx = _nb(y, x, d, H, W)
                if T[ny, nx] == 3 and B[ny, nx] == 0:
                    T[ny, nx] = 2
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
            if t == 2 and pore and _n_ends(T, B, ny, nx, H, W) >= 2:
                pass
            elif u == 0:
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
           P["p_join"], P["p_splice"], P["p_dis"], P["p_disf"], P["p_bb"], P["MIN_SEP"],
           P["p_flu"], P["p_ins"], P["p_rec"], P["p_krep"], P["p_kdec"], P["pore"], P["swapS"], P["minloop"])
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
