# The daily compatibility run: both test suites against LumiBox production.
FROM node:24.21.0-trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
COPY python/requirements.txt python/
RUN python3 -m venv /venv && /venv/bin/pip install --no-cache-dir -r python/requirements.txt
COPY js/package.json js/package-lock.json js/
RUN cd js && npm ci --no-audit --no-fund
COPY . .
CMD ["compat/run.sh"]
