"""metrics.py — GENESIS (phase-3 L2->L1 reduction) LOCKED metric definitions.
Written BEFORE any certification battery (2026-02-19). Amendments must be dated.

Context anchors (imported facts):
  - machine/E5: hand-built saw (eps=5e-4, P=32, frac=0.85) moves a parked tau=5.7
    lone blob at v_drift = 0.0125 px/tu (moving-segment fit) to the trough; park
    displacement bounded ~12px by trough spacing.
  - tau=5.7 is the PAIR-ONLY zone: a lone blob on FLAT b is provably immobile
    (M4/M5); therefore ANY sustained directed drift of a lone parked blob = track
    function of the landscape under test.
  - bfield teaser T5: self-written standing saw, fresh edge b=-0.00378, lap decay
    0.49, e-fold ell = c*tau_b = 125px.

MEASURES
  v_slide: on the approach segment (records before parking), directed speed toward
    the b-minimum = median of d(x_along)/dt over records where |d/dt| > 1e-3 px/tu;
    if never above 1e-3, v_slide = net_along/T (reported, likely ~0).
  park_pos: mean unwrapped position over the last 300 tu.
  park_speed: |linear-fit velocity| over the last 300 tu.
  trough_dist: min-image distance from park_pos to the frozen-landscape b-minimum
    location (computed from the frozen b field along the track line).

GATES (task 1 — functional sawtooth, frozen self-written landscape)
  G-SLIDE  PASS: net displacement toward the b-minimum >= 2 px AND mean directed
           speed over the slide >= 1.5e-3 px/tu (>=10x measurement floor).
  G-PARK   PASS: park_speed <= 1e-3 px/tu sustained over final 300 tu AND
           trough_dist <= 3 px AND blob alive with ncomp==1 throughout.
  G-BRAKE  PASS: with sigma=2e-3, a blob parked at the trough stays within 3 px
           of it for >= 1000 tu (net |drift| < 3 px).
  Fidelity numbers reported (no gate): tooth height ratio h_self/h_hand with
    h_hand = 0.0136 (machine saw full span 2*0.0068); slope ratio; v ratio
    v_self/0.0125; susceptibility chi = v_slide/|local slope| both worlds.

GATES (task 2 — self-dug racetrack)
  G-RING   PASS (write phase): after T_write, azimuthally-averaged b along the
           orbit circle shows a closed ring: min over angles of |b_ring(theta)| >=
           0.25 * max over angles (no gap), depth |b|_ring_mean >= 1e-3.
  G-ORBIT  PASS (frozen ring, anchor REMOVED, fresh tau=6.0 blob launched
           tangentially at ring radius): swept angle about the ring center >=
           2*pi (one full guided revolution) AND radial rms about R_ring <= 3 px
           over the guided lap. CONTROL (same launch, b=0) must NOT complete a
           revolution (swept < pi/2 or radial escape > 3px rms) — else invalid.
  G-CIRC   bonus: fresh tau=5.7 blob PARKED on the frozen ring: azimuthal
           displacement along the ring >= 5 px in 2000 tu (track-driven creep).

GATES (task 3 — genesis from noise; NULL quantification)
  Nucleation event: any record with ncomp >= 1 (connected u > thr component;
    thr = u0 + 0.45*(sqrt(lam)-u0), the frozen program threshold).
  For each (gamma, tau_b, D_b, sigma, source) cell, report over T:
    n_nucleation_events, max_t |u-u0|, max_t |b|. NULL is the honest expected
    deliverable: zero events + amplitude ceilings quantified.
  SURPRISE gate (if any nucleation): blob persists >= 500 tu after nucleation
    -> escalate to films + seeds.

Reduction-map verdict vocabulary: GROWABLE (self-written landscape passes the
functional gate at native L1 amplitude), SHAPE-ONLY (correct shape but needs
amplitude boost b_scale>1 to function; report the threshold scale),
NOT-GROWABLE (no L1 process found writes it), UNTESTED.
"""
E5_V_HAND = 0.0125        # px/tu, machine E5 moving-segment drift on hand saw
HAND_SLOPE = 5e-4         # k4-units/px, machine saw up-ramp slope (eps)
HAND_TOOTH = 0.0136       # full span of machine saw tooth (2*0.0068)
