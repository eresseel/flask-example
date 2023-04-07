FROM python:3.11.2-alpine3.17

WORKDIR /app

COPY templates/ ./templates/
COPY app.py	.
COPY requirements.txt .
COPY .env .
COPY .git/ .git/

RUN apk update && \
    apk add git && \
    pip install -r requirements.txt && \
    pip install waitress==2.1.2

EXPOSE 8080

CMD ["/usr/local/bin/waitress-serve", "--host=0.0.0.0", "app:app"]