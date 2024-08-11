# Use a lightweight Python image for production
FROM python:3.12-slim

# Set the working directory
WORKDIR /microservice5

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
build-essential \
protobuf-compiler \
libpq-dev \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Copy only the necessary files to install dependencies
COPY pyproject.toml poetry.lock /microservice5/

# Install poetry
RUN pip install poetry 

# Configure poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy the application code
COPY . /microservice5/

# Expose the port the application runs on
EXPOSE 8007

# Define the command to run the application
CMD ["poetry", "run", "uvicorn", "service5.main:app", "--host", "0.0.0.0", "--port", "8007"]
