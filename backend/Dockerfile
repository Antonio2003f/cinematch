# ---- Stage 1: builder ----
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# TARGETARCH e populat automat de Docker/buildx: "amd64" pe PC-uri x86,
# "arm64" pe masini ARM (ex. Oracle Cloud Ampere, Apple Silicon).
ARG TARGETARCH

# Pe amd64: torch se ia de pe indexul CPU-only al PyTorch, ca sa NU
# traga dependintele CUDA/GPU (peste 1.5GB inutile fara placa video).
# Pe arm64: acel index nu publica wheel-uri deloc - dar nu conteaza,
# pentru ca PyPI-ul normal ofera deja pe ARM un build CPU-only implicit
# (NVIDIA/CUDA nu exista pe arhitectura asta), deci instalam normal.
RUN if [ "$TARGETARCH" = "amd64" ]; then \
    pip install --user --no-cache-dir torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu; \
    else \
    pip install --user --no-cache-dir torch==2.4.1; \
    fi

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
