import os, sys
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labbundle as LB
b = LB.open_bundle(sys.argv[1], profile="evaluation")
o = b.make_oracle()
import labkit, labkit.ops
print(labkit.__file__, labkit.ops.__file__, sys.dont_write_bytecode, os.environ.get("PYTHONDONTWRITEBYTECODE"))
print([p for p in sys.path][:4])
