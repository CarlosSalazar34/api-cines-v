"""
Script para poblar la base de datos con datos falsos de prueba.
Ejecutar: python create_fake_data.py
"""

import os
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Session
from database import engine
from models import (
    Usuarios,
    Cines,
    Seats,
    Movies,
    MovieSchedules,
    Tickets,
    TicketEstado,
)

# ── Eliminar la DB existente para empezar limpio ──────────────────────────────
DB_PATH = "cine.db"
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"🗑️  Base de datos '{DB_PATH}' eliminada.")

# ── Crear todas las tablas ────────────────────────────────────────────────────
SQLModel.metadata.create_all(engine)
print("✅ Tablas creadas correctamente.\n")


# ── Datos de prueba ───────────────────────────────────────────────────────────

def seed_data():
    with Session(engine) as session:

        # ── Usuarios ──────────────────────────────────────────────────────
        usuarios = [
            Usuarios(nombre="Carlos Salazar", email="carlos@email.com", password="hashed_abc123"),
            Usuarios(nombre="María García", email="maria@email.com", password="hashed_def456"),
            Usuarios(nombre="Juan Pérez", email="juan@email.com", password="hashed_ghi789"),
            Usuarios(nombre="Ana Rodríguez", email="ana@email.com", password="hashed_jkl012"),
            Usuarios(nombre="Luis Martínez", email="luis@email.com", password="hashed_mno345"),
            Usuarios(nombre="Sofía López", email="sofia@email.com", password="hashed_pqr678"),
            Usuarios(nombre="Diego Torres", email="diego@email.com", password="hashed_stu901"),
            Usuarios(nombre="Valentina Díaz", email="valentina@email.com", password="hashed_vwx234"),
        ]
        session.add_all(usuarios)
        session.commit()
        for u in usuarios:
            session.refresh(u)
        print(f"👤 {len(usuarios)} usuarios creados.")

        # ── Cines ─────────────────────────────────────────────────────────
        cines = [
            Cines(nombre="CinePlex Centro", ubicacion="Av. Libertador 1200, Centro"),
            Cines(nombre="MegaCine Mall Norte", ubicacion="CC Mall Norte, Local 45"),
            Cines(nombre="CineArte Independiente", ubicacion="Calle Cultura 88, Zona Colonial"),
        ]
        session.add_all(cines)
        session.commit()
        for c in cines:
            session.refresh(c)
        print(f"🏢 {len(cines)} cines creados.")

        # ── Asientos (Seats) ──────────────────────────────────────────────
        filas = ["A", "B", "C", "D", "E", "F"]
        asientos_por_fila = 10
        seats = []
        for cine in cines:
            for fila in filas:
                for numero in range(1, asientos_por_fila + 1):
                    seats.append(
                        Seats(cine_id=cine.id, fila=fila, numero=numero)
                    )
        session.add_all(seats)
        session.commit()
        for s in seats:
            session.refresh(s)
        print(f"💺 {len(seats)} asientos creados ({len(filas)} filas × {asientos_por_fila} asientos × {len(cines)} cines).")

        # ── Películas (Movies) ────────────────────────────────────────────
        movies = [
            Movies(
                titulo="El Último Viaje",
                sinopsis="Un astronauta debe tomar una decisión imposible cuando su nave pierde contacto con la Tierra durante una misión a Marte.",
                duracion_minutos=135,
            ),
            Movies(
                titulo="Sombras del Pasado",
                sinopsis="Una detective retirada regresa a investigar un caso que nunca pudo resolver y que está conectado con su propia familia.",
                duracion_minutos=118,
            ),
            Movies(
                titulo="Código Aurora",
                sinopsis="Un grupo de hackers descubre una conspiración gubernamental oculta en el código fuente de una red social popular.",
                duracion_minutos=142,
            ),
            Movies(
                titulo="Corazón de Acero",
                sinopsis="Drama basado en hechos reales sobre un bombero que arriesga todo para salvar a los atrapados en un edificio en llamas.",
                duracion_minutos=127,
            ),
            Movies(
                titulo="La Isla Olvidada",
                sinopsis="Comedia de aventuras donde un grupo de turistas queda varado en una isla desierta con secretos inesperados.",
                duracion_minutos=105,
            ),
            Movies(
                titulo="Frecuencia Cero",
                sinopsis="Thriller de ciencia ficción donde una señal de radio misteriosa comienza a alterar la realidad de un pequeño pueblo.",
                duracion_minutos=130,
            ),
        ]
        session.add_all(movies)
        session.commit()
        for m in movies:
            session.refresh(m)
        print(f"🎬 {len(movies)} películas creadas.")

        # ── Horarios (MovieSchedules) ─────────────────────────────────────
        # Generar horarios para los próximos 3 días
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        horarios = []

        turnos_hora = [10, 13, 16, 19, 22]  # horarios de funciones

        for dia_offset in range(3):
            fecha = hoy + timedelta(days=dia_offset)
            for i, movie in enumerate(movies):
                # Cada película se muestra en un cine y horario específico
                cine = cines[i % len(cines)]
                hora = turnos_hora[i % len(turnos_hora)]
                inicio = fecha.replace(hour=hora, minute=0)
                fin = inicio + timedelta(minutes=movie.duracion_minutos)
                horarios.append(
                    MovieSchedules(
                        movie_id=movie.id,
                        theater_id=cine.id,
                        fecha_hora_inicio=inicio,
                        fecha_hora_fin=fin,
                    )
                )
        session.add_all(horarios)
        session.commit()
        for h in horarios:
            session.refresh(h)
        print(f"🗓️  {len(horarios)} horarios de funciones creados ({len(movies)} películas × 3 días).")

        # ── Tickets ───────────────────────────────────────────────────────
        tickets = [
            # Carlos compra 2 entradas pagadas para "El Último Viaje"
            Tickets(user_id=usuarios[0].id, schedule_id=horarios[0].id, seat_id=seats[0].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_001"),
            Tickets(user_id=usuarios[0].id, schedule_id=horarios[0].id, seat_id=seats[1].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_002"),

            # María tiene un ticket pendiente para "Sombras del Pasado"
            Tickets(user_id=usuarios[1].id, schedule_id=horarios[1].id, seat_id=seats[60].id,
                    estado=TicketEstado.PENDIENTE, stripe_payment_id=None),

            # Juan canceló su ticket para "Código Aurora"
            Tickets(user_id=usuarios[2].id, schedule_id=horarios[2].id, seat_id=seats[120].id,
                    estado=TicketEstado.CANCELADO, stripe_payment_id="pi_fake_003"),

            # Ana tiene 3 tickets pagados para "Corazón de Acero"
            Tickets(user_id=usuarios[3].id, schedule_id=horarios[3].id, seat_id=seats[10].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_004"),
            Tickets(user_id=usuarios[3].id, schedule_id=horarios[3].id, seat_id=seats[11].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_005"),
            Tickets(user_id=usuarios[3].id, schedule_id=horarios[3].id, seat_id=seats[12].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_006"),

            # Luis tiene un ticket pagado para "La Isla Olvidada"
            Tickets(user_id=usuarios[4].id, schedule_id=horarios[4].id, seat_id=seats[65].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_007"),

            # Sofía tiene un ticket pendiente para "Frecuencia Cero"
            Tickets(user_id=usuarios[5].id, schedule_id=horarios[5].id, seat_id=seats[125].id,
                    estado=TicketEstado.PENDIENTE, stripe_payment_id=None),

            # Diego compra para el día 2
            Tickets(user_id=usuarios[6].id, schedule_id=horarios[6].id, seat_id=seats[3].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_008"),

            # Valentina compra para el día 3
            Tickets(user_id=usuarios[7].id, schedule_id=horarios[12].id, seat_id=seats[70].id,
                    estado=TicketEstado.PAGADO, stripe_payment_id="pi_fake_009"),
        ]
        session.add_all(tickets)
        session.commit()
        print(f"🎫 {len(tickets)} tickets creados.")

        # ── Resumen ───────────────────────────────────────────────────────
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE DATOS DE PRUEBA")
        print("=" * 50)
        print(f"  👤 Usuarios:    {len(usuarios)}")
        print(f"  🏢 Cines:       {len(cines)}")
        print(f"  💺 Asientos:    {len(seats)}")
        print(f"  🎬 Películas:   {len(movies)}")
        print(f"  🗓️  Horarios:    {len(horarios)}")
        print(f"  🎫 Tickets:     {len(tickets)}")
        print("=" * 50)
        print("✅ ¡Base de datos poblada exitosamente!")


if __name__ == "__main__":
    seed_data()
