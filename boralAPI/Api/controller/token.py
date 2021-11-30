from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from Api.config import Config
from Domain.Entities.token import Token
from Infra.Mock.mock_user import MockUser
from Infra.Repositories.auth import Authentication


token_router = InferringRouter()


@cbv(token_router)
class TokenRouter():

    form_data: OAuth2PasswordRequestForm = Depends()

    @token_router.post("/token", response_model=Token)
    async def login_for_access_token(self):
        
        user = Authentication.authenticate_user(
                    MockUser.fake_users_db,
                    self.form_data.username,
                    self.form_data.password
                )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Authentication.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
