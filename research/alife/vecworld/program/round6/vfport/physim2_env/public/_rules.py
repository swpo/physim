"""physim2._rules -- the public rules that turn a submission directory into what the grader runs, and a
predictor's reply file into samples. One source for both sides: the grader's worker applies them to the
archive collected from your box; `lab.validate(...)` applies the same code in your box.

freeze(raw, root, max_mib)   the frozen submission: regular files and directories only (links and special
                             files are left out, as are __pycache__ directories and names with control
                             characters or undecodable bytes), at most max_mib MiB of file bytes, predict.py
                             required at the top; everything read-only and owned by root. REFUSED as a whole:
                             an archive that names the same path twice, a path that is both a file and a
                             directory, a path longer than MAX_PATH bytes (MAX_NAME per component), more than
                             MAX_MEMBERS members. These are the rules of agentenv's evaluator/submission.py
                             snapshot(), applied to a tar archive instead of a host directory; the refusals
                             cover what a directory can never contain but a hand-made archive can.
read_reply(raw, max_values)  reply.npz -> {level: float64 array}. Strict: members named level<l>.npy only, one
                             per level, at most MAX_LEVELS; every member a C-ordered little-endian float32 array
                             with three axes (what physim2/predict_runner.py writes); at most max_values numbers
                             in all. Nothing is allocated from a size the reply declares before that size is
                             checked; pickles cannot be loaded.
"""
import hashlib
import io
import os
import re
import tarfile
import zipfile

import numpy as np

MIB = 1 << 20
MAX_MEMBERS = 20000
MAX_PATH = 1024
MAX_NAME = 255
MAX_DEPTH = 32
MAX_LEVELS = 16
_LEVEL = re.compile(r"^level(0|[1-9][0-9]{0,3})\.npy$")


