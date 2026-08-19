# M5 MACHINE — first blob machine: net UPSTREAM cargo transport (SUMMARY)

**Verdict: B6 PASS — "RELAY TUG" machine certified. 3/3 cycles (pickups), net
upstream cargo displacement 756-766 px (gate: 30), efficiency 5.6-5.7x the
do-nothing baseline, in ALL of 3 noise seeds + 1 jitter draw + film run; paired
no-locomotive NULL clean. B1 PASS (all 6 structures alive & compact at every
record, 3600 tu, sigma=2e-3). B7 PASS with documented one-off exceptions.
Grid-check one-off: per-blob net_x dx=0.25 vs dx=0.5 within 0.5-2.4%.**

## World decision (round-3 integration question, resolved first)
Machine world = **single-species (u,v,w) A=4 family** (M4's certified traveling-
bond world), NOT the vvw two-species world:
1. The motor is the wake-locked tandem/train — certified in single-species M4.
   In vvw NO binding exists (all pairs repel; M3 encounter table, transport P3):
   porting the motor would be a fresh physics campaign, not an integration step.
2. The isod gradient ports EXACTLY to single-species as **"isok" mode**:
   k1 -> k1 + u0*b(x), k4 -> k4 + b(x) with u0=-0.70354 (uniform state).
   u0 stays an EXACT root of the driven cubic for all b; reaction perturbation
   = b*(u0-w) vanishes identically on the background. C1 control: no-blob saw
   world flat to 1.1e-16. Zero-footprint force field, same class as transport's
   isod (force<->stability decoupled by construction).
3. Cargo = same species as carrier: **flavor is not needed for machine v1** —
   machine function (transport against a load) never invokes species identity;
   cargo identity is positional, measured by tracking. Cost: no species-
   selective sorting in v1 (vvw B-B binding = open item).

## The machine (v2, certified)
World: A=4 family at tau=5.70 (pair-only drift zone), IMEX-FFT dx=0.5 dt=0.02,
L=160 periodic, noise sigma=2e-3 (M4 cert convention).
Environment (static, no per-blob terms, honesty rules):
  b(x,y) = saw(x; eps=5e-4, P=32, frac=0.85, 5 teeth) + 0.002*min(|y-80|, 24)
  applied in isok mode. Saw span +-0.0068 (k4-units); the y-term = channel RAILS.
IC: A=4 stamp (composite/data reused). Locomotive = 3-train at x=2,17,32
(y=80), each blob kicked +x (kick_d=0.5, IC-only). Cargo = 3 unkicked blobs
parked at trough-settle points x=66.3/98.3/130.3 (E5-measured rest position).
DOWNSTREAM = -x (C4/E5: lone blob slides down-b and parks at trough).
UPSTREAM = +x = against the saw teeth, over cliffs.

Function (all runs identical to 0.4% in net_up): the self-propelled 3-train
climbs its tooth, crosses the cliff, reaches cargo 1 head-on -> cargo wake-locks
at the first shell (gap 14.4-15.4 px) as the NEW LEADER (pusher-tug) -> 4-train
(faster: M4 train-length law) -> picks up cargo 2 -> 5-train -> cargo 3 ->
6-train at c~0.085. Around t~1150 the 6-train sheds its rearmost loco blob
(near-onset power ceiling: 6 > max sustainable length uphill); the shed blob
slides back to a trough, WAITS (pair-only zone: lone blob immobile), and is
RE-COLLECTED next lap (t~1750) — a self-healing relay. All 6 blobs end in
2 trains (5+1 re-locking or 6), circulating upstream indefinitely.

## Certification battery (locked metrics.py BEFORE runs; 1 documented amendment
before any cert run: v_drift = moving-segment fit, because the lone blob PARKS
at the trough and a whole-track fit would understate the adversary)
- Cycles = pickups (locked): cargo advances >=2 px upstream AND sustains
  >= 5e-3 px/tu over the next 100 tu; complete if carried >=10 px and
  train-bound at end (nearest-neighbor in shell band 12-32 px).
- seed1/2/3 (sigma=2e-3): pickups at t=245/515/765 (+-5 tu across seeds!),
  net_up = 758.98 / 757.39 / 756.19 px, efficiency 5.62/5.61/5.60.
- jitter draw (park positions +U(-2,2) px, seed 4): pickups 255/540/785,
  net_up 766.35, eff 5.68. film seed5: 765.99, eff 5.67.
