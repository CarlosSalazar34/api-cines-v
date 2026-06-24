from datetime import datetime
from sqlmodel import Field, SQLModel


class MovieSchedules(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    movie_id: int | None = Field(foreign_key="movies.id", default=None)
    theater_id: int | None = Field(foreign_key="cines.id", default=None)
    fecha_hora_inicio: datetime | None = Field(default=None)
    fecha_hora_fin: datetime | None = Field(default=None)
