"""Safe capture: copy files that came out of a box onto the worker's disk, for the record.

Everything a box hands out is hostile input: the agent is root there and controls both the files and the tools
(`tar`, `find`) that pack them. This module is the ONLY code that writes box content to the worker's file
system. Its rules:

  one pass        the archive is read as a stream, once; for every entry the decision is taken from the entry's
                  header alone, before any of its bytes is read; nothing is looked up twice (no stat-then-copy)
  regular files   only entries of type "regular file" are written. Symbolic links, hard links, devices, fifos,
                  sparse files and every other type are skipped and listed
  names           absolute paths, paths with a ".." component and paths outside the declared root are skipped.
                  Every component of a kept path is rewritten to letters, digits and `. _ + = @ , -` (anything
                  else becomes `_`); a component of dots only becomes `_`. Two entries that map to the same
                  name: the second is skipped
  caps            at most `max_files` entries (files AND the directories made for them) and `max_bytes` bytes in
                  all (default 2000 and 20 MiB), counted while writing; depth and name length are bounded. What
                  does not fit is skipped and listed
  a cut archive   a file whose bytes end early, or whose read fails inside the archive, stays as far as it was
                  written: it is listed under "skipped" with `partial` (its safe path and the bytes on disk)
  where           only below `dest`, a directory this module creates itself (it refuses one that exists). Every
                  directory and file is created relative to an open directory handle with O_NOFOLLOW and O_EXCL,
                  mode 0700 / 0600: a link cannot be followed and an existing file cannot be overwritten
  no execution    nothing is unpacked by an external tool, nothing is imported, nothing gets an execute bit

The result is a manifest: the files written (safe path, bytes, sha256) and what was skipped (why, the declared
size, and the original name escaped to ASCII and cut to 200 characters; that text is the agent's, treat it as
data). Nothing here deletes, moves or changes modes of anything.
"""
from __future__ import annotations

import hashlib
import io
import os
import re
import shlex
import tarfile

MAX_FILES = 2000
MAX_BYTES = 20 << 20
MAX_DEPTH = 16
MAX_NAME = 120
MAX_PATH = 512
MAX_LISTED = 500                                             # entries of the "skipped" listing (the count is always exact)
UNSAFE = re.compile(r"[^A-Za-z0-9._+=@,-]")
CHUNK = 1 << 16
WHY = ("not a regular file: symbolic link", "not a regular file: hard link", "not a regular file: device",
       "not a regular file: fifo", "not a regular file: other type", "sparse file", "absolute path", "parent path",
       "outside the root", "empty name", "too deep", "path too long", "name collision", "file count cap", "size cap",
       "write failed", "short read")


def safe_parts(name: str, root: str):
    """(list of sanitised path components relative to `root`, None) or (None, why). Pure; no file system."""
    if name.startswith("/"):
        return None, "absolute path"
    parts = [p for p in name.split("/") if p not in ("", ".")]
    if ".." in parts:
        return None, "parent path"
    rparts = [p for p in root.strip("/").split("/") if p not in ("", ".")]
    if parts[:len(rparts)] != rparts:
        return None, "outside the root"
    parts = parts[len(rparts):]
    if not parts:
        return None, "empty name"
    if len(parts) > MAX_DEPTH:
        return None, "too deep"
    out = []
    for p in parts:
        s = UNSAFE.sub("_", p)
        if not s.strip("."):
            s = "_" * max(1, len(s))
        out.append(s[:MAX_NAME])
    if len("/".join(out)) > MAX_PATH:
        return None, "path too long"
    return out, None


def kind(m: tarfile.TarInfo):
    """None for a plain regular file, else why the entry is not written (from the header's type alone)."""
    if m.type in (tarfile.REGTYPE, tarfile.AREGTYPE) and not m.issparse():
        return None
    if m.issparse():
        return "sparse file"
    if m.issym():
        return "not a regular file: symbolic link"
    if m.islnk():
        return "not a regular file: hard link"
    if m.ischr() or m.isblk():
        return "not a regular file: device"
    if m.isfifo():
        return "not a regular file: fifo"
    return "not a regular file: other type"


def _shown(name) -> str:
    return ascii(str(name))[1:-1][:200]


