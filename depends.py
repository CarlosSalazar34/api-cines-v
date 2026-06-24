from constants import oauth2_schemes
from fastapi import HTTPException, Depends, status
from security.passwords import *
from database import engine
from models import Usuarios
from jose import JWTError
from sqlmodel import Session, select

# DEPENDENCIAS RUTA PARA OBTENER INFORMACION DEL USUARIO
def get_current_user(token: str = Depends(oauth2_schemes)):
    auth_error = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autorizado",
                headers={ 
                    "WWW-Authenticate": "Bearer"
                })
    try:
        payload: dict = verify_access_token(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise auth_error
    except JWTError: 
        raise auth_error
            
    with Session(engine) as session: 
        statement = select(Usuarios).where(Usuarios.nombre == username)
        username = session.exec(statement=statement).first()
        if username is None:
            raise auth_error
        return username