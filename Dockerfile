FROM python:3.11.7-alpine

RUN apk add --update --no-cache \
    nodejs \
    npm \
    mariadb-dev \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    pkgconfig

RUN npm install pm2 -g

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["pm2-runtime", "start", "/app/ecosystem.config.js"]