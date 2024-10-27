#!/bin/bash
# Copyright © 2024 David Siegl
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/.


create_docker_service() {

  # Create the systemd service file for the Disco Docker container
  sudo tee /etc/systemd/system/disco.service > /dev/null <<EOF
[Unit]
Description=Disco Docker Container Service
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --rm --name disco-container --volume /opt/disco/:/opt/disco/ ghcr.io/flottercodername/disco
ExecStop=/usr/bin/docker stop disco-container

[Install]
WantedBy=multi-user.target
EOF
  
  # Reload systemd to apply the new service
  sudo systemctl daemon-reload
  
  # Enable and start the service
  sudo systemctl enable disco.service
  sudo systemctl start disco.service

}


# Check if Docker is running
if ! systemctl is-active --quiet docker; then
  echo "Docker is not running. Please start Docker and try again."
  exit 1
fi

# Pull the latest Docker image
sudo docker pull ghcr.io/flottercodername/disco


if create_docker_service; then
  echo "Disco Docker container service installed and started."
else
  echo "Failed to install Disco Docker container service."
  exit 1
fi

exit 0
