"use client";

import { useEffect, useState } from "react";
import { Note, Document } from "@/types";
import { logout } from "@/lib/auth";
import api from "@/lib/api";
import ReactMarkdown from "react-markdown";

export default function DashboardPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<
    { role: string; content: string }[]
  >([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [urlInput, setUrlInput] = useState("");
  const [showUrlInput, setShowUrlInput] = useState(false);

  const fetchNotes = async () => {
    const response = await api.get<Note[]>("/notes");
    setNotes(response.data);
  };

  const fetchDocuments = async () => {
    const response = await api.get<Document[]>("/documents");
    setDocuments(response.data);
  };

  const uploadUrl = async () => {
    if (!urlInput.trim()) return;
    const formData = new FormData();
    formData.append("url", urlInput);
    await api.post("/documents/url", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setUrlInput("");
    setShowUrlInput(false);
    fetchDocuments();
  };

  const uploadPdf = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    await api.post("/documents/pdf", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    fetchDocuments();
  };

  useEffect(() => {
    fetchNotes();
    fetchDocuments();
  }, []);

  const createNote = async () => {
    const response = await api.post<Note>("/notes", {
      title: "Nueva nota",
      content: "",
    });
    setNotes([response.data, ...notes]);
    selectNote(response.data);
  };

  const selectNote = (note: Note) => {
    setSelectedNote(note);
    setTitle(note.title);
    setContent(note.content || "");
  };

  const saveNote = async () => {
    if (!selectedNote) return;
    setSaving(true);
    const response = await api.put<Note>(`/notes/${selectedNote.id}`, {
      title,
      content,
    });
    setNotes(notes.map((n) => (n.id === selectedNote.id ? response.data : n)));
    setSelectedNote(response.data);
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const deleteNote = async () => {
    if (!selectedNote) return;
    await api.delete(`/notes/${selectedNote.id}`);
    setNotes(notes.filter((n) => n.id !== selectedNote.id));
    setSelectedNote(null);
    setTitle("");
    setContent("");
  };

  const sendMessage = async () => {
    if (!chatInput.trim()) return;
    const userMessage = chatInput;
    setChatInput("");
    setChatMessages((prev: { role: string; content: string }[]) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);
    setChatLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ query: userMessage }),
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = "";

      setChatMessages((prev: { role: string; content: string }[]) => [
        ...prev,
        { role: "assistant", content: "" },
      ]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk
          .split("\n")
          .filter((line) => line.startsWith("data: "));

        for (const line of lines) {
          const data = JSON.parse(line.replace("data: ", ""));
          if (data.chunk) {
            assistantMessage += data.chunk;
            setChatMessages((prev: { role: string; content: string }[]) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                role: "assistant",
                content: assistantMessage,
              };
              return updated;
            });
          }
        }
      }
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="flex w-full h-screen">
      {/* SIDEBAR */}
      <div className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-4 border-b border-slate-200">
          <h1 className="font-semibold text-slate-900">MyBrain</h1>
        </div>

        <div className="flex-1 overflow-y-auto p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
              Notas
            </span>
            <button
              onClick={createNote}
              className="text-emerald-500 hover:text-emerald-600 text-lg font-light"
            >
              +
            </button>
          </div>

          {notes.map((note) => (
            <button
              key={note.id}
              onClick={() => selectNote(note)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm mb-1 transition-colors ${
                selectedNote?.id === note.id
                  ? "bg-emerald-50 text-emerald-700"
                  : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              {note.title}
            </button>
          ))}

          <div className="mt-4 mb-2 flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
              Documentos
            </span>
            <div className="flex gap-1">
              <label
                className="text-slate-400 hover:text-slate-600 cursor-pointer text-sm"
                title="Subir PDF"
              >
                📄
                <input
                  type="file"
                  accept=".pdf"
                  className="hidden"
                  onChange={uploadPdf}
                />
              </label>
              <button
                onClick={() => setShowUrlInput(!showUrlInput)}
                className="text-slate-400 hover:text-slate-600 text-sm"
                title="Añadir URL"
              >
                🌐
              </button>
            </div>
          </div>

          {showUrlInput && (
            <div className="mb-2 flex gap-1">
              <input
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && uploadUrl()}
                className="flex-1 px-2 py-1 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-emerald-500"
                placeholder="https://..."
              />
              <button
                onClick={uploadUrl}
                className="px-2 py-1 bg-emerald-500 text-white text-xs rounded-lg"
              >
                →
              </button>
            </div>
          )}

          {documents.map((doc) => (
            <div
              key={doc.id}
              className="px-3 py-2 text-sm text-slate-500 truncate"
            >
              {doc.source_type === "pdf" ? "📄" : "🌐"} {doc.title}
            </div>
          ))}
        </div>

        <div className="p-3 border-t border-slate-200 space-y-1">
          <button
            onClick={() => setChatOpen(!chatOpen)}
            className="w-full text-left px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-50 transition-colors"
          >
            💬 Chat con MyBrain
          </button>
          <button
            onClick={logout}
            className="w-full text-left px-3 py-2 rounded-lg text-sm text-slate-400 hover:bg-slate-50 transition-colors"
          >
            Cerrar sesión
          </button>
        </div>
      </div>

      {/* EDITOR */}
      <div className="flex-1 flex flex-col">
        {selectedNote ? (
          <>
            <div className="p-6 border-b border-slate-200 flex items-center justify-between">
              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="text-xl font-semibold text-slate-900 bg-transparent focus:outline-none flex-1"
                placeholder="Título de la nota"
              />
              <div className="flex gap-2 ml-4">
                <button
                  onClick={saveNote}
                  disabled={saving}
                  className={`px-4 py-1.5 text-white text-sm rounded-lg transition-all ${
                    saved
                      ? "bg-emerald-600"
                      : "bg-emerald-500 hover:bg-emerald-600"
                  }`}
                >
                  {saving ? "Guardando..." : saved ? "Guardado ✓" : "Guardar"}
                </button>
                <button
                  onClick={deleteNote}
                  className="px-4 py-1.5 bg-red-50 hover:bg-red-100 text-red-500 text-sm rounded-lg transition-colors"
                >
                  Eliminar
                </button>
              </div>
            </div>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="flex-1 p-6 text-slate-700 bg-transparent focus:outline-none resize-none text-sm leading-relaxed"
              placeholder="Escribe aquí el contenido de tu nota..."
            />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <p className="text-slate-400 text-sm">
                Selecciona una nota o crea una nueva
              </p>
              <button
                onClick={createNote}
                className="mt-3 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-sm rounded-lg transition-colors"
              >
                + Nueva nota
              </button>
            </div>
          </div>
        )}
      </div>

      {/* CHAT PANEL */}
      {chatOpen && (
        <div className="w-80 bg-white border-l border-slate-200 flex flex-col">
          <div className="p-4 border-b border-slate-200 flex items-center justify-between">
            <span className="font-medium text-slate-900 text-sm">
              Chat con MyBrain
            </span>
            <button
              onClick={() => setChatOpen(false)}
              className="text-slate-400 hover:text-slate-600"
            >
              ✕
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {chatMessages.length === 0 && (
              <p className="text-slate-400 text-xs text-center">
                Pregúntame sobre tus notas
              </p>
            )}
            {chatMessages.map((msg, i) => (
              <div
                key={i}
                className={`text-sm ${msg.role === "user" ? "text-right" : "text-left"}`}
              >
                <div
                  className={`inline-block px-3 py-2 rounded-lg max-w-[90%] ${
                    msg.role === "user"
                      ? "bg-emerald-500 text-white"
                      : "bg-slate-100 text-slate-700 prose prose-sm"
                  }`}
                >
                  {msg.role === "user" ? (
                    msg.content
                  ) : (
                    <ReactMarkdown>
                      {msg.content}
                    </ReactMarkdown>
                  )}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="text-left">
                <span className="inline-block px-3 py-2 rounded-lg bg-slate-100 text-slate-400 text-sm">
                  Pensando...
                </span>
              </div>
            )}
          </div>

          <div className="p-3 border-t border-slate-200 flex gap-2">
            <input
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="flex-1 px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Pregunta algo..."
            />
            <button
              onClick={sendMessage}
              disabled={chatLoading}
              className="px-3 py-2 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white text-sm rounded-lg transition-colors"
            >
              →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
