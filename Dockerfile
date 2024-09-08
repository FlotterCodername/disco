# Copyright © 2024 Fabian H. Schneider

# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file,
# You can obtain one at https://mozilla.org/MPL/2.0/.

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY poetry.lock pyproject.toml /app/

# Configure environment
ENV PATH="/root/.local/bin:$PATH"
ENV DISCO_IS_DOCKER=1

# Install linux dependencies and poetry
RUN apt update &&  \
    apt install -y curl &&  \
    rm -rf /var/lib/apt/lists/* &&  \
    (curl -sSL https://install.python-poetry.org | python3 -)

# Install the dependencies
RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    poetry install --sync --without=dev --no-root

# Copy the rest of the application code into the container
COPY . /app

# Install the application
RUN poetry install --sync --without=dev

# Set the default command to run the bot
CMD ["poetry", "run", "disco"]
