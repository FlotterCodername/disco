# Disco!

[![License](https://img.shields.io/github/license/FlotterCodername/disco)](https://github.com/FlotterCodername/disco/blob/main/LICENSE.txt)
[![Python Version](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/disco-automate/badge/?version=latest)](https://disco-automate.readthedocs.io/en/latest/?badge=latest)
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

Prepare a host directory for the container to store its data, e.g. at `/opt/disco/`:

```
opt/
  disco/
    log/
      disco.log  # Automatically created
    run/
      secrets.toml
    sqlite/
      db.sqlite3  # Automatically created
```

In this directory, the only thing you need to provide ahead of time is your *Discord App secret*. Store this in
`secrets.toml`:

```toml
[disco]
token = "YOUR_TOKEN_HERE"
```

Run the container while mounting the host directory at `/opt/disco/`:

```bash
docker run --volume /opt/disco/:/opt/disco/ ghcr.io/flottercodername/disco
```
