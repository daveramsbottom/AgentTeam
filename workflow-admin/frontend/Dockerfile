# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json ./

# Install all dependencies (including dev dependencies for build)
RUN npm install --silent

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 3000 (instead of default 80)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]