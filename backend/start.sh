#! /usr/bin/env sh
set -e

./prestart.sh

uvicorn app.main:app --host 0.0.0.0 --port 8080
