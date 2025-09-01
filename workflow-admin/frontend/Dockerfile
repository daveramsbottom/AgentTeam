# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package.json package-lock.json* ./

# Install dependencies using npm ci for faster, reproducible builds
RUN if [ -f package-lock.json ]; then npm ci --silent; else npm install --silent; fi

# Copy source code (after dependencies for better caching)
COPY . .

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

# Install curl for health checks in a single layer
RUN apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

# Copy nginx configuration first (for better layer caching)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application (this layer changes most frequently)
COPY --from=builder /app/dist /usr/share/nginx/html

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs && \
    chown -R nextjs:nodejs /usr/share/nginx/html

# Expose port 3000 (instead of default 80)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]