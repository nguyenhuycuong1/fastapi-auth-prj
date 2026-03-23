
from sqlalchemy.orm import Session

from app.core.auth import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

class UserService:

    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user_create: UserCreate, db: Session):
        hashed_password = hash_password(user_create.password)
        user_create.password = hashed_password
        return self.user_repo.create(user_create, db)

    def get_all_users(self, db: Session):
        return self.user_repo.get_all(db)

    def get_user_by_id(self, user_id: int, db: Session):
        return self.user_repo.get_by_id(user_id, db)

    def get_user_by_username(self, username: str, db: Session):
        return self.user_repo.get_by_username(username, db)


