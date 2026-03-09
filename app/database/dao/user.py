from app.database.dao.base import BaseDAO
from app.database.models import User


class UserDAO(BaseDAO):
    model = User