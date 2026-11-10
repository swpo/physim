"""physim2.wire -- JSON-lines messages with numpy arrays (shared by the Lab client and the Lab server).

One request per line: {"op": str, "args": {...}, "token": str}; one reply per line:
{"ok": true, "result": ...} or {"ok": false, "error": str, "kind": "violation" | "budget" | "closed" | "request"}.
Arrays travel as {"__nd__": [dtype, shape, base64 of the raw little-endian bytes]}.
"""
from __future__ import annotations

import base64
import json

import numpy as np

MAX_LINE = 64 * 1024 * 1024


def enc(o):
    if isinstance(o, np.ndarray):
        a = np.ascontiguousarray(o)
        if a.dtype.kind not in "fiub":
            raise TypeError(f"wire: unsupported array dtype {a.dtype}")
        return {"__nd__": [a.dtype.str, list(a.shape), base64.b64encode(a.tobytes()).decode("ascii")]}
    if isinstance(o, dict):
        return {str(k): enc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [enc(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def dec(o):
    if isinstance(o, dict):
        if "__nd__" in o and len(o) == 1:
            dt, shape, b = o["__nd__"]
            dt = np.dtype(dt)
            if dt.kind not in "fiub":
                raise ValueError("wire: unsupported array dtype")
            return np.frombuffer(base64.b64decode(b), dtype=dt).reshape(shape).copy()
        return {k: dec(v) for k, v in o.items()}
    if isinstance(o, list):
        return [dec(v) for v in o]
    return o


def dumps(o) -> bytes:
    return (json.dumps(enc(o), allow_nan=False) + "\n").encode("utf-8")


def loads(b: bytes):
    return dec(json.loads(b.decode("utf-8")))
