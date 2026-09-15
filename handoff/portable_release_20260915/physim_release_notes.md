Physim 0.12.1 provides a standalone Verifiers environment for experimental prediction in prepared physical worlds. It depends on the public Blobkit 0.3.5 wheel, pinned by SHA-256.

Published-world configs explicitly select the original reference, BF trail lab, or XV rotor lab at an immutable Hugging Face revision. Data are fetched and verified by the trusted host; the agent receives observations and its own workspace. No world is selected implicitly. Completed attempts without a valid predictor earn zero reward; infrastructure failures remain Verifiers errors.

Download `requirements.txt` and `physim-setup.tar.gz`, verify `SHA256SUMS`, and follow the included README to install with Python 3.12 and uv, build the two Docker images, and run a selected config. The PyPI project named physim is unrelated.

```sh
uv venv --python 3.12
uv pip install -r requirements.txt
```

Source commit: `55ab966415f1504a430379064b74e274d8bde553`. Validation before publication: 48 native/bundle/roster tests with 13 subtests, followed by 20 native tests with six subtests after the zero-reward policy change; Ruff and both Docker builds passed. The installed wheels' package bytes match the source commit. The scientific numerical implementation and world/preparation/suite identities are unchanged.

Full standalone installation command:

```sh
uv pip install 'physim[hub,reference] @ https://github.com/swpo/physim/releases/download/physim-v0.12.1/physim-0.12.1-py3-none-any.whl#sha256=1d81f8716666d4c89f09194f4a215cecb76882ba0de6a634fa6621bb5455bb74'
```
