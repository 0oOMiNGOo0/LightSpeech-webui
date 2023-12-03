FROM node:18-alpine

COPY ./frontend /app
WORKDIR /app

RUN npm install
RUN npm run build

EXPOSE 3000

ENTRYPOINT ["npm", "start"]