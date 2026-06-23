# MyBrain 🧠

> **Estado: En construcción activa** — Backend en desarrollo, frontend próximamente.

Aplicación de segundo cerebro personal con inteligencia artificial. Permite guardar notas y documentos, y conversar con ellos mediante un sistema RAG (Retrieval-Augmented Generation).

## Stack tecnológico

**Backend**
- FastAPI + Python 3.12
- PostgreSQL + SQLAlchemy
- ChromaDB (búsqueda vectorial semántica)
- Groq API — Llama 3.3 70B (chat con IA)
- JWT Authentication

**Frontend** *(próximamente)*
- Next.js + TypeScript
- Tailwind CSS

## Funcionalidades

- [x] Autenticación completa con JWT (registro, login, rutas protegidas)
- [x] CRUD de notas protegido por usuario
- [x] Integración con ChromaDB para búsqueda semántica
- [ ] Chat RAG con Groq (Llama 3.3 70B)
- [ ] Procesado de PDFs y URLs
- [ ] Frontend completo
- [ ] Deploy en producción

## Desarrollo local

### Requisitos
- Python 3.12+
- PostgreSQL

### Backend

```bash
cd backend
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crea un archivo `.env` en `backend/` siguiendo `.env.example`:

```bash
DATABASE_URL=postgresql://postgres:tu_contraseña@localhost:5432/mybrain
GROQ_API_KEY=tu_api_key
SECRET_KEY=tu_clave_secreta
```

Arranca el servidor:

```bash
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000` — documentación en `http://localhost:8000/docs`

## Autor

Alan Fernández — [alanfdez.dev](https://alanfdez.dev) · [GitHub](https://github.com/AlansitoFdez)