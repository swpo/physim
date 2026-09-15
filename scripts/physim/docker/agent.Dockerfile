FROM physim-predictor:0.12.0
USER root
RUN pip install --no-cache-dir uv==0.8.22 && \
    mkdir -p /workspace /observations
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages
WORKDIR /workspace
