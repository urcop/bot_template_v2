FROM python:3.11-slim

WORKDIR /app/bot/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x scripts/entrypoint.sh