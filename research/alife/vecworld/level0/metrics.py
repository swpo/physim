"""Cheap level-0 screens: periodic connected components of A_sum above a density threshold,
overlap-based tracking with merge / split events, contacts, speeds, occupancy."""
import numpy as np
import scipy.ndimage as ndi

S8 = np.ones((3, 3), bool)


def periodic_label(mask):
    """8-connected labels on the torus. Returns (lab, n) with labels 1..n."""
    lab, n = ndi.label(mask, structure=S8)
    if n == 0:
        return lab, 0
    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    H, W = mask.shape
    pairs = []
    # rows 0 / H-1 (with diagonal neighbours), columns 0 / W-1
    for d in (-1, 0, 1):
        a, b = lab[0], np.roll(lab[-1], d)
        pairs.append(np.stack([a, b], 1))
        a, b = lab[:, 0], np.roll(lab[:, -1], d)
        pairs.append(np.stack([a, b], 1))
    pairs = np.concatenate(pairs)
    pairs = pairs[(pairs[:, 0] > 0) & (pairs[:, 1] > 0)]
    for a, b in np.unique(pairs, axis=0):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(i) for i in range(n + 1)])
    uniq, newid = np.unique(roots, return_inverse=True)
    # label 0 maps to 0 because root(0) = 0 is the smallest
    return newid[lab], len(uniq) - 1


def components(Asum, thr, m_min, B=None):
    """Bodies: periodic components of B > thr (B = Asum, or a blurred Asum so that a body with
    holes or dotted parts is one component) with mass >= m_min (mass and centroid from Asum).
    Returns lab (0 = none, 1..n) and a list of dicts (mass, area, cy, cx, rg)."""
    H, W = Asum.shape
    lab, n = periodic_label((Asum if B is None else B) > thr)
    if n == 0:
        return lab, []
    L = lab.ravel()
    a = Asum.ravel()
    bc = lambda w: np.bincount(L, w, minlength=n + 1)[1:]
    mass = bc(a)
    area = np.bincount(L, minlength=n + 1)[1:].astype(float)
    yy, xx = np.mgrid[0:H, 0:W]
    # periodic mass-weighted centroid via circular means
    ty, tx = (2 * np.pi * yy / H).ravel(), (2 * np.pi * xx / W).ravel()
    cy = np.arctan2(bc(a * np.sin(ty)), bc(a * np.cos(ty))) * H / (2 * np.pi) % H
    cx = np.arctan2(bc(a * np.sin(tx)), bc(a * np.cos(tx))) * W / (2 * np.pi) % W
    keep = mass >= m_min
    out, relab = [], np.zeros(n + 1, int)
    j = 0
    for i in range(n):
        if not keep[i]:
            continue
        j += 1
        relab[i + 1] = j
        out.append({"mass": float(mass[i]), "area": float(area[i]), "cy": float(cy[i]), "cx": float(cx[i])})
    lab = relab[lab]
    # radius of gyration (periodic, around centroid)
    for i, c in enumerate(out):
        m = lab == i + 1
        dy = (yy[m] - c["cy"] + H / 2) % H - H / 2
        dx = (xx[m] - c["cx"] + W / 2) % W - W / 2
        w = Asum[m]
        c["rg"] = float(np.sqrt((w * (dy ** 2 + dx ** 2)).sum() / w.sum()))
    return lab, out


def pdist(a, b, H, W):
    dy = (a[0] - b[0] + H / 2) % H - H / 2
    dx = (a[1] - b[1] + W / 2) % W - W / 2
    return float(np.hypot(dy, dx))


