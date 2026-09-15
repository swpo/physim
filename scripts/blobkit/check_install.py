"""Verify a blobkit wheel in a fresh environment outside the source checkout."""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--python", default="3.12")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    target = args.workdir.resolve()
    target.mkdir(parents=True, exist_ok=False)
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required")
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("VIRTUAL_ENV", "PYTHONPATH", "PYTHONHOME", "UV_PROJECT_ENVIRONMENT")
        and not any(part in key.upper() for part in ("TOKEN", "SECRET", "API_KEY"))
    }
    env.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    subprocess.run([uv, "venv", "--python", args.python, str(target / "venv")], check=True, env=env)
    python = target / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    extras = "test,plot" if args.plot else "test"
    subprocess.run(
        [uv, "pip", "install", "--python", str(python), str(args.wheel.resolve()) + "[" + extras + "]"],
        check=True,
        env=env,
    )
    shutil.copytree(
        ROOT / "packages/blobkit/tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )
    code = (
        "import json,sys,blobkit; from importlib.metadata import version; "
        + "assert 'jax' not in sys.modules; "
        + "print(json.dumps({'python':sys.version,'path':blobkit.__file__,"
        + "'integrity':blobkit.verify_locks(strict=True),'versions':"
        + "{n:version(n) for n in ('blobkit','numpy','scipy')}}))"
    )
    installed = subprocess.check_output([str(python), "-I", "-c", code], cwd=target, env=env, text=True)
    (target / "installation.json").write_text(json.dumps(json.loads(installed), indent=2) + "\n")
    subprocess.run(
        [
            str(python),
            "-I",
            "-m",
            "pytest",
            "tests",
            "-m",
            "not accelerator and not slow",
            "-v",
            "--junitxml=tests.xml",
        ],
        cwd=target,
        env=env,
        check=True,
    )


if __name__ == "__main__":
    main()
