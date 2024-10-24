FROM node:16.20.2-alpine AS builder

RUN apk add --update --no-cache

WORKDIR /app
COPY api/package*.json ./

RUN if [ -f package-lock.json ]; then npm ci --production; else npm install --production; fi

COPY api/ .

RUN npm install ts-migrate && npm run build

FROM node:16.20.2-alpine AS final
RUN apk add --update --no-cache \
    python3 \
    py3-pip \
    python3-dev \
    mariadb-dev \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    pkgconfig \
    curl

RUN npm install pm2 -g

WORKDIR /app
COPY . .

RUN rm -rf /app/api

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/package*.json /app
COPY --from=builder /app/.tmp /app/.tmp

RUN npm ci --production

CMD ["pm2-runtime", "start", "/app/ecosystem.config.js"]
