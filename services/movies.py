from fastapi import APIRouter, Depends, HTTPException, status
from database import engine
from models import Usuarios, Movies
from depends import get_current_user
from sqlmodel import Session, select

router = APIRouter(tags=["movies"], prefix="/movies")

@router.get("/all")
async def get_all_movies(usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Movies)
        data = session.exec(statement).all()
        session.commit()
        return data

@router.post("/new")
async def post_movies(movie: Movies):
    with Session(engine) as session: 
        statement = select(Movies).where(movie.titulo == Movies.titulo)
        pelicula_existe = session.exec(statement=statement).first()
        if pelicula_existe:
            raise HTTPException( 
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta pelicula ya existe"
            )
        session.add(movie)
        session.commit()
        session.refresh(movie)
        return { 
            "movie": movie.titulo,
            "message": "pelicula agregada"
        }
