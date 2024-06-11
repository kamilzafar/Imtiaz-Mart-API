FROM python:3.12

WORKDIR /service1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false

RUN pip instal poetry 

COPY . /service1/

RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "service.main:app", "--host", "0.0.0.0", "--reload"]