def tar_dir(path: str) -> bytes:
    """A plain tar of directory `path`, members named relative to it (links are stored as links, not followed)."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        tar.add(path, arcname=".", recursive=True)
    return buf.getvalue()


def _clean(name: str) -> bool:
    """A name the frozen archive can carry to any box: valid text without control characters."""
    try:
        name.encode("utf-8")
    except UnicodeError:                                     # undecodable bytes arrive as lone surrogates
        return False
    return not any(ord(c) < 32 or ord(c) == 127 for c in name)


def freeze(raw: bytes | None, root: str, max_mib: float):
    """(archive bytes | None, manifest dict, error str | None). `root` is the member-name prefix of the
    submission inside `raw` ("." for tar_dir, "workspace/submission" for an archive collected by the grader);
    the returned archive keeps that prefix, so it restores to the same place."""
    none = {"files": [], "bytes": 0}
    if raw is None:
        return None, none, "submission directory not found"
    root = root.strip("/") or "."
    files, dirs_seen, total, skipped = {}, set(), 0, 0
    try:
        src = tarfile.open(fileobj=io.BytesIO(raw), mode="r:")
        members = []
        for m in src:
            members.append(m)
            if len(members) > MAX_MEMBERS:
                return None, none, f"submission has more than {MAX_MEMBERS} entries"
    except (tarfile.TarError, EOFError, ValueError, OSError):
        return None, none, "unreadable submission archive"
    for m in members:
        name = os.path.normpath(m.name)
        if name != root and not name.startswith(root + "/") and root != ".":
            skipped += 1
            continue
        rel = "." if name == root else (name if root == "." else name[len(root) + 1:])
        parts = [] if rel == "." else rel.split("/")
        if os.path.isabs(name) or ".." in parts or "__pycache__" in parts or not _clean(rel):
            skipped += 1
            continue
        if not (m.isdir() or m.isfile()):
            skipped += 1                                     # symbolic links, hard links, devices, fifos
            continue
        if len(rel.encode()) > MAX_PATH or len(parts) > MAX_DEPTH or any(len(p.encode()) > MAX_NAME for p in parts):
            return None, none, f"submission has a path longer than {MAX_PATH} bytes (or a name longer than {MAX_NAME})"
        if m.isdir():
            if rel in files:
                return None, none, "submission archive names one path as a file and as a directory"
            dirs_seen.add(rel)
            continue
        if rel in files:
            return None, none, "submission archive names the same file twice"
        total += m.size
        if total > max_mib * MIB:
            return None, {"files": [], "bytes": total}, f"submission larger than {max_mib:g} MiB"
        try:
            data = src.extractfile(m).read()
        except (tarfile.TarError, EOFError, ValueError, OSError, AttributeError):
            return None, none, "unreadable submission archive"
        if len(data) != m.size:
            return None, none, "unreadable submission archive"
        files[rel] = data
    if "predict.py" not in files:
        return None, {"files": [], "bytes": total, "skipped": skipped}, "submission has no predict.py"
    dirs = {"."}
    for f in files:                                          # every parent directory of every kept file
        cur = os.path.dirname(f)
        while cur:
            dirs.add(cur)
            cur = os.path.dirname(cur)
    if (dirs | dirs_seen) & set(files):
        return None, none, "submission archive names one path as a file and as a directory"
    out = io.BytesIO()
    man = []
    with tarfile.open(fileobj=out, mode="w", format=tarfile.PAX_FORMAT) as dst:
        for d in sorted(dirs, key=lambda x: (x.count("/"), x)):          # shallowest first
            ti = tarfile.TarInfo(root if d == "." else f"{root}/{d}" if root != "." else d)
            ti.type, ti.mode, ti.uid, ti.gid = tarfile.DIRTYPE, 0o555, 0, 0
            dst.addfile(ti)
        for rel in sorted(files):
            data = files[rel]
            ti = tarfile.TarInfo(f"{root}/{rel}" if root != "." else rel)
            ti.size, ti.mode, ti.uid, ti.gid = len(data), 0o444, 0, 0
            dst.addfile(ti, io.BytesIO(data))
            man.append({"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    digest = hashlib.sha256("".join(f"{f['path']}:{f['sha256']}\n" for f in man).encode()).hexdigest()
    return out.getvalue(), {"files": man, "bytes": total, "skipped": skipped, "sha256": digest}, None


def reply_mib(max_values: int) -> int:
    """The driver's --max-reply-mib for a request that can legitimately return `max_values` numbers: float32 and
    the npz framing, rounded up to whole MiB (1 for the ring: 256 samples x 36 values = 36 KiB)."""
    return max(1, -(-(4 * int(max_values) + (64 << 10)) // MIB))


def read_reply(raw: bytes, max_values: int) -> dict:
    """reply.npz bytes -> {level: array (float64)}. Raises ValueError (public wording) on anything else than
    what predict_runner.py writes. `max_values` bounds the numbers the request can legitimately return."""
    from numpy.lib import format as npf
    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
    except (zipfile.BadZipFile, OSError, ValueError):
        raise ValueError("the reply is not an .npz file") from None
    infos = zf.infolist()
    if not 1 <= len(infos) <= MAX_LEVELS:
        raise ValueError(f"the reply must hold one array per level (at most {MAX_LEVELS})")
    names = [i.filename for i in infos]
    if len(set(names)) != len(names) or not all(_LEVEL.match(n) for n in names):
        raise ValueError("the reply's arrays must be named level<l>, one per level")
    if sum(i.file_size for i in infos) > 4 * max_values + 1024 * len(infos):
        raise ValueError("the reply is larger than the request allows")
    out, left = {}, int(max_values)
    for i in infos:
        try:
            with zf.open(i) as f:
                version = npf.read_magic(f)
                if version == (1, 0):
                    shape, fortran, dtype = npf.read_array_header_1_0(f)
                elif version == (2, 0):
                    shape, fortran, dtype = npf.read_array_header_2_0(f)
                else:
                    raise ValueError("format version")
                if dtype != np.dtype("<f4") or fortran or len(shape) != 3:
                    raise ValueError(f"level arrays must be C-ordered float32 with three axes (as predict_runner.py writes them); got {dtype} with {len(shape)} axes")
                count = 1
                for s in shape:
                    count *= int(s)
                if count > left:
                    raise ValueError("the reply is larger than the request allows")
                left -= count
                data = f.read(4 * count + 1)
        except ValueError as e:
            raise ValueError(str(e) if "level arrays" in str(e) or "larger" in str(e) else "a level array of the reply is unreadable") from None
        except Exception:
            raise ValueError("a level array of the reply is unreadable") from None
        if len(data) != 4 * count:
            raise ValueError("a level array of the reply is unreadable")
        out[int(_LEVEL.match(i.filename).group(1))] = np.frombuffer(data, "<f4").reshape(shape).astype(np.float64)
    return out
