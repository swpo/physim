# PhySim-v2 exam image (CPU): the pinned scientific stack of the vw library. Used for the lab/grader container
# and as the base of the agent container. NOT BUILT OR RUN in the cloud container that wrote it (no Docker daemon).
FROM python:3.12-slim
RUN pip install --no-cache-dir numpy==2.5.4 scipy==1.18.1 jax==0.12.0.1 jaxlib==0.12.0.1
# util-linux in the base image provides prlimit, setpriv and unshare (evaluator/sandbox.py uses what is available).
ENV OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 JAX_PLATFORMS=cpu
WORKDIR /workspace
