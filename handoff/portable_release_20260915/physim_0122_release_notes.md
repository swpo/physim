Physim 0.12.2 fixes cold-start reliability of the stock Verifiers bash harness. Build `physim-agent:0.12.2` using the setup archive: its dependency cache is prepared at image build time, and runtime startup uses `UV_OFFLINE=true` and `PIP_NO_INDEX=1`. The unchanged predictor image remains `physim-predictor:0.12.0`.

The original live smoke exposed a harness setup timeout before model execution. The corrected image now starts the exact stock harness with Docker networking disabled in 2.2 seconds. Native integration checks pass. Numerical source, scoring, and world/preparation/suite identities are unchanged.

This release retains explicit immutable HF world selection and zero reward for otherwise completed runs without a valid predictor. Infrastructure failures remain native Verifiers errors. The separately released Blobkit 0.3.5 wheel remains pinned by SHA-256.

Download `physim-setup-0.12.2.tar.gz` and verify `SHA256SUMS-0.12.2`; the archive contains `requirements.txt`, world configs, Dockerfiles, and verification helpers. Use Python 3.12:

```sh
uv venv --python 3.12
uv pip install 'physim[hub,reference] @ https://github.com/swpo/physim/releases/download/physim-v0.12.2/physim-0.12.2-py3-none-any.whl#sha256=dee8ec2e19b0ab57531758c535b1838020f8c3f0f6c138ae9d1eeed61c45e57f'
```

Source commit: `eb6647cb429226dc43b27db6950329ed849b92d9`. The wheel's package files match this source byte for byte. The PyPI project named `physim` is unrelated; use these explicit release assets.

Final verification completed on 15 September 2026: a [fresh Linux runner](https://github.com/swpo/physim/actions/runs/34970845043) installed the public wheels outside a checkout, anonymously fetched all three world preparations, verified offline reuse, reproduced the reference controls, ran fresh short simulations, built both Docker images and started the exact stock harness with networking disabled. The offline harness check took 3.13 seconds on Linux and 2.20 seconds on macOS.

Two live four-turn DeepSeek V4 Flash rollouts on BF completed without infrastructure errors. Both reached the turn limit without a predictor and correctly earned zero reward. This is an integration smoke, not a capability evaluation. Full configs retain the generous investigation budgets.

The [HF dataset card and release metadata](https://huggingface.co/datasets/seanpohorence/physim-worlds/tree/0813ee4d0a4e97a12bbf598d5d43a45eddf5492f) now link this release. Scientific payloads and runtime data pins are unchanged. The older README line in the packaged distribution saying that no predictor raises a task error is stale: the implemented and tested behavior is zero reward for otherwise completed attempts. The current source README is corrected.
