FROM python:3.6-alpine

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

RUN apk add --no-cache gcc g++ libffi-dev libressl-dev musl-dev python3-dev openssl-dev cargo ffmpeg
RUN pip install pipenv

COPY . /app

WORKDIR /app

RUN pipenv install --deploy --system --ignore-pipfile

CMD ["python", "main.py"] 