from fastapi import FastAPI
from sqladmin import Admin

from app.db.session import engine
from app.auth.users_controller import router as auth_user_router
from app.controller.query_endpoints_controller import router as query_endpoints_router
from app.admin_panel import QueryAdmin, HistoryAdmin, UserAdmin, RoleAdmin


app = FastAPI(title='Antipoff')


app.include_router(auth_user_router)
app.include_router(query_endpoints_router)


admin = Admin(app=app, engine=engine, title='Панель Администратора')


admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(QueryAdmin)
admin.add_view(HistoryAdmin)
