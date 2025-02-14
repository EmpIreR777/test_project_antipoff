from sqladmin import ModelView
from app.db.models.models import Query, History
from app.auth.models import User, Role


class RoleAdmin(ModelView, model=Role):
    column_list = [Role.id, Role.name]
    column_searchable_list = [Role.name]
    column_sortable_list = [Role.id, Role.name]
    icon = 'fa-solid fa-users-gear'

    def __repr__(self):
        return f'RoleAdmin: {self.model}'


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.full_name,
        User.email,
        User.is_active,
        User.role_id,
        ]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.role_id]
    icon = 'fa-solid fa-user'

    column_details_list = [User.role]

    def __repr__(self):
        return f'UserAdmin: {self.model}'


class QueryAdmin(ModelView, model=Query):
    column_list = [
        Query.id,
        Query.cadastral_number,
        Query.latitude,
        Query.longitude,
        ]
    column_searchable_list = [Query.cadastral_number]
    column_sortable_list = [Query.id, Query.cadastral_number]
    icon = 'fa-solid fa-search'

    def __repr__(self):
        return f'QueryAdmin: {self.model}'


class HistoryAdmin(ModelView, model=History):
    column_list = [
        History.id,
        History.query_id,
        History.history,
        ]
    column_searchable_list = [History.query_id]
    column_sortable_list = [History.id, History.query_id]
    icon = 'fa-solid fa-history'

    column_details_list = [History.query]

    def __repr__(self):
        return f'HistoryAdmin: {self.model}'