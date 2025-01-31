from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password: str) -> str:
    return pwd_contend.hash(password)

def decrypt_password_and_verify(password: str, hashed_password: str) -> bool:
    return pwd_contend.verify(password, hashed_password)