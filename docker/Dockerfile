FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/usr/local/bin:/usr/bin:/bin"

# Install dependencies from uv.lock
COPY pyproject.toml uv.lock ./
RUN uv sync

# Copy project
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "\
    uv run python manage.py migrate --noinput && \
    uv run python manage.py collectstatic --noinput && \
    uv run gunicorn --bind 0.0.0.0:8000 bank_CFNOB_norm.wsgi:application"]
