# copied from: 

# Dependency Pre-stage
FROM python:3.10-slim-bullseye as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Main App Setup
FROM python:3.10-slim-bullseye

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./alembic.ini /code/

COPY ./prestart.sh /code/

COPY ./start.sh /code/

EXPOSE 8080

ENV PYTHONPATH=/code

CMD ["./start.sh"]
