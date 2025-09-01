# Docker Build Issues & Solutions

## Issues Identified

### 1. **npm ci vs npm install**
- **Problem**: `npm ci --only=production` fails because we need dev dependencies for building
- **Fix**: Use `npm install` instead of `npm ci` when no `package-lock.json` exists

### 2. **Missing Dependencies**
- **Problem**: Build process requires dev dependencies (TypeScript, Vite, etc.)
- **Fix**: Install all dependencies, not just production ones

### 3. **Health Check Dependencies**
- **Problem**: nginx:alpine doesn't include curl for health checks
- **Fix**: Add `RUN apk add --no-cache curl`

### 4. **Build Performance**
- **Problem**: npm install takes 5+ minutes in Docker
- **Fix**: Create development dockerfile with hot reload instead

## Current Dockerfile Status

### ✅ Fixed Issues:
- Changed `npm ci --only=production` to `npm install`  
- Added curl installation for health checks
- Added proper .dockerignore
- Added missing TypeScript definitions

### ⏳ Remaining Challenge:
- **Long Build Times**: npm install takes 5+ minutes
- **Solution**: Use development dockerfile for testing

## Quick Test Commands

### Development Mode (Recommended for Stage 1):
```bash
# Use development dockerfile
docker-compose -f docker-compose.frontend-dev.yml up --build

# Should be accessible at http://localhost:3000
```

### Production Mode (When build completes):
```bash
# Use production dockerfile  
docker-compose --profile frontend up --build
```

## Stage 1 Verification

Since our goal is to prove the stack works, we can:

1. **Use development mode** to verify React + API connectivity
2. **Optimize production build** in later stages
3. **Focus on functionality** over build performance for now

The frontend code is complete and ready - the Docker optimization is a deployment detail we can refine.

---
*Status: Core functionality ready, Docker build optimization in progress*