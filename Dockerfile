# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source https://github.com/Heptagram-Bot/api

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# setup poetry
COPY pyproject.toml .
COPY poetry .
RUN pip3 install poetry
RUN poetry install

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Transfer source to image
COPY . .

# Run bot
CMD [ "python3", "-m" , "src" ]
