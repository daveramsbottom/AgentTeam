"""
Alembic environment configuration for workflow-admin migrations

Supports both SQLite (local) and PostgreSQL (cloud) databases
with automatic table creation and migration handling.
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path so we can import our models
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent.parent))

# Import our models
from app.database.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Override database URL from environment if provided
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # Enable batch mode for SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    
    # Get configuration
    configuration = config.get_section(config.config_ini_section)
    
    # Override with environment variables
    if os.getenv("DATABASE_URL"):
        configuration["sqlalchemy.url"] = os.getenv("DATABASE_URL")
    
    # Create engine
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    # Handle SQLite specific settings
    database_url = configuration.get("sqlalchemy.url", "")
    render_as_batch = database_url.startswith("sqlite")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=render_as_batch,  # Required for SQLite ALTER TABLE support
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare server defaults
        )

        with context.begin_transaction():
            context.run_migrations()


def run_cloud_migrations() -> None:
    """
    Run migrations on cloud database if configured
    This is used for hybrid sync setup
    """
    cloud_url = os.getenv("CLOUD_DATABASE_URL")
    if not cloud_url:
        print("No cloud database URL configured, skipping cloud migrations")
        return
    
    print(f"Running cloud migrations on: {cloud_url}")
    
    # Temporarily override the database URL
    original_url = config.get_main_option("sqlalchemy.url")
    config.set_main_option("sqlalchemy.url", cloud_url)
    
    try:
        # Create engine for cloud database
        configuration = config.get_section(config.config_ini_section)
        configuration["sqlalchemy.url"] = cloud_url
        
        connectable = engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=False,  # PostgreSQL doesn't need batch mode
                compare_type=True,
                compare_server_default=True,
            )

            with context.begin_transaction():
                context.run_migrations()
                
        print("Cloud migrations completed successfully")
                
    except Exception as e:
        print(f"Cloud migrations failed: {e}")
        raise
    finally:
        # Restore original URL
        config.set_main_option("sqlalchemy.url", original_url)


def ensure_data_directory() -> None:
    """
    Ensure data directory exists for SQLite database
    """
    database_url = config.get_main_option("sqlalchemy.url")
    if database_url and database_url.startswith("sqlite:///"):
        db_path = database_url.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created database directory: {db_dir}")


# Check if we should run cloud migrations
run_cloud = os.getenv("RUN_CLOUD_MIGRATIONS", "false").lower() == "true"

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Ensure data directory exists
    ensure_data_directory()
    
    # Run local migrations
    run_migrations_online()
    
    # Optionally run cloud migrations
    if run_cloud:
        run_cloud_migrations()