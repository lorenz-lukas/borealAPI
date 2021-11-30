from jose import jwt
from typing import Optional
from datetime import datetime, timedelta
from Domain.Handlers.user import UserHandler
from Domain.Handlers.password import PasswordHandler
from Api.config import Config


class Authentication():

    
    def authenticate_user(fake_db, username: str, password: str):
        user = UserHandler.get_user(fake_db, username)
        if not user:
            return False
        if not PasswordHandler.verify_password(password, user.hashed_password):
            return False
        return user

    
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt