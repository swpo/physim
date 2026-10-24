"""Random-rule search for self-propelled Flow-Lenia bodies: one noise patch, measure COM travel."""
import sys
sys.path.insert(0, 'threads/flow-lenia/scripts')
from screen import run
lo, hi, C, Rs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
for r in range(lo, hi):
    print(run('threads/flow-lenia/worlds/fl_base/world.py', f'threads/flow-lenia/screens/mot/C{C}_r{r}.png', steps=800,
              nframes=8, size=(96, 96), sets=[f'rule_seed={r}', f'C={C}', f'R_scale={Rs}', 'patch=20'], quiet=True), flush=True)
