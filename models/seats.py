from sqlmodel import Field, SQLModel


class Seats(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    cine_id: int | None = Field(foreign_key="cines.id", default=None)
    fila: str | None = Field(default=None)
    numero: int | None = Field(default=None)
