# Stage 1: Build stage
FROM node:14-alpine as builder

WORKDIR /app

COPY package*.json ./

RUN npm install

# Stage 2: Final stage
FROM grafana/k6

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Expose the necessary ports
EXPOSE 3000

CMD ["npm", "start"]
