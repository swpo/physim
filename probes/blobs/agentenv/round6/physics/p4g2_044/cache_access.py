"""Small read-only helpers for uncompressed NPZ caches. No field extraction."""
import json
import struct
import zipfile
from pathlib import Path
import numpy as np


def memmap_member(path, name):
    """Map a ZIP_STORED .npy member directly; fail rather than silently copy."""
    path = Path(path)
    member = name if name.endswith(".npy") else name + ".npy"
    with zipfile.ZipFile(path) as z:
        info = z.getinfo(member)
        if info.compress_type != zipfile.ZIP_STORED:
            raise ValueError("memmap requires ZIP_STORED: " + member)
        header_offset = info.header_offset
    with path.open("rb") as f:
        f.seek(header_offset)
        header = f.read(30)
        if header[:4] != b"PK\x03\x04":
            raise ValueError("bad local ZIP header")
        name_len, extra_len = struct.unpack("<HH", header[26:30])
        f.seek(header_offset + 30 + name_len + extra_len)
        version = np.lib.format.read_magic(f)
        shape, fortran, dtype = np.lib.format._read_array_header(f, version)
        if dtype.hasobject:
            raise ValueError("object arrays cannot be mapped")
        offset = f.tell()
    return np.memmap(path, dtype=dtype, mode="r", offset=offset,
                     shape=shape, order="F" if fortran else "C")


def json_member(path, name="meta"):
    with np.load(path, allow_pickle=False) as z:
        return json.loads(str(z[name]))


def project_root():
    return Path(__file__).resolve().parents[6]


def make_devices(root, nf=12, L=128.0):
    import sys
    sys.path.insert(0, str(root / "probes/blobs/agentenv"))
    import device as D
    roster = [dict(lattice="square", n_rings=3, base_ds=3.5),
              dict(lattice="hex", n_rings=3, base_ds=3.0)]
    sec = D.world_secrets("p4g2_044|s928|A0", nf, roster, L)
    devs = []
    for i, (cfg, ds) in enumerate(zip(roster, sec["devices"])):
        devs.append(D.ProbeDevice(dev_id=i, L=L, **cfg, **ds))
    return sec, devs


def raw_stats(F):
    return dict(min=F.min(axis=(1, 2)).tolist(), max=F.max(axis=(1, 2)).tolist(),
                mean=F.mean(axis=(1, 2)).tolist(), std=F.std(axis=(1, 2)).tolist())
