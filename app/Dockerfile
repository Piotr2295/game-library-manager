FROM python:3.12.1-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Load environment variables from .env during build
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Install uvicorn
RUN pip install uvicorn

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
