from sqlmodel import Field, SQLModel


class Movies(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    titulo: str | None = Field(default=None)
    sinopsis: str | None = Field(default=None)
    duracion_minutos: int | None = Field(default=None)
