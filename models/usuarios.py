from sqlmodel import Field, SQLModel


class Usuarios(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    nombre: str | None = Field(default=None)
    email: str | None = Field(default=None, unique=True)
    password: str | None = Field(default=None)
