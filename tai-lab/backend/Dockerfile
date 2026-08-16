# Hugging Face Spaces serves on port 7860 by default for Docker SDK spaces.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY backend/pyproject.toml ./pyproject.toml
RUN pip install --upgrade pip && pip install .

COPY backend/app ./app

# The BoK is mounted alongside the backend so the Docker build context must
# include both. CI copies the trustworthy-ai repo root into /app/bok.
COPY README.md /app/bok/README.md
COPY pages /app/bok/pages
COPY code /app/bok/code

ENV BOK_ROOT=/app/bok \
    CORS_ORIGINS=https://*.vercel.app

EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
