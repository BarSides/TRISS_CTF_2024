FROM node:22-alpine AS initdb

WORKDIR /app/
COPY package*.json /app/
COPY init.js /app/

RUN npm install
CMD ["node", "init.js"]

WORKDIR /app/
COPY package*.json /app/
COPY app.js /app/
COPY init.js /app/

FROM node:22-alpine

WORKDIR /app
COPY package*.json /app
COPY app.js .
COPY init.js .
RUN npm install && npm install -g pm2
EXPOSE 8000
CMD ["pm2", "start", "app.js", "--attach"]
