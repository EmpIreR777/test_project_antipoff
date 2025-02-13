import logging
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.models.models import Query, History
from app.dao.base_dao import BaseDAO


#Возможно для нашего не большого проекта это избыточно, \ 
# но я стараюсь везде использовать такой паттерн проектирования
class QueryDAO(BaseDAO):
    model = Query


class HistoryDAO(BaseDAO):
    model = History

    @classmethod
    async def find_histories_by_cadastral_number(
        cls, session: AsyncSession, cadastral_number: str
        ):
        """
        Находит все истории, связанные с кадастровым номером.
        """
        try:
            query = (
                select(cls.model)
                .join(Query)
                .options(joinedload(cls.model.query))
                .where(Query.cadastral_number == cadastral_number)
                )
            result = await session.execute(query)
            histories = result.scalars().all()

            return histories
        except SQLAlchemyError as e:
            logging.error(f'Ошибка при получении всех историй запросов: {e}')
            raise