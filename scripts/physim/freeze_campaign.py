"""Archive the local implementation and dependency identities before paid runs."""

import hashlib
import importlib.metadata
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def freeze(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    paths = set()
    for directory in ("environments/physim", "packages/blobkit", "generators/physim", "scripts/physim"):
        for path in (ROOT / directory).rglob("*"):
            if (
                path.is_file()
                and path.suffix in (".py", ".toml", ".md")
                and not any(part in (".venv", "__pycache__", "build", "dist") for part in path.parts)
            ):
                paths.add(path)
    paths.update(ROOT / name for name in ("pyproject.toml", "uv.lock"))
    sources = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}
    archive_id = hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest()
    archive = output / f"sources-{archive_id}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        for path in sorted(paths):
            handle.write(path, path.relative_to(ROOT))
    packages = {
        dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions() if dist.metadata.get("Name")
    }
    images = json.loads(
        subprocess.check_output(["docker", "image", "inspect", "physim-agent:0.12.2", "physim-predictor:0.12.0"])
    )
    record = dict(
        created_utc=datetime.now(timezone.utc).isoformat(),
        source_id=archive_id,
        archive=archive.name,
        archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
        git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        sources=sources,
        packages=dict(sorted(packages.items())),
        images={tag: image["Id"] for image in images for tag in image["RepoTags"]},
    )
    (output / "provenance.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in ("source_id", "archive", "images")}, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/evaluation-campaign-20260916")
    freeze(parser.parse_args().output)
