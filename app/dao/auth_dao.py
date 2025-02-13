from app.auth.models import User, Role
from app.dao.base_dao import BaseDAO


#Возможно для нашего не большого проекта это избыточно, \ 
# но я стараюсь везде использовать такой паттерн проектирования
class UsersDAO(BaseDAO):
    model = User


class RoleDAO(BaseDAO):
    model = Role
