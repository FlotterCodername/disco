docker pull ghcr.io/flottercodername/disco && \
docker run --env DISCO_IS_DEBUG=1 --volume ~/.disco/run/secrets.json:/var/disco/run/secrets.json ghcr.io/flottercodername/disco
