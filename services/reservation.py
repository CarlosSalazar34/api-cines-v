from fastapi import APIRouter, Depends, HTTPException, status
from database import engine
from models import (
    Usuarios, Tickets, TicketEstado,
    Seats, MovieSchedules
)
from schemas.reservation import ReservationRequest
from depends import get_current_user
from sqlmodel import Session, select

router = APIRouter(tags=["reservation"], prefix="/seats-reservations")


# ──────────────────────────────────────────────
#  POST  /seats-reservations/reservar
#  Reservar un asiento para un horario específico
# ──────────────────────────────────────────────
@router.post("/reservar", status_code=status.HTTP_201_CREATED)
async def reservar_asiento(
    request: ReservationRequest,
    usuario: Usuarios = Depends(get_current_user)
):
    with Session(engine) as session:
        # 1. Verificar que el horario (schedule) exista
        schedule = session.get(MovieSchedules, request.schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El horario no existe"
            )

        # 2. Verificar que el asiento exista
        seat = session.get(Seats, request.seat_id)
        if not seat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El asiento no existe"
            )

        # 3. Verificar que el asiento pertenece al cine del horario
        if seat.cine_id != schedule.theater_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El asiento no pertenece al cine de este horario"
            )

        # 4. Control de concurrencia: verificar disponibilidad con bloqueo
        #    with_for_update() bloquea la fila para evitar doble reserva
        statement = (
            select(Tickets)
            .where(
                Tickets.schedule_id == request.schedule_id,
                Tickets.seat_id == request.seat_id,
                Tickets.estado.in_([
                    TicketEstado.PENDIENTE,
                    TicketEstado.PAGADO
                ])
            )
            .with_for_update()
        )
        ticket_existente = session.exec(statement).first()

        if ticket_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este asiento ya está reservado para este horario"
            )

        # 5. Crear el ticket con estado PENDIENTE
        nuevo_ticket = Tickets(
            user_id=usuario.id,
            schedule_id=request.schedule_id,
            seat_id=request.seat_id,
            estado=TicketEstado.PENDIENTE
        )
        session.add(nuevo_ticket)
        session.commit()
        session.refresh(nuevo_ticket)

        return {
            "message": "Reserva creada exitosamente ✅",
            "ticket": {
                "id": nuevo_ticket.id,
                "schedule_id": nuevo_ticket.schedule_id,
                "seat_id": nuevo_ticket.seat_id,
                "estado": nuevo_ticket.estado,
                "user_id": nuevo_ticket.user_id
            }
        }


# ──────────────────────────────────────────────
#  GET  /seats-reservations/mis-reservas
#  Ver todas las reservas del usuario autenticado
# ──────────────────────────────────────────────
@router.get("/mis-reservas")
async def get_mis_reservas(usuario: Usuarios = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Tickets).where(Tickets.user_id == usuario.id)
        reservas = session.exec(statement).all()
        return reservas


# ──────────────────────────────────────────────
#  DELETE  /seats-reservations/cancelar/{ticket_id}
#  Cancelar una reserva pendiente
# ──────────────────────────────────────────────
@router.delete("/cancelar/{ticket_id}")
async def cancelar_reserva(
    ticket_id: int,
    usuario: Usuarios = Depends(get_current_user)
):
    with Session(engine) as session:
        # 1. Buscar el ticket
        ticket = session.get(Tickets, ticket_id)
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket no encontrado"
            )

        # 2. Verificar que el ticket pertenece al usuario
        if ticket.user_id != usuario.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para cancelar este ticket"
            )

        # 3. Solo se pueden cancelar tickets PENDIENTES
        if ticket.estado != TicketEstado.PENDIENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cancelar un ticket con estado '{ticket.estado.value}'"
            )

        # 4. Cambiar estado a CANCELADO
        ticket.estado = TicketEstado.CANCELADO
        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        return {
            "message": "Reserva cancelada exitosamente ❌",
            "ticket": {
                "id": ticket.id,
                "estado": ticket.estado
            }
        }


# ──────────────────────────────────────────────
#  GET  /seats-reservations/disponibilidad/{schedule_id}
#  Ver disponibilidad de asientos para un horario
# ──────────────────────────────────────────────
@router.get("/disponibilidad/{schedule_id}")
async def get_disponibilidad(
    schedule_id: int,
    usuario: Usuarios = Depends(get_current_user)
):
    with Session(engine) as session:
        # 1. Verificar que el horario exista
        schedule = session.get(MovieSchedules, schedule_id)
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El horario no existe"
            )

        # 2. Obtener todos los asientos del cine
        statement_seats = select(Seats).where(
            Seats.cine_id == schedule.theater_id
        )
        asientos = session.exec(statement_seats).all()

        # 3. Obtener los asientos ocupados para este horario
        statement_occupied = select(Tickets.seat_id).where(
            Tickets.schedule_id == schedule_id,
            Tickets.estado.in_([
                TicketEstado.PENDIENTE,
                TicketEstado.PAGADO
            ])
        )
        asientos_ocupados = set(session.exec(statement_occupied).all())

        # 4. Construir respuesta con disponibilidad
        disponibilidad = []
        for asiento in asientos:
            disponibilidad.append({
                "seat_id": asiento.id,
                "fila": asiento.fila,
                "numero": asiento.numero,
                "disponible": asiento.id not in asientos_ocupados
            })

        total = len(disponibilidad)
        libres = sum(1 for a in disponibilidad if a["disponible"])

        return {
            "schedule_id": schedule_id,
            "theater_id": schedule.theater_id,
            "total_asientos": total,
            "asientos_libres": libres,
            "asientos_ocupados": total - libres,
            "asientos": disponibilidad
        }