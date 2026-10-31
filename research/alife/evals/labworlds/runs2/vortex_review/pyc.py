import os, sys
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labbundle as LB
from physim.bundles import digest
b = LB.open_bundle(sys.argv[1], profile="evaluation")
if len(sys.argv) > 2:
    b.make_oracle()
print("opened ok; pyc digest", digest(os.path.join(sys.argv[1], "world/__pycache__/world.cpython-312.pyc"))[:12])