class Tracker:
    """Overlap tracking between successive snapshots. Merge: >= 2 previous bodies overlap one
    current body (the most massive parent keeps its id). Split: one previous body overlaps >= 2
    current bodies (the most massive child keeps the id, the others are born by split)."""

    def __init__(self, shape, thr, m_min, contact_px=2, blur=0.0):
        self.H, self.W = shape
        self.thr, self.m_min, self.blur = thr, m_min, blur
        self.contact_px = contact_px
        self.prev_lab, self.prev = None, None
        self.next_id = 0
        self.tracks = {}       # id -> dict(t0, t1, path [(t, cy, cx, mass, area)], start, end)
        self.events = []       # (t, kind, ids)
        self.series = []       # per snapshot summary
        self.contact_pairs = set()
        self.contact_events = 0

    def _new(self, t, c, how):
        i = self.next_id
        self.next_id += 1
        self.tracks[i] = {"t0": t, "t1": t, "start": how, "end": None,
                          "path": [(t, c["cy"], c["cx"], c["mass"], c["area"], c["rg"])]}
        return i

    def update(self, t, A):
        Asum = A.sum(0)
        H, W = self.H, self.W
        B = ndi.gaussian_filter(Asum, self.blur, mode="wrap") if self.blur > 0 else None
        lab, comps = components(Asum, self.thr, self.m_min, B)
        occ = float(((Asum if B is None else B) > self.thr).mean())
        ids = [None] * len(comps)
        n_merge = n_split = 0
        if self.prev is None:
            for j, c in enumerate(comps):
                ids[j] = self._new(t, c, "initial")
        else:
            P, Q = len(self.prev), len(comps)
            ov = np.zeros((P + 1, Q + 1), int)
            if P and Q:
                np.add.at(ov, (self.prev_lab.ravel(), lab.ravel()), 1)
            ov = ov[1:, 1:]
            E = ov > 0
            # fallback for fast small bodies: no overlap -> nearest previous body within 2 rg + 3
            for j in range(Q):
                if not E[:, j].any() and P:
                    d = [pdist((comps[j]["cy"], comps[j]["cx"]), (p["cy"], p["cx"]), H, W) for p in self.prev]
                    i = int(np.argmin(d))
                    if d[i] < 2 * self.prev[i]["rg"] + 3 and not E[i].any():
                        E[i, j] = True
            pid = self.prev_ids
            claimed = {}
            for j in range(Q):
                parents = np.nonzero(E[:, j])[0]
                if len(parents) == 0:
                    ids[j] = self._new(t, comps[j], "appear")
                    continue
                if len(parents) >= 2:
                    n_merge += 1
                    self.events.append((t, "merge", [int(pid[i]) for i in parents]))
                heir = parents[np.argmax([self.prev[i]["mass"] for i in parents])]
                claimed.setdefault(int(heir), []).append(j)
            for i in range(P):
                kids = np.nonzero(E[i])[0]
                tr = self.tracks[pid[i]]
                if len(kids) >= 2:
                    n_split += 1
                    self.events.append((t, "split", [int(pid[i])]))
                js = claimed.get(i)
                if js:
                    # continues into its most massive claimed child; the others are born by split
                    js = sorted(js, key=lambda j: -comps[j]["mass"])
                    ids[js[0]] = pid[i]
                    c = comps[js[0]]
                    tr["t1"] = t
                    tr["path"].append((t, c["cy"], c["cx"], c["mass"], c["area"], c["rg"]))
                    for j in js[1:]:
                        ids[j] = self._new(t, comps[j], "split")
                else:
                    tr["end"] = "merged" if len(kids) else "vanish"
        # contacts: bodies whose masks come within contact_px of each other
        n_contact = 0
        if len(comps) >= 2:
            dil = ndi.grey_dilation(lab, footprint=np.ones((2 * self.contact_px + 1,) * 2, bool), mode="wrap")
            m = (dil > 0) & (lab > 0) & (dil != lab)
            pairs = set()
            for a, b in zip(lab[m], dil[m]):
                pairs.add((min(ids[a - 1], ids[b - 1]), max(ids[a - 1], ids[b - 1])))
            new = pairs - self.contact_pairs
            self.contact_events += len(new)
            self.contact_pairs = pairs
            n_contact = len(pairs)
        else:
            self.contact_pairs = set()
        self.series.append({"t": t, "n": len(comps), "occ": occ, "merge": n_merge, "split": n_split,
                            "contacts": n_contact,
                            "mass_in_bodies": float(sum(c["mass"] for c in comps)),
                            "max_body_frac": float(max([c["mass"] for c in comps], default=0) / max(Asum.sum(), 1e-12))})
        self.prev_lab, self.prev, self.prev_ids = lab, comps, ids
        return lab, comps, ids

    def summary(self, T_total):
        H, W = self.H, self.W
        ser = self.series
        n = np.array([s["n"] for s in ser])
        occ = np.array([s["occ"] for s in ser])
        half = len(ser) // 2
        trk = []
        for i, tr in self.tracks.items():
            path = tr["path"]
            life = tr["t1"] - tr["t0"]
            # path length on a 10-snapshot stride (suppresses centroid jitter of static bodies),
            # skipping strides in which the body's mass jumped by > 30% (a fusion or fission moves
            # the centroid without motion); net displacement from the unwrapped trajectory
            P = np.array([q[1:4] for q in path]) if len(path) else np.zeros((0, 3))
            if len(P) > 1:
                d = P[1:, :2] - P[:-1, :2]
                d[:, 0] = (d[:, 0] + H / 2) % H - H / 2
                d[:, 1] = (d[:, 1] + W / 2) % W - W / 2
                jump = np.maximum(P[1:, 2], P[:-1, 2]) / np.maximum(np.minimum(P[1:, 2], P[:-1, 2]), 1e-9) > 1.3
                d[jump] = 0.0
                U = np.vstack([[0.0, 0.0], np.cumsum(d, 0)])
                sub = U[::10] if (len(U) - 1) % 10 == 0 else np.vstack([U[::10], U[-1:]])
                dist = float(np.hypot(*np.diff(sub, axis=0).T).sum())
                net = float(np.hypot(*(U[-1] - U[0])))
            else:
                dist = net = 0.0
            size = float(np.median([2 * max(p[5], 1.0) for p in path]))
            trk.append({"id": i, "life": life, "dist": dist, "speed": dist / life if life > 0 else 0.0,
                        "body_len": size, "lengths_travelled": dist / size, "net_lengths": net / size,
                        "mass": float(np.median([p[3] for p in path])), "start": tr["start"], "end": tr["end"]})
        long = [x for x in trk if x["life"] >= 0.25 * T_total]
        ev_m = sum(s["merge"] for s in ser)
        ev_s = sum(s["split"] for s in ser)
        return {
            "n_bodies_median_2nd_half": float(np.median(n[half:])) if len(n) else 0.0,
            "n_bodies_final": int(n[-1]) if len(n) else 0,
            "n_bodies_min_2nd_half": int(n[half:].min()) if len(n) else 0,
            "occupancy_median_2nd_half": float(np.median(occ[half:])) if len(occ) else 0.0,
            "occupancy_max": float(occ.max()) if len(occ) else 0.0,
            "max_body_frac_final": ser[-1]["max_body_frac"] if ser else 0.0,
            "n_tracks": len(trk),
            "n_long_tracks": len(long),
            "long_track_median_life": float(np.median([x["life"] for x in long])) if long else 0.0,
            "long_track_median_speed": float(np.median([x["speed"] for x in long])) if long else 0.0,
            "long_track_median_lengths": float(np.median([x["lengths_travelled"] for x in long])) if long else 0.0,
            "long_track_median_net_lengths": float(np.median([x["net_lengths"] for x in long])) if long else 0.0,
            "long_track_frac_moving3": float(np.mean([x["lengths_travelled"] >= 3 for x in long])) if long else 0.0,
            "long_track_median_body_len": float(np.median([x["body_len"] for x in long])) if long else 0.0,
            "merges": int(ev_m), "splits": int(ev_s), "contact_events": int(self.contact_events),
            "contacts_per_body_mean": float(np.mean([s["contacts"] / max(s["n"], 1) for s in ser])) if ser else 0.0,
            "tracks": trk,
        }


def score(s):
    """Screening score in [0, 1]: several bodies, persistent, moving, interacting, bounded."""
    nb = s["n_bodies_median_2nd_half"]
    f_n = min(1.0, max(0.0, (nb - 1.5) / 2.5)) * (1.0 if nb <= 40 else 40.0 / nb)
    f_occ = 1.0 if s["occupancy_median_2nd_half"] < 0.35 else max(0.0, 1 - (s["occupancy_median_2nd_half"] - 0.35) / 0.25)
    f_persist = min(1.0, s["n_long_tracks"] / 3.0)
    f_move = min(1.0, s["long_track_median_lengths"] / 4.0) * min(1.0, s["long_track_frac_moving3"] / 0.5 + 0.2)
    inter = s["merges"] + s["splits"] + s["contact_events"]
    f_int = min(1.0, inter / 6.0)
    # penalise collapse into one dominant body
    f_dom = 1.0 if s["max_body_frac_final"] < 0.6 else max(0.0, (0.9 - s["max_body_frac_final"]) / 0.3)
    return float(f_n * f_occ * f_persist * f_move * (0.3 + 0.7 * f_int) * f_dom)
