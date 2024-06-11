FROM python:3.12

WORKDIR /microservice1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN pip instal poetry 

COPY . /microservice1/

RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8002

CMD ["poetry", "run", "uvicorn", "service1.main:app", "--host", "0.0.0.0", "--reload"]