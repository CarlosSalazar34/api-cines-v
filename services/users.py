from fastapi import APIRouter, status, HTTPException, Depends
from database import engine
from models import Usuarios
from sqlmodel import Session, select
from security.passwords import (generate_password,
                                 verify_password,
                                   create_access_token)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from depends import get_current_user

router = APIRouter(tags=["Users"], prefix="/users")


# RUTAS PARA ACCIONES DEL USUARIO
@router.get("/me", status_code=status.HTTP_200_OK)
async def me(username: Usuarios = Depends(get_current_user)):
    return { 
        "name": username.nombre,
        "email": username.email,
        "message": "usuario encontrado ✅"
    }

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try: 
        with Session(engine) as session:
            statement = select(Usuarios).where(Usuarios.nombre == form_data.username)
            username = session.exec(statement).first()
            if not username or not verify_password(form_data.password, username.password):
                raise HTTPException( 
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            else: 
                access_token = create_access_token(data={ 
                    "sub": username.nombre
                })
                return {
                    "access_token": access_token,
                    "token_type": "bearer"
                }
                
    except Exception: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

@router.post("/register_user", status_code=status.HTTP_201_CREATED)
async def register_user(user: Usuarios):
    try: 
        with Session(engine) as session:
            statement = select(Usuarios).where(Usuarios.nombre == user.nombre)
            usuario_existe = session.exec(statement=statement).first()
            if usuario_existe: 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este usuario ya existe en la base de datos"
                )
            else:
                hashed_password = generate_password(user.password) 
                user.password = hashed_password
                session.add(user)   
                session.commit()
                session.refresh(user)
            return { 
                "message": "user created"
            }
    except Exception: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado"
        )