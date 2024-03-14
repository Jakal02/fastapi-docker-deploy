#!/usr/bin/bash

set -e

echo "Building Docker image."

docker build . -t fastapi-backend:latest
