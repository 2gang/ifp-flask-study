FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk update && \
    apk add \
            nginx \
            build-base \
            linux-headers 

RUN pip3 install --upgrade pip && \
    pip install -r requirements/common.txt && pip install -r requirements/prod.txt \
    && pip install -r requirements/dev.txt

RUN chmod +x /app/deploy/entrypoint.sh
ENTRYPOINT [ "/app/deploy/entrypoint.sh" ]