def extract(raw: bytes | None, root: str, dest: str, *, max_files: int = MAX_FILES, max_bytes: int = MAX_BYTES,
            write: bool = True) -> dict:
    """Write the regular files of tar archive `raw` that lie below `root` (a member-name prefix such as
    "workspace/submission") into the NEW directory `dest`; with write=False only the manifest is made.
    Never raises on the archive's content: an unreadable or truncated archive ends the pass and is recorded."""
    man = {"root": root, "files": [], "skipped": [], "n_files": 0, "bytes": 0, "n_skipped": 0, "skipped_bytes_declared": 0,
           "directories_seen": 0, "directories_made": 0, "caps": {"max_files": int(max_files), "max_bytes": int(max_bytes)},
           "complete": True, "archive": "none" if raw is None else "read to its end", "written": bool(write)}
    if raw is None:
        return man
    top = -1
    if write:
        os.mkdir(dest, 0o700)                                # FileExistsError: never write into something that is already there
        top = os.open(dest, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    seen: set[str] = set()
    made: set[str] = set()                                   # directories made below dest (they count against max_files)

    def skip(m, why, partial=None):
        man["n_skipped"] += 1
        man["complete"] = False
        man["skipped_bytes_declared"] += max(0, int(getattr(m, "size", 0) or 0)) if m is not None and m.isreg() else 0
        if len(man["skipped"]) < MAX_LISTED:
            row = {"name": _shown(getattr(m, "name", "?")), "why": why, "bytes_declared": int(getattr(m, "size", 0) or 0)}
            if partial is not None:
                row["partial"] = partial
            man["skipped"].append(row)

    try:
        tar = tarfile.open(fileobj=io.BytesIO(raw), mode="r|")           # a stream: one pass, no seeking back
        for m in tar:
            if m.isdir():
                man["directories_seen"] += 1
                continue
            why = kind(m)
            parts = None
            if why is None:
                parts, why = safe_parts(m.name, root)
            if why is None and "/".join(parts) in seen:
                why = "name collision"
            new_dirs = [] if why is not None else ["/".join(parts[:i]) for i in range(1, len(parts)) if "/".join(parts[:i]) not in made]
            if why is None and man["n_files"] + len(made) + len(new_dirs) + 1 > max_files:
                why = "file count cap"
            if why is None and (m.size < 0 or man["bytes"] + m.size > max_bytes):
                why = "size cap"
            if why is not None:
                skip(m, why)
                continue
            rel = "/".join(parts)
            made.update(new_dirs)                            # counted whether or not they are written (write=False)
            h, n, fd, dirs, ok, opened, broken = hashlib.sha256(), 0, -1, [], True, False, None
            try:
                src = tar.extractfile(m)                     # bounded by the header's size; read in pieces below
                if write:
                    cur = top
                    for p in parts[:-1]:                     # one level at a time, relative to a handle, never through a link
                        try:
                            os.mkdir(p, 0o700, dir_fd=cur)
                        except FileExistsError:
                            pass
                        nxt = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=cur)
                        dirs.append(nxt)
                        cur = nxt
                    fd = os.open(parts[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=cur)
                    opened = True
                while n < m.size:
                    b = src.read(min(CHUNK, m.size - n))
                    if not b:
                        break
                    if man["bytes"] + n + len(b) > max_bytes:            # counted while writing, whatever the header said
                        ok = False
                        break
                    if fd >= 0:
                        os.write(fd, b)
                    h.update(b)
                    n += len(b)
            except OSError:
                ok = False
            except (tarfile.TarError, EOFError, ValueError) as e:     # the archive broke inside this file's bytes
                ok, broken = False, e
            finally:
                if fd >= 0:
                    os.close(fd)
                for d in dirs:
                    os.close(d)
            seen.add(rel)
            man["directories_made"] = len(made)
            if not ok or n != m.size:
                partial = {"path": rel, "bytes_on_disk": n} if opened else None
                skip(m, "short read" if broken is not None else "size cap" if man["bytes"] + n >= max_bytes else "short read" if ok
                     else "write failed", partial)
                man["bytes"] += n                            # what reached the disk counts against the cap
                if broken is not None:
                    raise broken                             # the stream is broken: end the pass (recorded below)
                continue
            man["files"].append({"path": rel, "bytes": n, "sha256": h.hexdigest()})
            man["n_files"] += 1
            man["bytes"] += n
    except (tarfile.TarError, EOFError, ValueError, OSError) as e:
        man["archive"] = f"unreadable or cut after {man['n_files'] + man['n_skipped']} entries ({type(e).__name__})"
        man["complete"] = False
    finally:
        if top >= 0:
            os.close(top)
    man["directories_made"] = len(made)
    return man


def workspace_command(workdir: str, out: str, *, exclude=("physim2", "submission"), max_file_kib: int = 2048,
                      max_files: int = MAX_FILES, max_bytes: int = MAX_BYTES) -> str:
    """The shell line that packs a size-capped copy of the working directory INSIDE the box (its `find`, `tar`
    and `head`: the agent's tools, so the result is only ever read by `extract`). Regular files of at most
    max_file_kib KiB, at most max_files of them, without the public package and submission/ (captured on its
    own) and without bytecode caches; the stream is cut at max_bytes."""
    prune = " -o ".join(f"-path ./{shlex.quote(e)}" for e in exclude) + " -o -name __pycache__"
    return (f"cd {shlex.quote(workdir)} && find . -xdev \\( {prune} \\) -prune -o -type f -size -{int(max_file_kib) + 1}k -print0 2>/dev/null "
            f"| head -z -n {int(max_files)} | tar --null --no-recursion -T - -cf - 2>/dev/null | head -c {int(max_bytes)} > {shlex.quote(out)}; "
            f"test -f {shlex.quote(out)}")


def listing_command(workdir: str, max_lines: int = 4000) -> str:
    """The shell line that lists the working directory inside the box: type, size in bytes, path (one per line)."""
    return (f"cd {shlex.quote(workdir)} && find . -xdev -name __pycache__ -prune -o -printf '%y %s %p\\n' 2>/dev/null "
            f"| head -n {int(max_lines)} | head -c 400000")


def parse_listing(text: str, max_lines: int = 4000) -> dict:
    """The listing as data: [type letter, size, name escaped to ASCII and cut]. The text is the box's own."""
    rows, total = [], 0
    for line in text.splitlines()[:max_lines]:
        p = line.split(" ", 2)
        if len(p) != 3 or len(p[0]) != 1 or not p[1].isdigit():
            continue
        size = int(p[1][:15])
        rows.append([p[0] if p[0] in "fdlpsbc" else "?", size, _shown(p[2])])
        total += size if p[0] == "f" else 0
    return {"entries": rows, "n": len(rows), "file_bytes": total, "cut_at_lines": max_lines}
