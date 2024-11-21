FROM node:20
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN VITE_API_BASE_URL='/api' npm run build
