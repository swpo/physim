"""operators_v3.py — v3 Track B spatial-merge operator (2026-08-31). NEW
module per relock protocol: does NOT edit ds2_ops.py / operators_lib.py /
any locked sim file.

merge_spatial_ic (the v3 bridge, V3_TRACKB_SPEC "SPATIAL MERGE"):
  offspring inherits ONE parent's chemistry (parent A, verbatim deepcopy);
  the IC is composed from BOTH parents' DEVELOPED states stamped into
  disjoint soft-masked regions (soft half-plane or disk seam). Populations
  meet in space; chemistry stays uniform -> no numerics change, the locked
  stepper runs the child exactly like any other genome.

Developed states: pass saved full-field snapshots (npz with F=(na+nc,N,N)
or an array) — else the operator RE-SIMS each parent's own soup IC for
T_DEV=300tu with the locked soup_sim_v2 (chunk-aligned) and uses that state.

Field mapping B -> A's field space (chemistry is A's):
  activators by index up to min(naA, naB): B's u_i pasted as DEVIATION from
  B's vacuum added onto A's vacuum (u_A0 + (u_B - u_B0)) — backgrounds stay
  consistent; A-only activators start at A's vacuum in the B region.
  channels by index up to min(ncA, ncB): channels are deviation fields
  (==0 at vacuum) and paste directly; A-only channels start at 0 there.

Assay-path hook (verified, see VALIDATION_V3.md): assay_v3.run_assay accepts
ic_override=(na+nc,N,N); it replaces S["F"] right after SS2.init_soup —
a data-level hook on the state dict, no locked-file edit. The deploy-pod
runtime (pod_lib.evaluate) calls assay_v2.run_assay which has NO such kwarg;
the pilot needs the one-line swap `import assay_v3 as assay_v2` (or an
ic_override passthrough) in pod_lib — documented, NOT applied here.
"""
import copy, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stage2", "lib"))
import genome as G
import soup_sim_v2 as SS2

T_DEV = 300.0        # parent development horizon when no snapshot given (tu)
SEAM_PX = 4.0        # soft-mask seam width (px)
DISK_R_FRAC = 0.30   # disk-mask radius as fraction of L


def develop_state(g, L=128.0, seed=1, T=T_DEV, workers=2, kicks=None):
    """Run the locked soup protocol for T tu; return (na+nc,N,N) float64
    state + status. T must be a multiple of CREC=25."""
    S = SS2.init_soup(g, L=L, seed=seed, workers=workers, kicks=kicks)
    status = SS2.advance(S, float(T))
    return np.asarray(S["F"], np.float64).copy(), status


def _load_state(snap, g, L, seed, workers):
    """snap: None -> develop; ndarray -> use; str -> npz with 'F' key."""
    if snap is None:
        F, status = develop_state(g, L=L, seed=seed, workers=workers)
        return F, f"dev_T{T_DEV:g}_{status}"
    if isinstance(snap, str):
        F = np.load(snap)["F"]
        return np.asarray(F, np.float64), f"npz:{os.path.basename(snap)}"
    return np.asarray(snap, np.float64), "array"


def soft_mask(N, dx, rng, geometry=None):
    """Soft [0,1] mask (1 = parent-A region), half of the box by area.
    geometry: 'half' (random-axis half-plane) or 'disk' (centered disk,
    radius DISK_R_FRAC*L, ~28% area — A keeps the majority outside? no:
    disk = A inside, B outside)."""
    geom = geometry or ("half" if rng.random() < 0.5 else "disk")
    L = N * dx
    c = (np.arange(N) + 0.5) * dx
    w = SEAM_PX
    if geom == "half":
        ax = int(rng.integers(0, 2))
        x0 = rng.uniform(0.0, L)
        # periodic-safe soft band [x0, x0+L/2): distance from band CENTER
        # via min-image; prof = 1 inside, 0 outside, tanh seams at edges
        dctr = np.abs(G.min_image(c - (x0 + 0.25 * L), L))
        prof = 0.5 * (1.0 - np.tanh((dctr - 0.25 * L) / w))
        m = prof[:, None] * np.ones(N)[None, :] if ax == 0 \
            else np.ones(N)[:, None] * prof[None, :]
    else:
        cy, cx = rng.uniform(0, L, 2)
        R = DISK_R_FRAC * L
        dy = G.min_image(c - cy, L)[:, None]
        dxx = G.min_image(c - cx, L)[None, :]
        r = np.hypot(dy, dxx)
        m = 0.5 * (1.0 - np.tanh((r - R) / w))
    return m, geom


def merge_spatial_ic(gA, gB, snapA=None, snapB=None, rng=None, L=128.0,
                     seed=1, workers=2, geometry=None):
    """Compose the spatial-merge child.
    Returns (child_genome, ic_override, info). child = deepcopy(gA) with a
    fresh provenance note; ic_override = (naA+ncA, N, N) float64."""
    rng = rng or np.random.default_rng()
    gA = copy.deepcopy(gA)
    gB = copy.deepcopy(gB)
    dx = 0.5
    N = int(round(L / dx))
    FA, srcA = _load_state(snapA, gA, L, seed, workers)
    FB, srcB = _load_state(snapB, gB, L, seed + 1, workers)
    naA, ncA = len(gA["acts"]), len(gA["chans"])
    naB, ncB = len(gB["acts"]), len(gB["chans"])
    assert FA.shape == (naA + ncA, N, N), (FA.shape, naA + ncA, N)
    assert FB.shape[1:] == (N, N), FB.shape
    m, geom = soft_mask(N, dx, rng, geometry=geometry)
    ic = np.empty((naA + ncA, N, N))
    u0A = [a["u0"] for a in gA["acts"]]
    u0B = [a["u0"] for a in gB["acts"]]
    for i in range(naA):
        insideA = FA[i]
        if i < naB:
            outsideB = u0A[i] + (FB[i] - u0B[i])   # deviation paste
        else:
            outsideB = np.full((N, N), u0A[i])     # A-only act: vacuum
        ic[i] = m * insideA + (1.0 - m) * outsideB
    for c in range(ncA):
        insideA = FA[naA + c]
        if c < ncB:
            outsideB = FB[naB + c]                 # channels are deviations
        else:
            outsideB = np.zeros((N, N))
        ic[naA + c] = m * insideA + (1.0 - m) * outsideB
    child = gA
    idA, idB = gA.get("id", "A"), gB.get("id", "B")
    child["id"] = f"{idA}_x_{idB}_sic"
    prov = dict(child.get("provenance") or {})
    prov["merge_spatial_ic"] = dict(
        parents=[idA, idB], geometry=geom,
        srcA=srcA, srcB=srcB, L=L, seed=seed,
        map=dict(acts=min(naA, naB), chans=min(ncA, ncB)))
    child["provenance"] = prov
    info = dict(op="merge_spatial_ic", geometry=geom, srcA=srcA, srcB=srcB,
                mask_share_A=round(float(m.mean()), 3))
    return child, ic, info
