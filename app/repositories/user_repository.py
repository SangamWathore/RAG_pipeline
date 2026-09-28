from sqlalchemy.orm import Session
from app.models.user_model import User

class UserRepository:

    def __init__(self, db):
        self.db = db

    # cheking user is alerady exist or not
    def get_by_username(self, username:str):

        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )
    
    def get_by_id(self, user_id: int):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # creating a new user
    def create_user(
            self,
            username : str,
            hashed_password:str
    ):
        user = User(
            username = username,
            hashed_password = hashed_password
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user