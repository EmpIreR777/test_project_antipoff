from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.db.database import BaseModel
from app.core.config import settings
from app.db.models.models import Query, History
from app.auth.models import User, Role

config = context.config


sync_url = settings.get_database_url().replace('postgresql+asyncpg:', 'postgresql:')
config.set_main_option('sqlalchemy.url', sync_url)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Выполняйте миграцию в автономном режиме."""
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
    """Выполняйте миграцию в режиме онлайн."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()