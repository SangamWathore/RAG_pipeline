from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth_schema import (
    RegisterRequest,
    UserResponse,
    TokenResponse,
    LoginRequest
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",
        response_model=UserResponse
)
def register(
        request:RegisterRequest,
        db:Session = Depends(get_db)
):
    
    auth_service = AuthService(db) 

    try:
        user = auth_service.register(
            username=request.username,
            password=request.password
        )
        return user

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )



@router.post("/login",
        response_model=TokenResponse
    )
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db:Session = Depends(get_db)
):
    auth_service = AuthService(db)

    try:

        access_token = auth_service.login(
            username = form_data.username,
            password = form_data.password
        )

        return {
            "access_token":access_token,
            "token_type":"bearer"
        }

    except ValueError as error:
         raise HTTPException(
        status_code = 401,
        detail = str(error)
    )
