from Domain.Entities.password import Password


class PasswordHandler():
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return Password.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return Password.pwd_context.hash(password)