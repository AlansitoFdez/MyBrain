export interface User {
  id: number
  email: string
  username: string
  created_at: string
}

export interface Note {
  id: number
  title: string
  content: string | null
  user_id: number
  created_at: string
  updated_at: string | null
}

export interface Document {
  id: number
  title: string
  source: string
  source_type: "pdf" | "url"
  user_id: number
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface ChatMessage {
  role: "user" | "assistant"
  content: string
}