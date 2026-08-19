# ---- Stage 1: builder ----
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# torch e instalat separat, de pe index-ul CPU-only al PyTorch.
# Fara asta, pip trage automat dependintele CUDA/GPU (nvidia-cublas,
# nvidia-cudnn etc.) - peste 1.5GB inutile pentru un container fara GPU.
RUN pip install --user --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Stage 2: runtime ----
FROM python:3.11-slim

WORKDIR /app

RUN useradd --create-home appuser
COPY --from=builder /root/.local /home/appuser/.local

COPY app/ ./app/

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
