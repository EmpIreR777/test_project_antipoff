from typing import List
from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.utils import authenticate_user, set_tokens
from app.dependencies.auth_dep import \
    get_current_user, get_current_admin_user, check_refresh_token
from app.db.session import get_db_session
from app.exceptions import \
    UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.dao.auth_dao import UsersDAO
from app.dto.auth_dto import \
    SUserRegister, SUserAuth, SUserInfo


router = APIRouter(tags=['Authorization'])


@router.post('/register/')
async def register_user(
    user_data: SUserRegister,
    session: AsyncSession = Depends(get_db_session)
        ) -> dict:
    """
    Регистрация нового пользователя.
    """
    existing_user = await UsersDAO.find_one_or_none(
        session, email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    user_data_dict = user_data.model_dump()
    user_data_dict.pop('confirm_password', None)

    await UsersDAO.add(session, **user_data_dict)

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/')
async def auth_user(
    response: Response,
    user_data: SUserAuth,
    session: AsyncSession = Depends(get_db_session)
        ):
    """
    Авторизация пользователя.
    """
    user = await UsersDAO.find_one_or_none(session, email=user_data.email)

    if not (user and await authenticate_user(user=user, password=user_data.password)):
        raise IncorrectEmailOrPasswordException

    set_tokens(response, user.id)
    return {
        'ok': True,
        'message': 'Авторизация успешна!'
        }


@router.post('/logout')
async def logout(response: Response):
    """
    Выход пользователя из системы.
    """
    response.delete_cookie('user_access_token')
    response.delete_cookie('user_refresh_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get('/me/')
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    """
    Получение информации о текущем пользователе.
    """
    return SUserInfo.model_validate(user_data)


@router.get('/all_users/')
async def get_all_users(
    session: AsyncSession = Depends(get_db_session),
    user_data: User = Depends(get_current_admin_user)
        ) -> List[SUserInfo]:
    """
    Получение списка всех пользователей (только для администратора).
    """
    users = await UsersDAO.find_all(session)
    return [SUserInfo.model_validate(user) for user in users]


@router.post('/refresh')
async def process_refresh_token(
    response: Response,
    user: User = Depends(check_refresh_token)
        ):
    """
    Обновление токенов.
    """
    set_tokens(response, user.id)
    return {'message': 'Токены успешно обновлены'}