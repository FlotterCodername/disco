# Disco!

[![License](https://img.shields.io/github/license/FlotterCodername/disco)](https://github.com/FlotterCodername/disco/blob/main/LICENSE.txt)
[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/FlotterCodername/disco/main.svg)](https://results.pre-commit.ci/latest/github/FlotterCodername/disco/main)
[![📦🐳 Publish Docker](https://github.com/FlotterCodername/disco/actions/workflows/publish-docker.yml/badge.svg)](https://github.com/FlotterCodername/disco/actions/workflows/publish-docker.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<!--[![☝️🧐 pre-commit](https://github.com/FlotterCodername/disco/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/FlotterCodername/disco/actions/workflows/pre-commit.yml)-->

Discord automation stuff

## How to set it up?

Pull the docker image from the GitHub Container Registry:
```bash
docker pull ghcr.io/flottercodername/disco
```

Prepare your Discord App secret as JSON file for mounting, e.g. at `~/.disco/run/secrets.json`:
```json
{
  "org.flottercodername.disco": {
    "@@token": "YOUR_TOKEN_HERE"
  }
}
```

Run the container while mounting the secrets file at `/var/disco/run/secrets.json`:
```bash
docker run --volume ~/.disco/run/secrets.json:/var/disco/run/secrets.json ghcr.io/flottercodername/disco
```
