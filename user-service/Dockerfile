# Use a lightweight Python image for production
FROM python:3.12-slim

# Set the working directory
WORKDIR /microservice1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    protobuf-compiler \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

RUN dapr init --slim

# Copy only the necessary files to install dependencies
COPY pyproject.toml poetry.lock /microservice1/

# COPY entrypoint.sh /microservice1/entrypoint.sh

# RUN chmod +x /microservice1/entrypoint.sh

# Install poetry
RUN pip install poetry 

# Configure poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy the application code
COPY . /microservice1/

# Expose the port the application runs on
EXPOSE 8003

# Define the command to run the application
# ENTRYPOINT ["/microservice1/entrypoint.sh"]
CMD ["poetry", "run", "uvicorn", "service1.main:app", "--host", "0.0.0.0", "--port", "8003"]