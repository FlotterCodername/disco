#!/bin/bash

usage() {
  echo "Usage: $0 -s SERVICE_NAME -i IMAGE_NAME -v VOLUME_PATH [-p HOST_PORT:CONTAINER_PORT] [-r REPLICAS]"
  exit 1
}


# Parse command line arguments
while getopts "s:i:v:p:r:" opt; do
  case $opt in
    s) SERVICE_NAME=$OPTARG ;;
    i) IMAGE_NAME=$OPTARG ;;
    v) VOLUME_PATH=$OPTARG ;;
    p) PORT_MAPPING=$OPTARG ;;
    r) REPLICAS=$OPTARG ;;
    *) usage ;;
  esac
done

if [ -z "$SERVICE_NAME" ] || [ -z "$IMAGE_NAME" ] || [ -z "$VOLUME_PATH" ]; then
  usage
fi

if [ -z "$REPLICAS" ]; then
  REPLICAS=1
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
if [ -z "$PORT_MAPPING" ]; then
  if docker service create --name "$SERVICE_NAME" \
          --mount type=volume,destination="$VOLUME_PATH" \
          --replicas "$REPLICAS" \
          "$IMAGE_NAME"; then
    echo "Docker service $SERVICE_NAME created successfully."
  else
    echo "Failed to create Docker service $SERVICE_NAME."
    exit 1
  fi
else
  if docker service create --name "$SERVICE_NAME" \
        --mount type=volume,destination="$VOLUME_PATH" \
        --replicas "$REPLICAS" \
        -p "$PORT_MAPPING" \
        "$IMAGE_NAME"; then
    echo "Docker service $SERVICE_NAME created successfully."
  else
    echo "Failed to create Docker service $SERVICE_NAME."
    exit 1
  fi
fi

exit 0
