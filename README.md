# API para reservas de entradas de cine 🎥🍿

hola! desarrolle este backend para dar un ejemplo de como se desarrolla una api en el campo laboral (o al menos como lo hago yo XD) y adelantarme la materia de bases de datos en la universidad (los de 4to semestre ch*p3nl0 ;v), mas que todo para los mas iniciados, para que vean como se ve un codigo backend real.

si vienes de hacer puros `print("hola mundo")` y querías saber cómo se ve algo más serio... bienvenido, aquí vas a sufrir un poquito ;v pero vas a aprender un montón

## Tecnologias utilizadas

| Componente | Tecnología | Descripción / Rol en la API |
| :--- | :--- | :--- |
| **Lenguaje** | Python 🐍 | Base de todo el desarrollo por su legibilidad y ecosistema. |
| **Framework** | FastAPI ⚡ | Para construir rutas rápidas, asíncronas y con validación automática (Pydantic). |
| **Base de Datos** | SQLite 🗃️ | Base de datos ligera para desarrollo. Fácil de usar, sin configurar servidores. (la que usan los pobres XD) |
| **ORM** | SQLModel 🚀🧑‍💻 | Para mapear las tablas de la base de datos a objetos de Python de forma limpia. |
| **Autenticación** | JWT (python-jose / Passlib) 🔒 | Seguridad para el login de usuarios y protección de rutas críticas. |
| **Server** | Uvicorn 🦄 | Servidor ASGI ultrarrápido para correr nuestra app. |

## Estructura del proyecto

```
backend-proyects/
├── app.py                  # 🚀 Punto de entrada, aquí arranca todo el show
├── database.py             # 🔌 Configuración del engine de la BD
├── constants.py            # 📌 Constantes (esquema OAuth2, etc.)
├── depends.py              # 🔐 Dependencias (get_current_user y esas cosas bonitas)
├── create_fake_data.py     # 🎭 Script para llenar la BD con datos falsos (para testear pues)
├── requirements.txt        # 📦 Dependencias del proyecto
│
├── models/                 # 📊 Modelos de la base de datos (SQLModel)
│   ├── usuarios.py         #     → Usuarios
│   ├── cines.py            #     → Cines / Teatros
│   ├── seats.py            #     → Asientos
│   ├── movies.py           #     → Películas
│   ├── movie_schedules.py  #     → Horarios de funciones
│   └── tickets.py          #     → Tickets / Reservas
│
├── schemas/                # 📝 Schemas de validación (Pydantic)
│   └── reservation.py      #     → Schema para crear reservas
│
├── services/               # ⚙️ Lógica de negocio (los endpoints viven aquí)
│   ├── users.py            #     → Login, registro, perfil
│   ├── theaters.py         #     → Info de cines, asientos, horarios
│   ├── movies.py           #     → CRUD de películas
│   └── reservation.py      #     → Reservar, cancelar, ver disponibilidad
│
└── security/               # 🛡️ Seguridad
    └── passwords.py        #     → Hashing de contraseñas y manejo de JWT
```

> si, separé todo en carpetas porque meter 500 líneas en un solo archivo es de psicópatas 🫠

## Endpoints disponibles

### 👤 Usuarios (`/users`)

