from fastapi import Depends
from sqlalchemy.orm import Session as SessionType
from app.db.engine import get_db
from app.services.auth import AuthService
from app.services.user import UserService

def get_user_service(db: SessionType = Depends(get_db)) -> UserService:
    return UserService(db=db)

def get_auth_service(db: SessionType = Depends(get_db)) -> AuthService:
    return AuthService(db=db)