# Build Front_End
FROM node:16 as frontend-build
WORKDIR /app/Front_End
COPY Front_End/package*.json ./
RUN npm install
COPY Front_End/ ./
RUN npm run build --configuration production --aot

# Build Back_End
FROM python:3.10 as backend-build
WORKDIR /app/Back_End
COPY Back_End/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY Back_End/ ./

# Stage 3: Create final image
FROM python:3.10

# Copy backend code
WORKDIR /app/Back_End
COPY --from=backend-build /app/Back_End /app/Back_End

# Copy built Angular frontend
WORKDIR /app/Front_End
COPY --from=frontend-build /app/Front_End/dist /app/Front_End/dist

# Install a simple HTTP server to serve the Angular frontend
RUN npm install -g http-server

# Add a script to run both the HTTP server for Angular and the Bottle backend
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80
EXPOSE 8080

CMD ["/entrypoint.sh"]
