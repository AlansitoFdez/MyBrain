from groq import Groq
from app.config import settings
from app.vector_store import search_notes

client = Groq(api_key=settings.GROQ_API_KEY)

def chat_with_notes(query: str, user_id: int) -> str:
    relevant_notes = search_notes(query, user_id)

    if relevant_notes:
        context = "\n\n".join(relevant_notes)
        system_prompt = f"""Eres un asistente personal inteligente. 
El usuario tiene las siguientes notas relevantes para su pregunta:

{context}

Responde basándote en el contenido de esas notas. Si la información no está en las notas, dilo claramente."""
    else:
        system_prompt = """Eres un asistente personal inteligente. 
El usuario no tiene notas relevantes para esta pregunta. 
Responde de forma general e indícale que puede añadir notas sobre este tema."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content