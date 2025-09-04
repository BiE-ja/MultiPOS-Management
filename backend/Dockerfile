FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

# Update system packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean
# crée le dossier de travail
WORKDIR /app/

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app


# Copie les fichiers nécessaires dans le dossier de travail
COPY ./scripts /app/scripts

COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

COPY ./README.md /app/README.md

COPY ./app /app/app  

# Sync the project
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#inter   
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD [ "fastapi", "run", "--workers", "4", "app/main.py"]
# --reload must be used only in development, not in production
# --workers is set to 4 for better performance in production


