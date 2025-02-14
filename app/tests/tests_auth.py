import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.db.session import get_db_session
from app.auth.models import User
from app.dao.auth_dao import UsersDAO


@pytest_asyncio.fixture
async def client():
    """Фикстура для тестового клиента."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture
async def session():
    """Фикстура для тестовой сессии."""
    async for session in get_db_session():
        yield session


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, session: AsyncSession):
    """Тест для регистрации пользователя."""
    user_data = {
        'username': 'testuser1',
        'email': 'test1@example.com',
        'password': 'password1',
        'confirm_password': 'password1',
        'first_name': 'Test1',
        'last_name': 'User1'
        }
    response = await client.post('/register/', json=user_data)
    assert response.status_code == 200
    assert response.json() == {'message': 'Вы успешно зарегистрированы!'}

    user = await UsersDAO.find_one_or_none(session, email=user_data['email'])
    assert user is not None


@pytest.mark.asyncio
async def test_auth_user(client: AsyncClient, session: AsyncSession):
    """Тест для авторизации пользователя."""
    user_data = {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password2',
        'confirm_password': 'password2',
        'first_name': 'Test2',
        'last_name': 'User2'
        }
    await client.post('/register/', json=user_data)

    auth_data = {
        'email': 'test2@example.com',
        'password': 'password2'
        }
    response = await client.post('/login/', json=auth_data)
    assert response.status_code == 200
    assert response.json() == {'ok': True, 'message': 'Авторизация успешна!'}
    print(response.cookies,'!!!!!!!!!!!!!!!!!!!!')
    assert 'user_access_token' in response.cookies
    assert 'user_refresh_token' in response.cookies


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    """Тест для выхода пользователя."""
    auth_data = {
        'email': 'test2@example.com',
        'password': 'password2'
        }
    await client.post('/login/', json=auth_data)

    response = await client.post('/logout')

    assert response.status_code == 200
    assert response.json() == {'message': 'Пользователь успешно вышел из системы'}

    assert 'user_access_token' not in response.cookies
    assert 'user_refresh_token' not in response.cookies


# @pytest.mark.asyncio
# async def test_get_me(client: AsyncClient):
# """Тест для получения информации о текущем пользователе"""
#     auth_data = {
#         'email': 'test2@example.com',
#         'password': 'password2'
#     }
#     login_response = await client.post('/login/', json=auth_data)
#     assert login_response.status_code == 200

#     access_token = client.cookies.get('user_access_token')
#     headers = {'Authorization': f'Bearer {access_token}'}

#     response = await client.get('/me/', headers=headers)
#     assert response.status_code == 200
#     assert response.json()['email'] == 'test2@example.com'



# @pytest.mark.asyncio
# async def test_get_all_users(client: AsyncClient, session: AsyncSession):
# """ Тест для получения списка всех пользователей (только для администратора)."""
#     admin_data = {
#         'username': 'testuser2',
#         'email': 'admin3@example.com',
#         'password': 'admin3',
#         'confirm_password': 'admin3',
#         'first_name': 'Test3',
#         'last_name': 'Admin3',
#         'is_admin': True
#         }
#     await client.post('/register/', json=admin_data)

#     auth_data = {
#         'email': 'admin3@example.com',
#         'password': 'admin3'
#     }
#     await client.post('/login/', json=auth_data)

#     response = await client.get('/all_users/')
#     assert response.status_code == 200
#     users = response.json()
#     assert len(users) > 0


# @pytest.mark.asyncio
# async def test_refresh_token(client: AsyncClient):
# """ Тест для обновления токенов."""
#     auth_data = {
#         'email': 'test1@example.com',
#         'password': 'password1'
#     }
#     await client.post('/login/', json=auth_data)

#     response = await client.post('/refresh')
#     assert response.status_code == 200
#     assert response.json() == {'message': 'Токены успешно обновлены'}

#     assert 'user_access_token' in response.cookies
#     assert 'user_refresh_token' in response.cookies