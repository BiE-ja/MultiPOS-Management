#Dockerfile (frontend/DockerFile)
FROM node:24.3.0-alpine AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# Stage 2: Dev
FROM node:24.3.0-alpine AS dev-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

ENV VITE_API_URL=$VITE_API_URL

CMD ["npm", "run", "dev"]

# Stage 3: Production
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]