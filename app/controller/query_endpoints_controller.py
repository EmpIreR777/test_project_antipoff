import asyncio
import random
from typing import List
from fastapi import APIRouter, Depends 
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.dto.query_endpoints_dto import \
    QueryCreate, QueryResponse, ResultCreate, ResultResponse
from app.services.query_endpoints_service import \
    add_query_in_bd, get_status_result, find_all_histories, \
    find_detail_histories
    

router = APIRouter(tags=['Requests for cadastral numbers'])


@router.post('/query', response_model=ResultCreate)
async def create_query(
    query: QueryCreate,
    session: AsyncSession = Depends(get_db_session)
        ):
    response = await add_query_in_bd(session=session, query=query)
    return response


@router.get('/ping')
async def ping():
    return {'status': 'Сервер запущен!'} # Если я правильно понял.


@router.get('/history/all', response_model=List[QueryResponse])
async def get_all_history(
    session: AsyncSession = Depends(get_db_session)
        ):
    history_all = await find_all_histories(session=session)
    return history_all


@router.get('/history/detail', response_model=List[ResultResponse])
async def get_detail_history(
    cadastral_number: str,
    session: AsyncSession = Depends(get_db_session)
        ):
    history_detail = await find_detail_histories(
        session=session, cadastral_number=cadastral_number
        )
    return history_detail


@router.get('/history')# И тут если я правильно понял.
async def get_result():
    delay = random.randint(1, 60)
    probability = random.randint(0, 1)
    await asyncio.sleep(delay)
    return {'history': bool(probability)}