# Dockerfile
# ── Stage 1: Builder ──
FROM python:3.12-slim AS builder

# Установить uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Сначала копируем только файлы зависимостей (кэширование Docker-слоёв)
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости без самого проекта
RUN uv sync --frozen --no-cache --no-install-project --no-dev

# Копируем весь проект
COPY . .

# Устанавливаем проект
RUN uv sync --frozen --no-cache --no-dev


# ── Stage 2: Runtime ──
FROM python:3.12-slim

WORKDIR /app

# Копируем uv из builder
COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /bin/uvx /bin/uvx

# Копируем виртуальное окружение и исходники из builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
# НОВОЕ ДЛЯ КРАСИВОГО ЧАТА
COPY --from=builder /app/src/api/static/ /app/src/api/static/                       

# Переменные окружения
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8001

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]