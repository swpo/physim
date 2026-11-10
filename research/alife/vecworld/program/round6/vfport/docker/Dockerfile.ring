# PhySim v2 ring exam: the ONE image of both boxes (agent box and verifier box; --env.id isolated-verifier boots
# the verifier from the solver's resolved image). CPU only. The public world module imports the vw library,
# which imports jax and scipy, so numpy alone is not enough (agentenv/physim2/world_ring.py:25-29).
#
#   docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/
# Behind a TLS-intercepting proxy: put its CA bundle in docker/extra-ca.crt (leave the file empty otherwise) and add
#   --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY
FROM python:3.12-slim AS build
ARG HTTPS_PROXY=""
COPY extra-ca.crt /tmp/extra-ca.crt
RUN set -e; if [ -s /tmp/extra-ca.crt ]; then export PIP_CERT=/tmp/extra-ca.crt; \
      sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources; \
      printf 'Acquire::https::Proxy "%s";\nAcquire::https::CaInfo "/tmp/extra-ca.crt";\n' "$HTTPS_PROXY" > /etc/apt/apt.conf.d/99proxy; fi; \
    export HTTPS_PROXY="$HTTPS_PROXY"; \
    pip install --no-cache-dir --no-compile --disable-pip-version-check --target /opt/site \
        numpy==2.5.4 scipy==1.18.1 jax==0.12.0.1 jaxlib==0.12.0.1; \
    apt-get update -q && apt-get install -y -q --no-install-recommends binutils; \
    # size only: symbol tables and test trees are not needed at run time (jaxlib/libjax_common.so: 328 -> 237 MB)
    find /opt/site -name '*.so*' -type f -exec strip --strip-unneeded {} + ; \
    find /opt/site -type d \( -name tests -o -name __pycache__ \) -prune -exec rm -rf {} + ; \
    rm -rf /opt/site/bin

FROM python:3.12-slim
COPY --from=build /opt/site /usr/local/lib/python3.12/site-packages
# bytecode once, here: the predictor runs as an unprivileged user with -B and cannot cache it (import numpy: 0.40 -> 0.22 s)
RUN python -m compileall -q /usr/local/lib/python3.12/site-packages > /dev/null || true
ENV OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 JAX_PLATFORMS=cpu \
    XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
WORKDIR /workspace
