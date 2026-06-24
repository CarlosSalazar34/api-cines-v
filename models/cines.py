from sqlmodel import Field, SQLModel


class Cines(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    nombre: str | None = Field(default=None)
    ubicacion: str | None = Field(default=None)
