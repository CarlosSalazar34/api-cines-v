from fastapi import FastAPI
from datetime import datetime
import models
from sqlmodel import SQLModel
from database import engine
from services import users, theaters, movies, reservation

app = FastAPI(title="api peliculas")
SQLModel.metadata.create_all(engine)


@app.get("/")
async def root():
    return { 
        "message": "api funcional",
        "time": datetime.utcnow()
    }

app.include_router(users.router, tags=["users"])
app.include_router(theaters.router, tags=["theaters"])
app.include_router(movies.router, tags=["movies"])
app.include_router(reservation.router, tags=["reservation"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:app", reload=True, port=8000)