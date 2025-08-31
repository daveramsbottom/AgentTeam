#!/usr/bin/env python3
"""
Simple mock API server for testing Newman setup
This will be replaced by FastAPI later
"""

from flask import Flask, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import get_database_info, check_database_connection

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    try:
        db_status = check_database_connection()
        return jsonify({
            "status": "healthy" if db_status else "unhealthy",
            "database": {
                "local_connection_ok": db_status
            },
            "message": "Mock API server is running"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/v1/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        "version": "1.0.0",
        "description": "Workflow Admin API - Mock Version",
        "database_connected": check_database_connection(),
        "endpoints": [
            "GET /health",
            "GET /api/v1/info", 
            "GET /api/v1/database/status"
        ]
    })

@app.route('/api/v1/database/status', methods=['GET'])
def database_status():
    """Database status and table information"""
    try:
        db_info = get_database_info()
        return jsonify(db_info), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to get database status",
            "details": str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "message": "Workflow Admin Mock API",
        "version": "1.0.0",
        "health_check": "/health",
        "api_info": "/api/v1/info"
    })

if __name__ == '__main__':
    print("🚀 Starting Mock API Server...")
    print("📊 Database connection:", "✅" if check_database_connection() else "❌")
    app.run(host='0.0.0.0', port=8000, debug=True)