#!/bin/bash

usage() {
  echo "Usage: $0 -s <service_name> -i <image_name> -p <host_port>:<container_port> -r <replicas> [-e ENV_VAR=value]..."
  exit 1
}


# Parse command line arguments
while getopts "s:i:p:r:e:" opt; do
  case $opt in
    s) SERVICE_NAME=$OPTARG ;;
    i) IMAGE_NAME=$OPTARG ;;
    p) PORT_MAPPING=$OPTARG ;;
    r) REPLICAS=$OPTARG ;;
    *) usage ;;
  esac
done

if [ -z "$SERVICE_NAME" ] || [ -z "$IMAGE_NAME" ] || [ -z "$PORT_MAPPING" ] || [ -z "$REPLICAS" ]; then
  usage
fi

# Check if Docker is running
if ! systemctl is-active --quiet docker; then
  echo "Docker is not running. Please start Docker and try again."
  exit 1
fi

if ! docker info | grep -q "Swarm: active"; then
  echo "Initializing Docker Swarm..."
  docker swarm init
fi

echo "Creating Docker service: $SERVICE_NAME from image: $IMAGE_NAME"
docker service create --name "$SERVICE_NAME" \
  -p "$PORT_MAPPING" \
  --replicas "$REPLICAS" \
  "$IMAGE_NAME"

if [ $? -eq 0 ]; then
  echo "Docker service $SERVICE_NAME created successfully."
else
  echo "Failed to create Docker service $SERVICE_NAME."
  exit 1
fi

exit 0
