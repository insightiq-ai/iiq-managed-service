# Pull base image
FROM python:3.9.2-slim-buster
WORKDIR /iiq-managed-service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install pipenv==2023.6.26
COPY Pipfile Pipfile.lock /iiq-managed-service/
RUN pipenv install --system --deploy && pipenv --clear
COPY app /iiq-managed-service/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
