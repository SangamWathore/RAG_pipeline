FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_HTTP_TIMEOUT=300 \
    UV_HTTP_RETRIES=5

COPY requirements.txt .

RUN uv pip install --system -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/documents /app/vectorstore

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]