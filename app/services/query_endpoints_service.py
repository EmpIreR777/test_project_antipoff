import logging
import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.dao.query_endpoints_dao import QueryDAO, HistoryDAO


async def add_query_in_bd(session: AsyncSession, query):
    try:
        new_query = await QueryDAO.add(
            session=session, **query.dict()
            )
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://localhost:3000/history', timeout=60
                    )
                response.raise_for_status()
                result_data = response.json()
                history = result_data['history']
        except httpx.HTTPError as e:
            logging.error(f'Ошибка при выполнении HTTP-запроса: {e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Сервис недоступен'
            )
        await HistoryDAO.add(
            session=session, query_id=new_query.id, history=history
            )
        return {'history': history}

    except SQLAlchemyError as e:
        logging.error(f'Ошибка при добавлении запроса в таблицу: {e}')
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка базы данных')


async def find_all_histories(session: AsyncSession):
    result_all = await QueryDAO.find_all(session=session)
    if not result_all:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='История всех запросов не найдена'
        )
    return result_all


async def find_detail_histories(session: AsyncSession, cadastral_number: str):
    result_detail = await HistoryDAO.find_histories_by_cadastral_number(
        session=session, cadastral_number=cadastral_number
        )
    if not result_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='История по кадастровому номеру не найдена'
        )
    return result_detail


async def get_status_result(session: AsyncSession, query_id: int):
    result_query_id = await HistoryDAO.find_one_or_none_by_id(
        session=session, query_id=query_id
        )
    if not result_query_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Результат по запросу не найден'
        )
    return result_query_id