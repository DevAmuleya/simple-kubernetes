# ---------- BUILD STAGE ----------
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---------- RUNTIME STAGE ----------
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY app/ ./app/

ENV PATH=/root/.local/bin:$PATH
ENV APP_VERSION=1.0

EXPOSE 8000

RUN useradd -m appuser
USER appuser

CMD ["python", "app/main.py"]