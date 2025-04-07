FROM python:3.12-slim

# avoid interactive prompts during Docker build
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* README.md /
COPY /app/__init__.py /app/

RUN poetry install --no-interaction

COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "python", "run.py"]
