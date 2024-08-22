#!/bin/sh

# Run Dapr
dapr run --app-id user-service \
         --app-port 8003 \
         --dapr-http-port 3500 \
         --components-path ./components \
         -- python /microservice1/service1/main.py

poetry run uvicorn service1.main:app --host 0.0.0.0 --port 8003