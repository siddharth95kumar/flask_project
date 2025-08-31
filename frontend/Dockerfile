# FROM mcr.microsoft.com/playwright/node:18-focal
FROM node:18-slim

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]

