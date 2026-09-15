"""Content-addressed genomes, recipe sources, generation runs, and harvested worlds.

Reading a registry never imports or executes recipe code. Evaluation bundles keep
their own physical identities; a world record can link to those identities.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path, PurePosixPath

FORMAT = "blobkit-registry-v1"
KINDS = {"genome", "recipe", "generation-run", "candidate", "checkpoint", "generation-result", "world-record"}
ID = re.compile(r"([a-z-]+):sha256:([0-9a-f]{64})\Z")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def _write_once(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"Registry content mismatch: {path}")
        return
    fd, temporary = tempfile.mkstemp(prefix=".record-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        # A hard link publishes complete bytes without replacing another writer.
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != data:
                raise ValueError(f"Registry content mismatch: {path}") from None
    finally:
        os.unlink(temporary)


class Registry:
    """A portable directory of immutable JSON records and binary artifacts."""

    def __init__(self, root):
        self.root = Path(root).resolve()

    def path(self, identifier):
        match = ID.fullmatch(identifier)
        if not match or match[1] not in KINDS | {"artifact"}:
            raise ValueError(f"Invalid registry ID: {identifier!r}")
        kind, digest = match.groups()
        return self.root / kind / (digest + (".bin" if kind == "artifact" else ".json"))

    def artifact(self, data):
        """Store exact bytes, including Python sources or prepared-state archives."""
        if not isinstance(data, bytes):
            raise TypeError("Artifacts must be bytes")
        identifier = "artifact:sha256:" + checksum(data)
        _write_once(self.path(identifier), data)
        return identifier

    def read_artifact(self, identifier):
        if not identifier.startswith("artifact:"):
            raise ValueError("Expected an artifact ID")
        data = self.path(identifier).read_bytes()
        if checksum(data) != identifier.rsplit(":", 1)[1]:
            raise ValueError(f"Artifact integrity mismatch: {identifier}")
        return data

    def put(self, kind, payload, *, refs=()):
        if kind not in KINDS:
            raise ValueError(f"Unknown record kind: {kind}")
        refs = sorted(set(refs))
        for ref in refs:
            self.read_artifact(ref) if ref.startswith("artifact:") else self.get(ref)
        body = dict(schema_version=FORMAT, kind=kind, refs=refs, payload=payload)
        identifier = kind + ":sha256:" + checksum(canonical(body))
        _write_once(self.path(identifier), canonical(dict(id=identifier, **body)) + b"\n")
        return identifier

    def get(self, identifier, *, kind=None):
        if identifier.startswith("artifact:"):
            raise ValueError("Use read_artifact for binary artifacts")
        record = json.loads(self.path(identifier).read_bytes())
        body = {key: value for key, value in record.items() if key != "id"}
        expected = body.get("kind", "") + ":sha256:" + checksum(canonical(body))
        if record.get("id") != identifier or expected != identifier or body.get("schema_version") != FORMAT:
            raise ValueError(f"Record integrity mismatch: {identifier}")
        if kind is not None and body["kind"] != kind:
            raise ValueError(f"Expected {kind}, got {body['kind']}")
        return record

    def records(self, kind):
        if kind not in KINDS:
            raise ValueError(f"Unknown record kind: {kind}")
        return [self.get(kind + ":sha256:" + p.stem) for p in sorted((self.root / kind).glob("*.json"))]

    def verify(self):
        """Verify every object and reference without executing archived code."""
        counts = {}
        for kind in sorted(KINDS):
            rows = self.records(kind)
            counts[kind] = len(rows)
            for row in rows:
                for ref in row["refs"]:
                    self.read_artifact(ref) if ref.startswith("artifact:") else self.get(ref)
        artifacts = list((self.root / "artifact").glob("*.bin"))
        for path in artifacts:
            self.read_artifact("artifact:sha256:" + path.stem)
        counts["artifact"] = len(artifacts)
        return dict(ok=True, counts=counts)

    def add_genome(self, genome):
        from .genome import genome_json, validate

        genome = genome_json(genome)
        canonical(genome)
        problems = validate(genome)
        if problems:
            raise ValueError("Invalid genome: " + "; ".join(problems))
        return self.put("genome", genome)

    def load_genome(self, identifier):
        """Load a fresh genome from either a genome ID or harvested world ID."""
        record = self.get(identifier)
        if record["kind"] == "world-record":
            record = self.get(record["payload"]["genome"], kind="genome")
        if record["kind"] != "genome":
            raise ValueError("Expected a genome or world record")
        return record["payload"]

    def add_source_world(self, name, genome, *, source, artifacts=None, links=None, recipe=None, run=None):
        """Register sourced or historical worlds without inventing missing runs.

        Source is a JSON object describing the known provenance and its gaps.
        Artifacts maps descriptive names to bytes. Links can include immutable
        Physim world/preparation/suite IDs, repository commits, and source URLs.
        """
        if not source:
            raise ValueError("A sourced world needs provenance")
        for identifier, kind in ((recipe, "recipe"), (run, "generation-run")):
            if identifier is not None:
                self.get(identifier, kind=kind)
        genome_id = self.add_genome(genome)
        archived = {name: self.artifact(data) for name, data in (artifacts or {}).items()}
        return self.put(
            "world-record",
            dict(
                name=name,
                genome=genome_id,
                source=source,
                artifacts=archived,
                links=links or {},
                run=run,
                recipe=recipe,
            ),
            refs=[genome_id, *archived.values(), *[ref for ref in (recipe, run) if ref is not None]],
        )

    def catalog(self):
        """Return a browsable projection; immutable records remain authoritative."""
        return {
            "schema_version": FORMAT,
            "verification": self.verify(),
            "worlds": [dict(id=row["id"], **row["payload"]) for row in self.records("world-record")],
            "recipes": [dict(id=row["id"], **row["payload"]) for row in self.records("recipe")],
            "runs": [dict(id=row["id"], **row["payload"]) for row in self.records("generation-run")],
            "results": [dict(id=row["id"], **row["payload"]) for row in self.records("generation-result")],
        }

    def export_recipe(self, identifier, destination):
        """Export recipe source files for inspection and explicit execution."""
        recipe = self.get(identifier, kind="recipe")["payload"]
        destination = Path(destination)
        sources = recipe["sources"]
        for name in sources:
            path = PurePosixPath(name)
            if path.is_absolute() or not path.parts or any(p in (".", "..") for p in name.split("/")) or "\\" in name:
                raise ValueError(f"Unsafe recipe source path: {name}")
            if name == "recipe.json":
                raise ValueError("recipe.json is reserved for the manifest")
        destination.mkdir(parents=True, exist_ok=False)
        for name, ref in sources.items():
            path = destination / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(self.read_artifact(ref))
        (destination / "recipe.json").write_bytes(canonical(dict(id=identifier, **recipe)) + b"\n")
        return destination
