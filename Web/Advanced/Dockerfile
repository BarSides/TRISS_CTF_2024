FROM node:22-alpine AS initdb

WORKDIR /app
COPY package*.json /app
COPY init.js .
RUN npm install
CMD ["node", "init.js"]


FROM node:22-alpine

WORKDIR /app
COPY package*.json /app
COPY app.js .
COPY init.js .
RUN npm install
EXPOSE 8000
CMD ["node", "app.js"]
