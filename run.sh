#!/bin/sh
# Starts the app on :5055 using settings from .env.local (BOT_API_KEY, SECRET_KEY, ADMIN_EMAIL, optional VERIFY_WEBHOOK_URL)
cd "$(dirname "$0")" && set -a && . ./.env.local && set +a && exec .venv/bin/python app.py