- Efficiency metric (controller-fixed): net_up / (|v_drift|*T*n_cargo);
  |v_drift| = 0.0125 px/tu (E5 moving-segment on the working track),
  baseline loss = 0.0125*3600*3 = 135 px. Ratio 5.6-5.7.
  (Honest note: the trough BOUNDS the do-nothing loss at ~12 px/cargo — the
  drift-rate baseline is the stronger reading of "what the field does to cargo";
  vs the bounded park-displacement the machine moves cargo ~250x further UP.)
- NULL (no locomotive, same track/noise): all 3 cargoes stay parked,
  dx = -0.55/-0.54/-0.67 px. null_ok.
- B1: ncomp==6 at every record post-transient in all 5 machine runs; areas
  31.5-33 px^2 throughout; no split/merge/death ever.
- Grid check one-off (T=700 noiseless segment): per-id net_x at dx=0.25 vs 0.5
  within 0.5-2.4% (cargo3 still parked in both: |dx|<0.4px), cargo-1 pickup time
  245 vs 240 tu, lead speed diff 0.6%. (First attempt was invalid — stamp wasn't
  resampled to dx; engine patched pre-rerun, documented in results.json.)

## Control ladder (all in results.json; the physics that set the design)
- C0/C2 anchors: M4 values reproduced (pair tau=6: c=0.1408 @T=600-window 0.139;
  tau=5.7: single decays to rest, pair c=0.0592 sep 15.23 = M4 audit).
- C3 c_pair(b) at tau=5.7: +0.094/-0.05, +0.085/-0.025, +0.059/0, +0.004/+0.025,
  0/+0.05 => quasi-static stall b* in (0.025,0.05); pair REPLICATES at b=-0.10;
  singles static (areas 46->25) for b in [-0.15,+0.2].
- C4 adversary: near-onset UNLEASHING, not vvw's linear law: parked lone blob on
  a slope runs DOWN-B at 0.05-0.08 px/tu (comparable to c_pair!), then parks at
  the trough. Down-running blob replicates if trough deeper than b ~ -0.09
  (=> saw span must stay well inside +-0.09; ours: +-0.0068).
- C5/C7 HONEST NEGATIVE: a PAIR cannot climb any tested saw at tau=5.7 (dynamic
  reversal at b_rev ~ 0.000 (eps=5e-4) / +0.005 (eps=2.5e-4)); apex-parked cargo
  falls down the cliff (apexes are not park spots).
- E-series climbing envelope: b_rev grows with train length: pair ~0/+0.005,
  3-TRAIN +0.0104 => locomotive must be a 3-train; tooth apex +0.0068 = 1.53x
  margin. E4: 3-train laps the machine tooth (+173 px / 2500 tu, ~6 cliffs).
- C6/P1 pickup primitive: PASS flat & on-track (approach -> overshoot to ~14.1
  -> lock at 14.95 as new leader; 3-train c=0.073 = +23% vs pair). t_pu=215-270.
- MC v1 (no rails) FAILED under noise — buckling: train turns off-axis into the
  trough VALLEY (y costs nothing), jams after 1-2 pickups (net_up 30/60/31 px,
  seeds). Fix = rails: R0 restore (y=86->80, damped), R1/R2 train on-axis
  (|dy|<0.6px) with climb intact (0.068/0.076 — faster than unrailed).
  v2 = v1 + channel. This is the honest cost of "machine": 2 static environment
  ingredients (saw + rails), both zero-footprint-class, no scripting.

## Files
sim.py (A=4 isok engine: saw+channel b(x,y), stamp paste incl. dx-resample,
persistent greedy tracking, fcntl results IO) · metrics.py (LOCKED pre-cert;
1 documented pre-cert amendment) · runjob.py/drive.py (job runner, quick
metrics) · results.json (71 records, append-only) · data/*.npz (tracks+snaps)
· strips/fig1 (pilot), fig2 (pilot film), fig3 (cert battery), fig4 (cert film)
· jobs_*.json (exact specs) · NOTES.md (working log).

## Budget (B7)
Controls at L=96-160 dx=0.5: 50-200 s => PASS. Machine cert runs (N=320, T=3600,
noise): 660-690 s each — documented one-offs (5 runs). dx=0.25 grid check 385 s.
Rates: 19-25 tu/s (L=96), 8.5 (L=160), 5.4 (L=160+noise), 1.8 (dx=0.25).
