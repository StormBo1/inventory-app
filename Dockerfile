# Dockerfile

FROM pypy:latest
WORKDIR /app
COPY . /app
CMD pypy inventory1.py