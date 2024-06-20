import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from dotenv import load_dotenv

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить строку подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Конфигурация Alembic
config = context.config

# Настройка SQLAlchemy URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Интерпретировать файл конфигурации для логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импорт моделей для автогенерации
from app.models import Base
target_metadata = Base.metadata

def run_migrations_offline():
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

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
