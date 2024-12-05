from app.database.repositories.interfaces.iuserrepository import IUserRepository
from app.models.user import User


class UserRepository(IUserRepository):
    def get_user_by_username(self, username: str) -> None | User:
        user = self.db_session.query(User).where(User.username == username).first()
        return user
