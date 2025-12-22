FROM oven/bun:1.2-alpine AS builder

WORKDIR /app

# Copy workspace configuration
# Note: Build from monorepo root with: docker build -f apps/service/Dockerfile -t service .
COPY package.json bun.lock ./
COPY apps/service/package.json ./apps/service/
COPY common/db/package.json ./common/db/
COPY common/rabbit/package.json ./common/rabbit/
COPY common/bucket/package.json ./common/bucket/

# Install dependencies
RUN bun install

# Copy source code
COPY apps/service ./apps/service
COPY common ./common

# Build the service
WORKDIR /app/apps/service
RUN bun run build

# Production stage
FROM alpine:3.20

WORKDIR /app

# Install necessary runtime dependencies
RUN apk add --no-cache libstdc++ libgcc

# Copy the compiled binary
COPY --from=builder /app/apps/service/dist/service ./service

# Expose port
EXPOSE 3000

# Run the service
CMD ["./service"]
