# Guía de Implementación: Sistema de Reserva de Entradas de Cine

Esta guía desglosa el diagrama de arquitectura en pasos lógicos y técnicos para que puedas programarlo paso a paso. Dado que estás trabajando en Python (por tu archivo `app.py`), los ejemplos conceptuales estarán orientados a frameworks como **FastAPI** o **Flask** usando **SQLAlchemy** para la base de datos.

## 1. Arquitectura: Monolito Modular
Aunque el diagrama muestra múltiples servicios (Users Service, Movies Service, etc.), todas las flechas apuntan a una **única base de datos central**. Por lo tanto, la forma más práctica de empezar es construir un **Monolito Modular**.
* En lugar de tener 5 aplicaciones separadas corriendo en puertos distintos, tendrás **una sola aplicación** (`app.py`).
* Cada "Servicio" del diagrama será un **módulo** o carpeta separada dentro de tu proyecto (ej. usando `APIRouter` en FastAPI o `Blueprints` en Flask).

## 2. Modelado de Datos Relacionales (SQL)
Este es el primer paso que debes programar. Aquí tienes una propuesta de esquema basada en tu diagrama:

* **Users (Usuarios):**
  * `id` (PK)
  * `nombre`, `email`, `password_hash`
* **Theaters (Cines):**
  * `id` (PK)
  * `nombre`, `ubicacion`
* **Seats (Asientos):**
  * `id` (PK)
  * `theater_id` (FK -> Theaters)
  * `fila` (ej. 'A', 'B'), `numero` (ej. 1, 2)
* **Movies (Películas):**
  * `id` (PK)
  * `titulo`, `sinopsis`, `duracion_minutos`
* **Movie Schedules (Horarios/Funciones):**
  * `id` (PK)
  * `movie_id` (FK -> Movies)
  * `theater_id` (FK -> Theaters)
  * `fecha_hora_inicio`, `fecha_hora_fin`
* **Tickets (Boletos/Reservas):**
  * `id` (PK)
  * `user_id` (FK -> Users)
  * `schedule_id` (FK -> Movie Schedules)
  * `seat_id` (FK -> Seats)
  * `estado` (Enum: 'PENDIENTE', 'PAGADO', 'CANCELADO')
  * `stripe_payment_id` (Varchar, opcional)

> [!IMPORTANT]  
> **Relación Asientos - Horarios:** Un asiento pertenece a un cine, pero su *disponibilidad* depende del horario (Movie Schedule). La tabla `Tickets` actuará como el registro de que un asiento está ocupado para un horario específico.

## 3. Implementación de los Servicios (Módulos)

Deberás crear endpoints (rutas) para cada uno de estos módulos:

### A. Users Service & Theaters Service & Movies Service
Estos son servicios CRUD (Crear, Leer, Actualizar, Borrar) básicos.
* **Users:** Registro, login, ver perfil.
* **Theaters:** Listar cines, ver detalles de un cine y sus asientos.
* **Movies:** Listar películas en cartelera, crear nuevas películas.

### B. Movies Service (Gestión de Horarios)
* **Endpoints:** Crear un horario para una película en un cine específico. Listar los horarios disponibles para una película.

### C. Seats Reservation Service (El núcleo lógico)
Este servicio es el más complejo porque requiere **Gestión de Transacciones**. Cuando un usuario selecciona un asiento, debes asegurarte de que nadie más pueda reservarlo al mismo tiempo.

**Lógica de Reserva (Paso a Paso):**
1. El usuario solicita reservar el `seat_id` 15 para el `schedule_id` 10.
2. Inicias una **Transacción de Base de Datos**.
3. Verificas si ya existe un registro en la tabla `Tickets` con ese `seat_id` y `schedule_id` cuyo estado sea `PAGADO` o `PENDIENTE`.
4. Si no existe, creas el registro en `Tickets` con estado `PENDIENTE`.
5. Haces el *Commit* de la transacción.

> [!TIP]
> **Gestión de Concurrencia:** Para evitar que dos personas reserven exactamente al mismo milisegundo, debes usar bloqueos a nivel de fila en SQL. En SQLAlchemy, esto se logra usando `with_for_update()` al hacer la consulta de verificación.

### D. Tickets Service & Stripe
Este servicio maneja el flujo de pago y la emisión final del boleto.

1. **Creación del Pago:** Cuando el usuario va a pagar su ticket `PENDIENTE`, tu backend llama a la API de Stripe para crear un *PaymentIntent*.
2. **Proceso en Frontend:** El cliente paga de forma segura usando el widget de Stripe.
3. **Confirmación (Webhook o Callback):** Stripe confirma el pago a tu backend.
4. **Actualización:** Tu backend actualiza el estado del registro en la tabla `Tickets` a `PAGADO` y guarda el `stripe_payment_id`.

> [!WARNING]
> **Gestión de Horarios (Timeouts):** Si un ticket se queda en estado `PENDIENTE` por más de 10-15 minutos (el usuario no completó el pago en Stripe), debes tener una tarea en segundo plano (ej. Celery o un cron job) que cambie el estado a `CANCELADO` o elimine el registro, liberando así el asiento para otros usuarios.

## 4. Orden de Desarrollo Recomendado

Para que programes esto de manera eficiente, te sugiero seguir este orden:
1. **Configurar el entorno:** `app.py`, conexión a base de datos y migraciones (ej. Alembic).
2. **Crear los Modelos (Tablas):** Define todas las clases de SQLAlchemy.
3. **CRUD Básico:** Desarrolla los endpoints para Películas, Cines y Usuarios.
4. **Horarios:** Crea la lógica para asignar películas a cines en horarios específicos.
5. **Reservas (Core):** Implementa el endpoint de selección de asientos con control de concurrencia.
6. **Pagos:** Integra la API de Stripe para finalizar el flujo de compra.
