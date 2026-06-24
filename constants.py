from fastapi.security.oauth2 import OAuth2PasswordBearer

ALGORITHM = "HS256"
SECRET_KEY = "llave_segura"
oauth2_schemes = OAuth2PasswordBearer(tokenUrl="/users/login")