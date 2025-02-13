from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.auth_dao import UsersDAO


async def find_user_by_email(session: AsyncSession, email: str):
    user = await UsersDAO.find_one_or_none(session, email=email)
    return user