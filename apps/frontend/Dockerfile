FROM node:20.11.1-alpine
WORKDIR /usr/src/app
COPY . .
RUN npm install
CMD ["npm", "run", "dev", "--host", "0.0.0.0"]