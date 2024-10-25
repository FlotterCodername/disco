#!/bin/bash
# Ensure this script uses bash instead of sh

# Pull the latest Docker image
sudo docker pull ghcr.io/flottercodername/disco

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

echo "Disco Docker container service installed and started."
