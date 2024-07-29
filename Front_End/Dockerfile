# Stage 1: Build the Angular application
FROM node:18 AS nodejs

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm install -g @angular/cli
RUN ng build --configuration production

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=nodejs /app/dist/Front_End /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
