# Stage 1: Build the application
FROM node:alpine3.18 AS builder

RUN apk add --no-cache git openssh

WORKDIR /app
ENV NODE_ENV=production PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Clone the repository without checking for the latest tag
RUN git clone https://github.com/wppconnect-team/wppconnect-server.git /tmp/repo && \
    cp -r /tmp/repo/* .

COPY package*.json ./

# Use --legacy-peer-deps to resolve dependency conflicts
RUN npm install --only=production --legacy-peer-deps

# Stage 2: Run the application
FROM cgr.dev/chainguard/node:latest

WORKDIR /app
ENV NODE_ENV=production PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Copy the built app from the previous stage
COPY --from=builder /app /app

# Set the correct entry point
ENTRYPOINT ["yarn", "start"]
