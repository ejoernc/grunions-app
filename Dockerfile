FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATA_DIR=/data PORT=10000
# Slim images omit timezone data. Without it, the clock is UTC and tonight's practice disappears at 5pm Pacific.
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && rm -rf /var/lib/apt/lists/*
ENV TZ=America/Los_Angeles
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Every runtime module. A named list left lineupfeed.py and sports.py out of the image.
COPY *.py ./
COPY static ./static
RUN mkdir -p /data
EXPOSE 10000
# 1 worker + threads: SQLite on a single disk; chat polling is light.
CMD gunicorn app:app --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 60
