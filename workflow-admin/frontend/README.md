# Frontend - Workflow Admin

React + TypeScript + Vite + Material-UI frontend for the Workflow Admin system.

## Stage 1: Foundation Proof ✅

### Tech Stack
- **React 18** with TypeScript
- **Vite** for fast development and building  
- **Material-UI (MUI)** for component library
- **Axios** for API integration
- **Docker** containerization with nginx
- **External browser access** on port 3000

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   └── HealthCheck.tsx    # API connectivity test component
│   ├── api/
│   │   └── client.ts          # Axios setup and API types
│   ├── theme/
│   │   └── index.ts           # Material-UI theme configuration
│   ├── App.tsx                # Main application component
│   └── main.tsx               # Entry point
├── public/
├── Dockerfile                 # Multi-stage build (Node + Nginx)
├── nginx.conf                 # Production server config with API proxy
├── docker-compose.yml         # Integration with backend services
└── package.json               # Dependencies and scripts
```

### Development Commands

```bash
# Install dependencies
npm install

# Development server (with backend proxy)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

### Docker Commands

```bash
# Build frontend container
docker-compose build frontend

# Run frontend only (requires backend to be running)
docker-compose --profile frontend up

# Run full stack (backend + frontend)
docker-compose --profile full up

# Development with live reload
docker-compose --profile full up --build
```

### API Integration

The frontend connects to the backend through:
- **Development**: Vite proxy configuration (`/api` → `http://backend:8000/api`)
- **Production**: Nginx proxy configuration in container

### Browser Access

- **Development**: http://localhost:3000
- **Production**: http://localhost:3000 (external browser access enabled)

### Stage 1 Components

#### HealthCheck Component
- Tests backend API connectivity
- Displays system status and database health
- Shows API information and available features
- Error handling for connection failures

#### App Component  
- Material-UI theming and layout
- Welcome section with stage information
- System status section
- Development progress tracking

### Success Criteria for Stage 1
- ✅ React app structure created
- ✅ Material-UI integration complete
- ✅ API client with TypeScript types
- ✅ Docker configuration ready
- ✅ External browser access configured
- ⏳ Build and deployment testing
- ⏳ End-to-end connectivity verification

### Next: Stage 2
Once Stage 1 is verified, Stage 2 will add:
- Projects list view
- Agents management interface  
- Teams overview
- Basic CRUD operations

---
*Stage 1 Status: Implementation Complete - Testing Phase*