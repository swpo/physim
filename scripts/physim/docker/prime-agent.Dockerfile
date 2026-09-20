# Build context: the verified, extracted official v0.9.5 Linux release.
FROM physim-agent:0.12.2
USER root
COPY . /opt/prime-agent/
RUN PIP_NO_INDEX=0 pip install --no-cache-dir /opt/prime-agent/prime-agent-runtime \
    dill requests httpx pyyaml tomli python-dotenv pandas beautifulsoup4 lxml && \
    ln -s /opt/prime-agent/prime-agent /usr/local/bin/prime-agent && \
    prime-agent --version && \
    pip freeze > /opt/prime-agent/python-lock.txt
ENV PRIME_AGENT_KERNEL_PYTHON=/usr/local/bin/python PI_OFFLINE=1 PI_TELEMETRY=0
WORKDIR /workspace
