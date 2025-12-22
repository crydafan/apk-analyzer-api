FROM oven/bun:1.2-alpine AS builder

WORKDIR /app

# Copy workspace configuration
# Note: Build from monorepo root with: docker build -f apps/agent/Dockerfile -t agent .
COPY package.json bun.lock ./
COPY apps/agent/package.json ./apps/agent/
COPY common/db/package.json ./common/db/
COPY common/rabbit/package.json ./common/rabbit/
COPY common/bucket/package.json ./common/bucket/

# Install dependencies
RUN bun install

# Copy source code
COPY apps/agent ./apps/agent
COPY common ./common

# Build the agent
WORKDIR /app/apps/agent
RUN bun run build

# Production stage
FROM alpine:3.20

WORKDIR /app

# Install necessary runtime dependencies
RUN apk add --no-cache libstdc++ libgcc

# Copy the compiled binary
COPY --from=builder /app/apps/agent/dist/agent ./agent

# Run the agent
CMD ["./agent"]
