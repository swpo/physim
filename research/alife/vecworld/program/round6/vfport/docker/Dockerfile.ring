# PhySim v2 ring exam: the ONE image of every box (agent box, verifier box, item boxes; the isolated grader boots
# the verifier from the solver's resolved image). CPU only. The public world module imports the vw library,
# which imports jax and scipy, so numpy alone is not enough (agentenv/physim2/world_ring.py:25-29).
#
#   docker build -f docker/Dockerfile.ring -t physim2-ring:2 docker/
#
# Version 2 (round 4): THE HARNESS IS PREINSTALLED. verifiers' stock `bash` harness prepares its chat program
# inside the box at set-up: `command -v uv || pip install --user uv || <download uv>`, then `uv sync --script`
# and `uv python find --script` on a script that declares six packages (verifiers runtimes/base.py:41-46,
# 258-292; harnesses/utils/launch.py:27-32). With image 1 every model rollout therefore downloaded uv and about
# 35 unpinned packages into its box. This image holds those packages already, each pinned and checked by hash
# (harness-requirements.txt), in /opt/physim2-harness/venv, and /usr/local/bin/uv is a stand-in of 40 lines
# (harness-uv) that hands verifiers that environment. A box fetches nothing at set-up and needs no network for
# it; nothing is written outside /tmp, so the box's root can be read-only. The scientific packages are pinned
# by hash as well (ring-requirements.txt). There is no real uv and no pip cache in the image.
#
# Network at build time: the base image, the package index (files.pythonhosted.org, pypi.org) and Debian's
# mirror (binutils, for `strip`, in the build stage only). Nothing of the build stage but the three copied
# trees reaches the final image.
#
# Behind a TLS-intercepting proxy (NOT on the lead's Mac): pass the proxy's own CA certificate, base64 of its PEM
# file on one line, and the proxy address; both default to nothing, and both stay in the build stage:
#   --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg EXTRA_CA_B64="$(base64 -w0 proxy-ca.crt)"
FROM python:3.12-slim AS build
ARG HTTPS_PROXY=""
ARG EXTRA_CA_B64=""
COPY ring-requirements.txt harness-requirements.txt /tmp/req/
RUN set -e; if [ -n "$EXTRA_CA_B64" ]; then \
      printf '%s' "$EXTRA_CA_B64" | base64 -d > /tmp/extra-ca.crt; \
      cat /etc/ssl/certs/ca-certificates.crt /tmp/extra-ca.crt > /tmp/ca-bundle.crt; \
      export PIP_CERT=/tmp/ca-bundle.crt; \
      sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources; \
      printf 'Acquire::https::Proxy "%s";\nAcquire::https::CaInfo "/tmp/ca-bundle.crt";\n' "$HTTPS_PROXY" > /etc/apt/apt.conf.d/99proxy; fi; \
    export HTTPS_PROXY="$HTTPS_PROXY"; \
    pip install --no-cache-dir --no-compile --disable-pip-version-check --require-hashes --only-binary :all: \
        --target /opt/site -r /tmp/req/ring-requirements.txt; \
    python -m venv --without-pip /opt/physim2-harness/venv; \
    pip --python /opt/physim2-harness/venv/bin/python install --no-cache-dir --no-compile --disable-pip-version-check \
        --require-hashes --only-binary :all: -r /tmp/req/harness-requirements.txt; \
    apt-get update -q && apt-get install -y -q --no-install-recommends binutils; \
    # size only: symbol tables and test trees are not needed at run time (jaxlib/libjax_common.so: 328 -> 237 MB)
    find /opt/site -name '*.so*' -type f -exec strip --strip-unneeded {} + ; \
    find /opt/site /opt/physim2-harness -type d \( -name tests -o -name __pycache__ \) -prune -exec rm -rf {} + ; \
    rm -rf /opt/site/bin

FROM python:3.12-slim
COPY --from=build /opt/site /usr/local/lib/python3.12/site-packages
COPY --from=build /opt/physim2-harness /opt/physim2-harness
COPY harness-uv /usr/local/bin/uv
# bytecode once, here: the predictor runs as an unprivileged user with -B and cannot cache it (import numpy: 0.40 -> 0.22 s),
# and a read-only root cannot cache the harness's either. Then prove, without network, that the harness's
# environment is complete and that the stand-in answers the two set-up commands for the program it was built for.
RUN set -e; chmod 755 /usr/local/bin/uv; \
    python -m compileall -q /usr/local/lib/python3.12/site-packages /opt/physim2-harness > /dev/null || true; \
    /opt/physim2-harness/venv/bin/python -B -c "import openai, mcp, httpx, httpx2, tenacity, certifi"; \
    printf '# /// script\n# requires-python = ">=3.10"\n# dependencies = ["openai", "mcp==2.0.0", "httpx", "httpx2", "tenacity", "certifi"]\n# ///\n' > /tmp/probe.py; \
    uv sync --script /tmp/probe.py -q --no-config; \
    test "$(uv python find --script /tmp/probe.py --no-config)" = /opt/physim2-harness/venv/bin/python; \
    rm -f /tmp/probe.py
ENV OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 JAX_PLATFORMS=cpu \
    XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
WORKDIR /workspace
