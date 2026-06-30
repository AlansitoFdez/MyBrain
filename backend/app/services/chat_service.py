from groq import Groq
from app.config import settings
from app.vector_store import search_notes
from typing import Generator

client = Groq(api_key=settings.GROQ_API_KEY)

def build_system_prompt(query: str, user_id: int, db) -> str:
    relevant_notes = search_notes(db, query, user_id)

    if relevant_notes:
        context = "\n\n".join(relevant_notes)
        return f"""Eres un asistente personal inteligente.
El usuario tiene las siguientes notas relevantes para su pregunta:

{context}

Responde basándote en el contenido de esas notas. Si la información no está en las notas, dilo claramente."""
    else:
        return """Eres un asistente personal inteligente.
El usuario no tiene notas relevantes para esta pregunta.
Responde de forma general e indícale que puede añadir notas sobre este tema."""

def chat_with_notes(query: str, user_id: int, db) -> str:
    system_prompt = build_system_prompt(query, user_id, db)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content

def chat_with_notes_stream(query: str, user_id: int, db) -> Generator[str, None, None]:
    system_prompt = build_system_prompt(query, user_id, db)

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        stream=True
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content