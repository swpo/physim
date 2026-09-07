#!/usr/bin/env python3
"""Inspect existing NPZ member headers without materializing full arrays."""
import argparse, json, zipfile
from pathlib import Path
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("paths", nargs="+")
p.add_argument("--out", type=Path)
a = p.parse_args()
report = []
for path in a.paths:
    entries = []
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if not info.filename.endswith(".npy"):
                continue
            with z.open(info) as f:
                version = np.lib.format.read_magic(f)
                shape, fortran, dtype = np.lib.format._read_array_header(f, version)
            entries.append(dict(name=info.filename, shape=shape, dtype=str(dtype),
                                fortran=fortran, uncompressed_bytes=info.file_size,
                                compressed_bytes=info.compress_size))
    report.append(dict(path=str(Path(path).resolve()), entries=entries))
text = json.dumps(report, indent=2)
if a.out:
    a.out.write_text(text + "\n")
print(text)
