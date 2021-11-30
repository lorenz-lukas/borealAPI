from datetime import datetime, timedelta
from typing import Optional
from json import loads
from requests import get

from fastapi.responses import JSONResponse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "70f9b42ecd696bc5545915d6316ca590623d09786f3876d71d50c92d7472cb6b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Order(BaseModel):
    User: str
    Order: float
    PreviousOrder: bool


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/getAll", tags=['Open Breweries'])
async def get_all_breweries_data(current_user: User = Depends(get_current_active_user)):
    try:
        print("User: {}".format(current_user))
        res = get("https://api.openbrewerydb.org/breweries/")
        openBreweriesApiResult = res.__dict__
        return loads(openBreweriesApiResult["_content"])
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"Unable to retrieve data from https://api.openbrewerydb.org/breweries/.\n Error: {}".format(e.__dict__)},
        )


@app.get("/getNames", tags=['Open Breweries'])
async def get_breweries_name(current_user: User = Depends(get_current_active_user)):
    try:
        print("User: {}".format(current_user))
        res = get("https://api.openbrewerydb.org/breweries/")
        openBreweriesApiResult = res.__dict__
        names = [beer["name"] for beer in loads(openBreweriesApiResult["_content"])]
        return names
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"Unable to retrieve data from https://api.openbrewerydb.org/breweries/.\n Error: {}".format(e.__dict__)},
        )


@app.post("/order", tags=['Order'])
async def show_order(order: Order, current_user: User = Depends(get_current_active_user)):
    try:
        print("User: {}".format(current_user))
        return order
    except Exception as e:
        return JSONResponse(
            status_code=422,
            content={"Unable to return given data.\n Error: {}".format(e.__dict__)},
        )

