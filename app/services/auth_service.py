from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.utils.jwt_utils import create_access_token

class AuthService:

    def __init__(self, db:Session):

        self.user_repository = UserRepository(db)
        self.password_hash = PasswordHash.recommended()

    def register(
            self,
            username:str,
            password:str
    ):
        existing_user = (
            self.user_repository
            .get_by_username(username)
        )
        if existing_user :
            raise ValueError(
                "Username already exists"
            )

        hashed_password = (
            self.password_hash.hash(password)
        )

        user = self.user_repository.create_user(
            username = username,
            hashed_password = hashed_password
        )

        return user
    

    def login(
        self,
        username: str,
        password: str
    ):

        user = (
            self.user_repository
            .get_by_username(username)
        )

        if not user:

            raise ValueError(
                "Invalid username or password"
            )

        password_valid = (
            self.password_hash.verify(
                password,
                user.hashed_password
            )
        )

        if not password_valid:

            raise ValueError(
                "Invalid username or password"
            )

        access_token = create_access_token(
            user.id
        )

        return access_token