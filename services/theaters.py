from fastapi import APIRouter, Depends
from database import engine
from models import Cines, Usuarios, Seats, MovieSchedules, Movies
from sqlmodel import select, Session
from depends import get_current_user

router = APIRouter(tags=['theaters'], prefix="/theaters")

@router.get("/all")
async def get_theaters(usuario: Usuarios = Depends(get_current_user)):
    """Solo usuarios autenticados pueden ver la informacion"""
    with Session(engine) as session:
        statement = select(Cines)
        data = session.exec(statement).all()
        session.commit()
        return data
        

@router.get("/{id}")
async def get_theater_detail(id: int, usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session: 
        statement = select(Cines).where(Cines.id == id)
        data = session.exec(statement).first()
        session.commit()
        return data

@router.get("/{id}/seats")
async def get_theater_seats(id: int, usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Seats).where(Seats.cine_id == id)
        data = session.exec(statement).all()
        session.commit()
        return data


@router.get("/{id}/schedules")
async def get_theater_schedules(id: int, usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(MovieSchedules).where(MovieSchedules.theater_id == id)
        data = session.exec(statement).all()
        return data

@router.get("/{id}/movies")
async def get_theater_movies(id: int, usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session:
        statement = (
            select(Movies)
            .join(MovieSchedules, MovieSchedules.movie_id == Movies.id)
            .where(MovieSchedules.theater_id == id)
        )
        data = session.exec(statement).all()
        return data
    