| Método | Ruta | Descripción | Auth |
| :--- | :--- | :--- | :---: |
| `POST` | `/users/register_user` | Registrar usuario nuevo | ❌ |
| `POST` | `/users/login` | Iniciar sesión (devuelve JWT) | ❌ |
| `GET` | `/users/me` | Ver tu perfil (pa' que veas que sí funcionó) | ✅ |

### 🎬 Películas (`/movies`)

| Método | Ruta | Descripción | Auth |
| :--- | :--- | :--- | :---: |
| `GET` | `/movies/all` | Ver todas las películas disponibles | ✅ |
| `POST` | `/movies/new` | Agregar una película nueva | ❌ |

### 🏟️ Cines (`/theaters`)

| Método | Ruta | Descripción | Auth |
| :--- | :--- | :--- | :---: |
| `GET` | `/theaters/all` | Ver todos los cines | ✅ |
| `GET` | `/theaters/{id}` | Detalle de un cine específico | ✅ |
| `GET` | `/theaters/{id}/seats` | Ver asientos de un cine | ✅ |
| `GET` | `/theaters/{id}/schedules` | Ver horarios de un cine | ✅ |
| `GET` | `/theaters/{id}/movies` | Ver qué películas dan en ese cine | ✅ |

### 🎟️ Reservaciones (`/seats-reservations`)

| Método | Ruta | Descripción | Auth |
| :--- | :--- | :--- | :---: |
| `POST` | `/seats-reservations/reservar` | Reservar un asiento (el momento de la verdad 😤) | ✅ |
| `GET` | `/seats-reservations/mis-reservas` | Ver tus reservas | ✅ |
| `DELETE` | `/seats-reservations/cancelar/{ticket_id}` | Cancelar una reserva pendiente | ✅ |
| `GET` | `/seats-reservations/disponibilidad/{schedule_id}` | Ver qué asientos están libres | ✅ |

> **Auth ✅** = necesitas mandar tu token JWT en el header `Authorization: Bearer <tu_token>`. Si no lo mandas, la API te va a mandar a volar con un 401 🚫

## Configuración

### 1. Clonar el repo

```bash
git clone <aqui pones la url bruto :,v>
cd backend-proyects
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

#### Activar el entorno:

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows (cmd):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

> si no sabes qué es un entorno virtual... n't🧠? google es tu amigo, pero básicamente es para no ensuciar tu Python global con dependencias que después no sabes de dónde salieron 🤷‍♂️

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Correr la API

```bash
python app.py
```

o si te sientes fancy:

```bash
uvicorn app:app --reload --port 8000
```

La API va a estar disponible en `http://localhost:8000` y la documentación automática (gracias FastAPI, te amo ❤️) en:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### 5. (Opcional) Llenar la BD con datos de prueba

```bash
python create_fake_data.py
```

> esto te mete usuarios, cines, asientos, películas, horarios y tickets de mentira para que puedas jugar sin tener que crear todo a mano. De nada 😎 (te amo claude XD).

## Cómo funciona la autenticación

1. Te registras con `POST /users/register_user`
2. Haces login con `POST /users/login` (te devuelve un token JWT)
3. Ese token lo mandas en el header de las peticiones protegidas:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
4. Si el token es válido → pasas ✅
5. Si el token es inválido o expiró → 401 Unauthorized 💀

> es como la pulsera de un festival: sin pulsera no entras a VIP 🎶

## 🚀 Por qué SQLModel?

Si te preguntas por qué no usamos SQLAlchemy puro o Tortoise ORM, la respuesta es simple: **SQLModel** fue creado por tiangolo (el mismo crack que hizo FastAPI) y combina lo mejor de SQLAlchemy con Pydantic.

Esto significa que usamos **la misma clase** tanto para validar los datos que entran por la API (como un schema) como para mapear las tablas en la base de datos. Menos código duplicado = menos dolores de cabeza 🧠✨.

## Flujo de una reserva

```
1. Login → obtienes tu token 🔑
2. GET /movies/all → ves qué películas hay 🎬
3. GET /theaters/all → eliges un cine 🏟️
4. GET /theaters/{id}/schedules → ves los horarios 🕐
5. GET /seats-reservations/disponibilidad/{schedule_id} → ves qué asientos están libres 💺
6. POST /seats-reservations/reservar → reservas tu asiento 🎟️
7. GET /seats-reservations/mis-reservas → confirmas que todo salió bien ✅
```

> si alguien te ganó el asiento entre el paso 5 y el 6... pues ni modo, así es la vida 🤡 (hay control de concurrencia tranquilo, no se va a duplicar)

## Modelo de datos

```
Usuarios ─────┐
               ├──→ Tickets ←──┬── Seats
               │                │
MovieSchedules ┘                └── Cines
    │
    └── Movies
```

- Un **Usuario** puede tener muchos **Tickets**
- Un **Ticket** está asociado a un **Asiento**, un **Horario** y un **Usuario**
- Un **Horario (MovieSchedule)** conecta una **Película** con un **Cine** en una fecha/hora
- Un **Cine** tiene muchos **Asientos**
- Los tickets tienen estados: `PENDIENTE`, `PAGADO`, `CANCELADO`

## Cosas que me gustaría agregar después (si no me da flojera)

- [ ] Roles de usuario (admin vs usuario normal)
- [ ] Paginación en los endpoints de listado
- [ ] Endpoint para pagar un ticket (integrar pasarela de pago)
- [ ] Dockerizar todo esto 🐳
- [ ] Migrar a PostgreSQL para producción
- [ ] Tests unitarios (sí, lo sé, debería haberlos puesto desde el principio 😅)
- [ ] Rate limiting para que no te spameen la API

## Notas finales

- Este proyecto es con fines educativos, no me manden issues diciendo que falta CI/CD... ya lo sé 😭
- Si encuentras un bug, felicidades, encontraste una *feature no documentada* 🐛
- Pull requests son bienvenidos, pero si el código no tiene sentido lo voy a rechazar con cariño 💕

---

hecho con ☕ y mucho python por **Carlos Salazar** 🚀

Talk is cheap, show me the code, bruto :,v