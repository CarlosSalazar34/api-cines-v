from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from constants import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password(password: str)->str:
    """Genera el password hasheado"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)->bool:
    """Verifica el password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict)->str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({
        "exp": expire
    })
    jwt_token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return jwt_token

def verify_access_token(token: str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

