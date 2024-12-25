FROM node:20
WORKDIR /app

COPY package*.json ./
ARG NPM_EXTRA_ARGS
RUN npm install ${NPM_EXTRA_ARGS}

COPY . .
RUN VITE_API_BASE_URL='/api' npm run build
