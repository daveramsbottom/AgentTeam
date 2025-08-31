"""
Database connection and session management

Handles both SQLite (local) and PostgreSQL (optional cloud) connections
with environment-based configuration switching.
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from typing import Generator, Optional
import logging

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/local/workflow-admin.db")
CLOUD_DATABASE_URL = os.getenv("CLOUD_DATABASE_URL", "")

# SQLite specific settings
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # Ensure directory exists for SQLite
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
else:
    connect_args = {}

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Optional cloud engine for sync
cloud_engine = None
CloudSessionLocal = None

if CLOUD_DATABASE_URL:
    try:
        cloud_engine = create_engine(
            CLOUD_DATABASE_URL,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
        CloudSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cloud_engine)
        logger.info("Cloud database connection configured")
    except Exception as e:
        logger.warning(f"Cloud database connection failed: {e}")


def get_db() -> Generator[Session, None, None]:
    """
    Get database session
    Used as dependency in FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cloud_db() -> Generator[Optional[Session], None, None]:
    """
    Get cloud database session (if available)
    Used for optional cloud sync operations
    """
    if CloudSessionLocal is None:
        yield None
        return
    
    db = CloudSessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session as context manager
    For use outside FastAPI (testing, scripts, etc.)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_cloud_db_session() -> Generator[Optional[Session], None, None]:
    """
    Get cloud database session as context manager
    Returns None if cloud database not configured
    """
    if CloudSessionLocal is None:
        yield None
        return
    
    db = CloudSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all tables in the database
    Used for initial setup and testing
    """
    from .models import Base
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Local database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create local database tables: {e}")
        raise
    
    # Optionally create cloud tables
    if cloud_engine:
        try:
            Base.metadata.create_all(bind=cloud_engine)
            logger.info("Cloud database tables created successfully")
        except Exception as e:
            logger.warning(f"Failed to create cloud database tables: {e}")


def drop_tables():
    """
    Drop all tables in the database
    Used for testing and cleanup
    """
    from .models import Base
    
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Local database tables dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop local database tables: {e}")
        raise
    
    # Optionally drop cloud tables
    if cloud_engine:
        try:
            Base.metadata.drop_all(bind=cloud_engine)
            logger.info("Cloud database tables dropped successfully")
        except Exception as e:
            logger.warning(f"Failed to drop cloud database tables: {e}")


def reset_database():
    """
    Reset database by dropping and recreating all tables
    Used for testing and development
    """
    logger.info("Resetting database...")
    drop_tables()
    create_tables()
    logger.info("Database reset complete")


def check_database_connection() -> bool:
    """
    Test database connection
    Returns True if connection successful
    """
    try:
        with get_db_session() as db:
            # Simple query to test connection
            db.execute(text("SELECT 1"))
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


def check_cloud_database_connection() -> bool:
    """
    Test cloud database connection
    Returns True if connection successful, False if no cloud DB configured
    """
    if not cloud_engine:
        logger.info("No cloud database configured")
        return False
    
    try:
        with get_cloud_db_session() as db:
            if db is None:
                return False
            # Simple query to test connection
            db.execute(text("SELECT 1"))
        logger.info("Cloud database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Cloud database connection test failed: {e}")
        return False


def get_database_info() -> dict:
    """
    Get database information for diagnostics
    """
    return {
        "local_database_url": DATABASE_URL,
        "cloud_database_configured": cloud_engine is not None,
        "local_connection_ok": check_database_connection(),
        "cloud_connection_ok": check_cloud_database_connection(),
        "engine_info": {
            "dialect": str(engine.dialect.name),
            "driver": str(engine.dialect.driver)
        }
    }


# Database health check functions
class DatabaseHealth:
    """Database health monitoring utilities"""
    
    @staticmethod
    def ping_local() -> bool:
        """Quick ping to local database"""
        return check_database_connection()
    
    @staticmethod
    def ping_cloud() -> bool:
        """Quick ping to cloud database"""
        return check_cloud_database_connection()
    
    @staticmethod
    def get_status() -> dict:
        """Get comprehensive database status"""
        return {
            "local": {
                "url": DATABASE_URL,
                "connected": DatabaseHealth.ping_local()
            },
            "cloud": {
                "configured": cloud_engine is not None,
                "connected": DatabaseHealth.ping_cloud() if cloud_engine else False
            }
        }


# Initialize database on module import (optional)
if os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true":
    create_tables()