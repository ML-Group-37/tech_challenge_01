#!/bin/bash
CONTAINER_NAME=$1

# Stop, rebuild, and restart the target container
docker compose -f /path/to/your/docker-compose.yml stop $CONTAINER_NAME
docker compose -f /path/to/your/docker-compose.yml build $CONTAINER_NAME
docker compose -f /path/to/your/docker-compose.yml up -d $CONTAINER_NAME

echo "Container $CONTAINER_NAME updated successfully"