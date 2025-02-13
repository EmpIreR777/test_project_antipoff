from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import Integer, func, inspect
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(AsyncAttrs, DeclarativeBase):
    """
    Класс Base будет использоваться для создания моделей таблиц, которые автоматически добавляют поля create_ts и update_ts для отслеживания времени создания и обновления записей.
    """
    __abstract__ = True

    # Так же мы можем использовать UUID если мы этого хотим TODO
    id: Mapped[str] = mapped_column(Integer(), primary_key=True)
    create_ts: Mapped[datetime] = mapped_column(server_default=func.now())
    update_ts: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                onupdate=func.now())

    def to_dict(self, exclude_none: bool = False):
        """
        Преобразует объект модели в словарь.
        Args: exclude_none (bool): Исключать ли None значения из результата
        Returns: dict: Словарь с данными объекта
        """
        history = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, uuid.UUID):
                value = str(value)

            if not exclude_none or value is not None:
                history[column.key] = value

        return history