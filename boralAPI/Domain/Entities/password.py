from passlib.context import CryptContext


class Password():

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")