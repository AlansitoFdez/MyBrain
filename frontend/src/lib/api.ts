import axios from "axios"

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,  // esto hace que axios envíe las cookies automáticamente
})

export default api