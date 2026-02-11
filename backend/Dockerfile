# Используем Python 3.11 (или твою версию)
FROM python:3.11-slim

# Настраиваем переменные окружения для Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Добавляем Poetry в PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Устанавливаем системные зависимости (curl нужен для установки Poetry)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Сначала копируем только файлы зависимостей (для кэширования слоев Docker)
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без dev-пакетов)
RUN poetry install --only main --no-root

# Теперь копируем весь остальной код приложения
COPY . .

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]