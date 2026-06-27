import api from "./api"
import { User } from "@/types"

export const login = async (email: string, password: string): Promise<void> => {
  await api.post("/auth/login", { email, password })
}

export const register = async (email: string, username: string, password: string): Promise<User> => {
  const response = await api.post<User>("/auth/register", { email, username, password })
  return response.data
}

export const logout = async (): Promise<void> => {
  await api.post("/auth/logout")
  window.location.href = "/auth"
}

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>("/auth/me")
  return response.data
}

export const isAuthenticated = async (): Promise<boolean> => {
  try {
    await getMe()
    return true
  } catch {
    return false
  }
}