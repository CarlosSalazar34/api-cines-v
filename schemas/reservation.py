from pydantic import BaseModel


class ReservationRequest(BaseModel):
    """Modelo de solicitud para reservar un asiento"""
    schedule_id: int
    seat_id: int
