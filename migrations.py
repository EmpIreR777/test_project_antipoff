import logging
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import DisconnectionError
from app.core.config import settings
import time


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_migrations_with_retry(max_attempts=3, delay=4):
    'Запускает миграции с повторными попытками при ошибках подключения'
    attempt = 0
    while attempt < max_attempts:
        try:
            run_migrations()
            return
        except DisconnectionError as e:
            attempt += 1
            if attempt == max_attempts:
                logger.error(f'Failed after {max_attempts} attempts: {e}')
                raise
            logger.warning(f'Connection error (attempt {attempt}/{max_attempts}): {e}')
            time.sleep(delay)


def run_migrations():
    sync_url = settings.get_database_url().replace('postgresql+asyncpg:', 'postgresql:')
    engine = create_engine(sync_url)

    try:
        # Проверяем подключение
        check_connection(engine)

        # Запускаем миграции
        alembic_cfg = Config()
        alembic_cfg.set_main_option('script_location', 'app/migration')
        alembic_cfg.set_main_option('sqlalchemy.url', sync_url)
        
        command.upgrade(alembic_cfg, 'head')

        # Проверяем таблицы
        inspector = inspect(engine)
        required_tables = ['users', 'categories', 'analytical_requests', 'goods', 'new_anl_configs']
        existing_tables = inspector.get_table_names()

        missing_tables = set(required_tables) - set(existing_tables)
        if missing_tables:
            raise Exception(f'Missing tables after migration: {missing_tables}')

        logger.info('Migrations completed successfully')

    except Exception as e:
        logger.error(f'Error during migrations: {e}')
        raise
    finally:
        engine.dispose()


def check_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
            logger.info('Database connection check: OK')
            return True
    except Exception as e:
        logger.error(f'Database connection check failed: {e}')
        return False


if __name__ == '__main__':
    run_migrations_with_retry()