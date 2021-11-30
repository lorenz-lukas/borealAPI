from passlib.context import CryptContext
from os import getenv


def main():
    PASSWORD = getenv("PASSWORD", "senha")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    encrypted_password = pwd_context.hash(PASSWORD)
    print("\n\nPassword encrypted: {}\n\n".format(encrypted_password))


if __name__ == "__main__":
    main()