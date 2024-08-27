# Use a lightweight Python image for production
FROM python:3.12-slim

# Set the working directory
WORKDIR /microservice3

# Install dependencies
RUN apt-get update && apt-get install -y \
build-essential \
protobuf-compiler \
wget \
libpq-dev \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the environment variable for dapr
# ENV PATH="/root/.dapr/bin:${PATH}"

# Install dapr
# RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Initialize dapr
# RUN dapr init --slim

# Verify dapr installation
# RUN which dapr

# Copy only the necessary files to install dependencies
COPY pyproject.toml poetry.lock /microservice3/

# Install poetry
RUN pip install poetry 

# Configure poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy the application code
COPY . /microservice3/

# COPY ./components /dapr/components

# Expose the port the application runs on
EXPOSE 8005

# Define the command to run the application
# CMD ["dapr", "run", "--app-id", "order-service", "--app-port", "3005", "--dapr-http-port", "3501", "--resources-path", "./components", "--", "poetry", "run", "uvicorn", "service3.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]
CMD ["poetry", "run", "uvicorn", "service3.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]