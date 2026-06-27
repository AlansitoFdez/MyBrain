import api from "./api"
import { AuthResponse, User } from "@/types"

export const login = async (email: string, password: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>("/auth/login", { email, password })
  localStorage.setItem("token", response.data.access_token)
  return response.data
}

export const register = async (email: string, username: string, password: string): Promise<User> => {
  const response = await api.post<User>("/auth/register", { email, username, password })
  return response.data
}

export const logout = () => {
  localStorage.removeItem("token")
  window.location.href = "/auth"
}

export const getMe = async (): Promise<User> => {
  const response = await api.get<User>("/auth/me")
  return response.data
}

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem("token")
}