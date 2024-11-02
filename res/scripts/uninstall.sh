#!/bin/bash
# Copyright © 2024 David Siegl
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/.


remove_docker_service() {

  sudo systemctl stop disco.service
  sudo systemctl disable disco.service
  sudo rm /etc/systemd/system/disco.service
  sudo systemctl daemon-reload

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

}


# Check if Docker is running
if ! systemctl is-active --quiet docker; then
  echo "Docker is not running. Please start Docker before running this script."
  exit 1
fi


if remove_docker_service; then
  echo "Disco Docker container service has been removed."
else
  echo "Failed to remove Disco Docker container service."
  exit 1
fi

exit 0
