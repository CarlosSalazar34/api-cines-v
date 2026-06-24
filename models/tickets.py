from enum import Enum
from sqlmodel import Field, SQLModel


class TicketEstado(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"


class Tickets(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int | None = Field(foreign_key="usuarios.id", default=None)
    schedule_id: int | None = Field(foreign_key="movieschedules.id", default=None)
    seat_id: int | None = Field(foreign_key="seats.id", default=None)
    estado: TicketEstado = Field(default=TicketEstado.PENDIENTE)
    stripe_payment_id: str | None = Field(default=None)
