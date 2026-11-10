"""physim2._rules -- the public rules that turn a submission directory into what the grader runs, and a
predictor's reply file into samples. One source for both sides: the grader's worker applies them to the
archive collected from your box; `lab.validate(...)` applies the same code in your box.

freeze(raw, root, max_mib)   the frozen submission: regular files and directories only (links and special
                             files are left out, as are __pycache__ directories), at most max_mib MiB of file
                             bytes, predict.py required at the top; everything read-only and owned by root.
                             These are the rules of agentenv's evaluator/submission.py snapshot(), applied to a
                             tar archive instead of a host directory.
read_reply(raw, ...)         reply.npz -> {level: float array}; refuses pickles and oversized (zip-bomb) members.
"""
import hashlib
import io
import os
import tarfile
import zipfile

import numpy as np

MIB = 1 << 20


def tar_dir(path: str) -> bytes:
    """A plain tar of directory `path`, members named relative to it (links are stored as links, not followed)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        tar.add(path, arcname=".", recursive=True)
    return buf.getvalue()


def freeze(raw: bytes | None, root: str, max_mib: float):
    """(archive bytes | None, manifest dict, error str | None). `root` is the member-name prefix of the
    submission inside `raw` ("." for tar_dir, "workspace/submission" for an archive collected by the grader);
    the returned archive keeps that prefix, so it restores to the same place."""
    if raw is None:
        return None, {"files": [], "bytes": 0}, "submission directory not found"
    root = root.strip("/") or "."
    keep, total, skipped = [], 0, 0
    try:
        src = tarfile.open(fileobj=io.BytesIO(raw), mode="r:")
        members = src.getmembers()
    except (tarfile.TarError, EOFError, ValueError):
        return None, {"files": [], "bytes": 0}, "unreadable submission archive"
    for m in members:
        name = os.path.normpath(m.name)
        if name != root and not name.startswith(root + "/") and root != ".":
            skipped += 1
            continue
        rel = "." if name == root else (name if root == "." else name[len(root) + 1:])
        parts = [] if rel == "." else rel.split("/")
        if os.path.isabs(name) or ".." in parts or "__pycache__" in parts:
            skipped += 1
            continue
        if m.isdir():
            keep.append((m, rel, None))
        elif m.isfile():
            total += m.size
            if total > max_mib * MIB:
                return None, {"files": [], "bytes": total}, f"submission larger than {max_mib:g} MiB"
            keep.append((m, rel, src.extractfile(m).read()))
        else:
            skipped += 1                                     # symbolic links, hard links, devices, fifos
    files = sorted(rel for _, rel, data in keep if data is not None)
    if "predict.py" not in files:
        return None, {"files": [], "bytes": total, "skipped": skipped}, "submission has no predict.py"
    out = io.BytesIO()
    man = []
    with tarfile.open(fileobj=out, mode="w") as dst:
        dirs = {"."} | {os.path.dirname(f) or "." for f in files}
        for d in sorted(dirs):                               # every parent directory, shallowest first
            cur = "."
            for part in ([] if d == "." else d.split("/")):
                cur = part if cur == "." else cur + "/" + part
                dirs.add(cur)
        for d in sorted(dirs, key=lambda x: (x.count("/"), x)):
            ti = tarfile.TarInfo(root if d == "." else f"{root}/{d}" if root != "." else d)
            ti.type, ti.mode, ti.uid, ti.gid = tarfile.DIRTYPE, 0o555, 0, 0
            dst.addfile(ti)
        for _, rel, data in sorted((k for k in keep if k[2] is not None), key=lambda k: k[1]):
            ti = tarfile.TarInfo(f"{root}/{rel}" if root != "." else rel)
            ti.size, ti.mode, ti.uid, ti.gid = len(data), 0o444, 0, 0
            dst.addfile(ti, io.BytesIO(data))
            man.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    digest = hashlib.sha256("".join(f"{f['path']}:{f['sha256']}\n" for f in man).encode()).hexdigest()
    return out.getvalue(), {"files": man, "bytes": total, "skipped": skipped, "sha256": digest}, None


def read_reply(raw: bytes, max_values: int) -> dict:
    """reply.npz bytes -> {level: array (float64)}. `max_values` bounds the total number of array elements the
    request can legitimately return; anything larger is refused before it is decompressed."""
    zf = zipfile.ZipFile(io.BytesIO(raw))
    if sum(i.file_size for i in zf.infolist()) > 8 * max_values + 4096 * (len(zf.infolist()) + 1):
        raise ValueError("reply larger than the request allows")
    z = np.load(io.BytesIO(raw), allow_pickle=False)
    return {int(k[5:]): np.asarray(z[k], float) for k in z.files}
