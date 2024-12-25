FROM node:20
WORKDIR /app

COPY package*.json ./
RUN npm install ${NPM_EXTRA_ARGS}

COPY . .
RUN VITE_API_BASE_URL='/api' npm run build
