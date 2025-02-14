from fastapi import FastAPI
from sqladmin import Admin

from app.db.session import engine
from app.auth.users_controller import router as auth_user_router
from app.controller.query_endpoints_controller import router as query_endpoints_router
from app.admin_panel import QueryAdmin, HistoryAdmin, UserAdmin, RoleAdmin


app = FastAPI(
    title='Antipoff',
    description="""
    **Antipoff** — это веб-приложение для управления пользователями, ролями и запросами кадастровых номеров.

    Основные возможности:
    - Регистрация и авторизация пользователей.
    - Управление ролями пользователей.
    - Работа с кадастровыми номерами: создание запросов и просмотр истории.
    - Административная панель для управления данными.

    Проект разработан с использованием FastAPI, SQLAlchemy, PostgreSQL и Docker-compose.
    """
        )


app.include_router(auth_user_router)
app.include_router(query_endpoints_router)


admin = Admin(app=app, engine=engine, title='Панель Администратора')


admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(QueryAdmin)
admin.add_view(HistoryAdmin)