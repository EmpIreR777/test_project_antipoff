import asyncio
import logging
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import DisconnectionError
from app.core.config import settings


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_migrations_with_retry(max_attempts=3, delay=4):
    """Запускает миграции с повторными попытками при ошибках подключения."""
    attempt = 0
    while attempt < max_attempts:
        try:
            run_migrations()
            return
        except DisconnectionError as e:
            attempt += 1
            if attempt == max_attempts:
                logger.error(f'Потерпел неудачу после {max_attempts} попытки: {e}')
                raise
            logger.warning(f'Ошибка соединения (попытки {attempt}/{max_attempts}): {e}')
            asyncio.delay(delay)


def run_migrations():
    """Основная функция для миграций."""
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
        required_tables = ['users', 'roles', 'histories', 'queries']
        existing_tables = inspector.get_table_names()

        missing_tables = set(required_tables) - set(existing_tables)
        if missing_tables:
            raise Exception(f'Отсутствующие таблицы после переноса: {missing_tables}')

        logger.info('Миграция успешно завершена')

    except Exception as e:
        logger.error(f'Ошибка во время миграции: {e}')
        raise
    finally:
        engine.dispose()


def check_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
            logger.info('Проверка подключения к базе данных: OK')
            return True
    except Exception as e:
        logger.error(f'Не удалось проверить подключение к базе данных: {e}')
        return False


if __name__ == '__main__':
    run_migrations_with_retry()