FROM node:15.12.0-alpine

WORKDIR /app/frontend_reactjs
COPY package.json ./
COPY yarn.lock ./

RUN yarn install
COPY . ./

EXPOSE 3000