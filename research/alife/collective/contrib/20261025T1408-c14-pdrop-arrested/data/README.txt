Screen settings (overrides of the P defaults in the first version of world.py, which had phi0=-0.95, noise=0.01, r=0.05, g=0.05, nK=0.3, F=0.004, Du=2.0):
o1 phi0 -0.4 | o2 phi0 -0.5 noise 0.05 | o3 phi0 -0.4 nK 1.5 | o4 phi0 -0.4 kcat 0.3   (all: particles die before droplets form)
o5 phi0 -0.3 noise 0.1 g 0.005 r 0.2 nK 0.5 | o6 same with g 0.01 r 0.1 nK 1 kd 0.01
o7 = o5 + F 0.01 | o8 = o5 + F 0.02 (one domain-filling phase)
o9 = o5 + F 0.01 Du 0.3 (the published defaults) | o10 = o5 + F 0.005 Du 0.2 | o11 = o5 + F 0.01 Du 0.1
Columns: drops = components of phi > 0, median/max area in px, occupancy, particle count, min fuel.
