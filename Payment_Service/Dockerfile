FROM python:3.12

WORKDIR /microservice6

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry 

COPY . /microservice6/

RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8008

CMD ["poetry", "run", "uvicorn", "service6.main:app", "--host", "0.0.0.0", "--reload"]