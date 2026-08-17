# Direction: MORPHO COUNTER (quantized pattern states + hysteresis staircase)

Build a Turing-pattern world whose STRIPE/SPOT COUNT is a crisp integer
macro variable controlled by a slow field.

Physics sketch: standard 2-field Turing pair (activator-inhibitor, e.g.
Gierer-Meinhardt or Gray-Scott in stripe regime) on a RING-like domain or
torus; a third SLOW control field C (diffusing, slowly relaxing toward a
drivable set-point) scales the pattern wavelength (e.g. multiplies diffusion
or feed). As C drifts, the pattern count n must requantize: n jumps between
integers with HYSTERESIS (Eckhaus-like band).

Target hierarchy:
  L1 (fast): local reaction-diffusion
  L2 (medium): defect dynamics — stripe insertion/annihilation events when
      the count requantizes (measurable as discrete events)
  L3 (slow, TOP): the integer STAIRCASE n(C) with hysteresis — top model
      "switch"/staircase; dwell statistics; the width of hysteresis loops is
      the compact law.

Theory coordinates: wavelength-control exponent (how C scales the intrinsic
wavelength), C relaxation time vs pattern adjustment time (need >= 10x
separation), domain size / wavelength ratio (sets accessible n range).
G3: staircase step positions must move smoothly with a micro parameter.
Count stripes robustly (FFT peak or connected components).

Real-world analogue: somites, digit count, convection-roll quantization.
Films: pattern smoothly morphing then SNAPPING to a new count.

Name your dir probes/search/morpho-counter/.
