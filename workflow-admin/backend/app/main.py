"""
FastAPI application for Workflow Admin
Multi-agent workflow management system
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from .database.database import get_db, get_database_info, check_database_connection
from .database.models import Base
from .routers import projects, agents, teams, workflows

# Create FastAPI app
app = FastAPI(
    title="Workflow Admin API",
    description="Multi-agent workflow management system with AI integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(agents.router)
app.include_router(teams.router)
app.include_router(workflows.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for container and load balancer monitoring"""
    try:
        db_status = check_database_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": {
                "local_connection_ok": db_status
            },
            "service": "workflow-admin-api",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities"""
    return {
        "name": "Workflow Admin API",
        "version": "1.0.0",
        "description": "Multi-agent workflow management system",
        "features": [
            "Agent management and assignment",
            "Workflow creation and execution",
            "Team collaboration",
            "Performance analytics",
            "Hybrid database support"
        ],
        "database_connected": check_database_connection(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "database_status": "/api/v1/database/status",
            "projects": "/api/v1/projects",
            "agents": "/api/v1/agents",
            "teams": "/api/v1/teams",
            "workflows": "/api/v1/workflows"
        }
    }

# Database status endpoint
@app.get("/api/v1/database/status")
async def database_status():
    """Database connectivity and schema information"""
    try:
        return get_database_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database status check failed: {str(e)}")

# Version endpoint
@app.get("/api/v1/version")
async def get_version():
    """Get application version information"""
    from datetime import datetime
    return {
        "version": "1.0.0",
        "buildDate": datetime.now().strftime("%Y-%m-%d"),
        "service": "workflow-admin-api"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic API information"""
    return {
        "message": "Welcome to Workflow Admin API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "api_info": "/api/v1/info"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)