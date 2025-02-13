import asyncio
from app.db.session import async_session_maker
from app.db.models.models import History, Query
from app.auth.models import Role, User

# Данные для ролей
roles_data = [
    {'id': 1, 'name': 'admin'},
    {'id': 2, 'name': 'user'},
    ]

# Данные для пользователей
users_data = [
    {
        'id': 1,
        'username': 'john_doe',
        'password': 'securepassword1',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'is_active': True,
        'role_id': 1,
    },
    {
        'id': 2,
        'username': 'jane_smith',
        'password': 'securepassword2',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'is_active': True,
        'role_id': 2,
    },
    ]

# Данные для запросов
test_queries = [
    {'cadastral_number': '1234567890123', 'latitude': 55.7558, 'longitude': 37.6173},
    {'cadastral_number': '9876543210123', 'latitude': 59.9343, 'longitude': 30.3351},
    ]

# Данные для истории запросов
test_results = [
    {'query_id': 1, 'history': True},
    {'query_id': 1, 'history': False},
    {'query_id': 2, 'history': True},
    ]

async def some_async_function():
    async with async_session_maker() as session:
        for role in roles_data:
            session.add(Role(**role))
        for user in users_data:
            session.add(User(**user))
        for query in test_queries:
            session.add(Query(**query))
        for result in test_results:
            session.add(History(**result))
        await session.commit()


if __name__ == '__main__':
    asyncio.run(some_async_function())