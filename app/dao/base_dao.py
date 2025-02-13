import logging
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import func, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    """
    Базовые/Универсальные методы для работы со всеми моделями.
    """
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, **kwargs):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.
        Аргументы:  Критерии фильтрации в виде идентификатора записи.
        Возвращает: Экземпляр модели или None, если ничего не найдено.
        """
        try:
            query = select(cls.model).filter_by(**kwargs)
            history = await session.execute(query)
            return history.scalar_one_or_none()
        except SQLAlchemyError as e:
            logging.error(f'Ошибка при получение по id: {e}')
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.
        Аргументы: **filter_by: Критерии фильтрации в виде именованных параметров.
        Возвращает: Экземпляр модели или None, если ничего не найдено.
        """
        try:
            query = select(cls.model).filter_by(**filter_by)
            history = await session.execute(query)
            return history.scalar_one_or_none()
        except SQLAlchemyError as e:
            logging.error(f'Ошибка при получение по фильтрам: {e}')
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by) -> List:
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.
        Аргументы: **filter_by: Критерии фильтрации в виде именованных параметров.
        Возвращает: Список экземпляров модели.
        """
        try:
            query = select(cls.model).filter_by(**filter_by)
            history = await session.execute(query)
            return history.scalars().all()
        except SQLAlchemyError as e:
            logging.error(f'Ошибка при получение всей таблицы: {e}')
            raise

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.
        Аргументы: **values: Именованные параметры для создания нового экземпляра модели.
        Возвращает: Созданный экземпляр модели.
        """

        try:
            new_instance = cls.model(**values)
            session.add(new_instance)
            await session.flush()
            await session.refresh(new_instance)
            return new_instance
        except SQLAlchemyError as e:
            logging.error(f'Ошибка при добавлении в таблицу: {e}')
            await session.rollback()
            raise e

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: list[dict]):
        """
        Добавляет несколько записей в базу данных.
        instances: Список словарей, каждый из которых содержит данные для создания нового экземпляра модели.
        return: Список созданных экземпляров модели.
        """
        async with session.begin():
            new_instances = [cls.model(**values) for values in instances]
            session.add_all(new_instances)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                logging.error(f'Ошибка при добавление нескольких записей в таблицу: {e}')
                await session.rollback()
                raise e
            return new_instances

    @classmethod
    async def update(cls, session: AsyncSession, filter_by, **values):
        """
        Обновляет записи в базе данных по заданным условиям.
        Args: filter_by (dict): Словарь с условиями фильтрации {column_name: value}
        **values: Значения для обновления в формате column_name=value
        Returns: int: Количество обновленных записей
        Raises: SQLAlchemyError: При ошибке обновления данных
        """
        async with session.begin():
            query = (
                sqlalchemy_update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                .values(**values)
                .execution_options(synchronize_session='fetch')
            )
            try:
                history = await session.execute(query)
                await session.commit()
            except SQLAlchemyError as e:
                logging.error(f'Ошибка при обновление записи в таблице: {e}')
                await session.rollback()
                raise e
            return history.rowcount

    @classmethod
    async def delete(cls, session: AsyncSession, delete_all: bool = False, **filter_by):
        """
        Удаляет записи из базы данных на основе заданных критериев фильтрации или удаляет все записи.
        param delete_all: Если True, удаляет все записи в таблице модели.
        param filter_by: Ключевые аргументы, представляющие критерии фильтрации для удаления записей.
        return: Количество удаленных записей.
        raises ValueError: Если не указан ни один фильтр при попытке удалить частично.
        """
        if not delete_all and not filter_by:
            raise ValueError('Нужен хотя бы один фильтр для удаления.')

        async with session.begin():
            query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
            history = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                logging.error(f'Ошибка при удаление записей: {e}')
                await session.rollback()
                raise e
            return history.rowcount