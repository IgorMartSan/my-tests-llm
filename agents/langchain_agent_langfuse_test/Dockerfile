# ==========================================
# STAGE 1 - BUILD
# ==========================================

FROM python:3.13-slim AS builder

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/

WORKDIR /app

# Configurações
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_PYTHON_DOWNLOADS=0

# Copia somente as dependências
COPY pyproject.toml uv.lock ./

# Instala dependências com cache
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Copia a aplicação
COPY . .

# Instala o projeto
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable


# ==========================================
# STAGE 2 - RUNTIME
# ==========================================

FROM python:3.13-slim

WORKDIR /app

# Configurações do Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Copia ambiente virtual e código
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# Cria usuário sem privilégios
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

USER appuser

# Executa o agente
CMD ["python", "-m", "src.main"]