from datetime import datetime, timedelta, timezone
import jwt

from app.config import (
 JWT_SECRET_KEY,
 JWT_ALGORITHM,
 JWT_ACCESS_TOKEN_EXPIRE_MINUTES   
)


def create_access_token(user_id:str):
    expire = datetime.now(timezone.utc)+timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token
