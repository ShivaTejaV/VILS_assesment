import os
import sys
from os import path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 1) Load .env into os.environ
from dotenv import load_dotenv
load_dotenv()  # reads .env in project root

# 2) Make sure “app” is importable
sys.path.insert(0, path.dirname(path.dirname(__file__)))

# 3) Import your app’s Base (and models) so metadata is registered
from app.database import Base
import app.models  # noqa: F401

# this is the Alembic Config object
config = context.config

# 4) Override the URL from alembic.ini with your .env setting,
#    escaping '%' so configparser treats it literally
db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("DB_URL not found in environment")
# double any '%' so ConfigParser won't interpret it
escaped_url = db_url.replace("%", "%%")
config.set_main_option("sqlalchemy.url", escaped_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 5) Point Alembic at your MetaData for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
