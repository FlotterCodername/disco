#!/bin/bash
# Copyright © 2024 David Siegl
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/.
# Function to display usage instructions
usage() {
  echo "Usage: $0 -s SERVICE_NAME [-c]"
  echo "  -s: Name of the Docker service to remove"
  echo "  -c: Optional flag to clean up unused containers, images, volumes, and networks"
  exit 1
}

CLEAN_UP=false

# Parse command line arguments
while getopts "s:c" opt; do
  case $opt in
    s) SERVICE_NAME=$OPTARG ;;
    c) CLEAN_UP=true ;;
    *) usage ;;
  esac
done

if [ -z "$SERVICE_NAME" ]; then
  usage
fi

# Check if Docker is running
if ! systemctl is-active --quiet docker; then
  echo "Docker is not running. Please start Docker before running this script."
  exit 1
fi

echo "Stopping and removing the Docker service: $SERVICE_NAME"
if docker service rm "$SERVICE_NAME"; then
  echo "Docker service $SERVICE_NAME removed successfully."
else
  echo "Failed to remove Docker service $SERVICE_NAME. It might not exist."
  exit 1
fi

if [ "$CLEAN_UP" = true ]; then
  echo "Cleaning up unused Docker resources..."

  # Remove unused containers
  echo "Removing unused containers..."
  docker container prune -f

  # Remove unused images
  echo "Removing unused images..."
  docker image prune -f

  # Remove unused volumes
  echo "Removing unused volumes..."
  docker volume prune -f

  # Remove unused networks
  echo "Removing unused networks..."
  docker network prune -f

  echo "Cleanup completed."
fi

exit 0
