"""Public roster and operational bounds for this worked-example version."""
from dataclasses import replace
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'environments/physim'))
from physim.blobround6_eval import DEFAULT_LIMITS, PublicRoster

ROSTER=PublicRoster(n_ports=12,device_slots=(13,19))
LIMITS=replace(DEFAULT_LIMITS,max_horizon_tu=50.)
