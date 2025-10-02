import type { UserPublic } from "@client/schemas"
import { createContext } from "react"

// 👇 Tu peux adapter ce type si tu veux exposer `user` aussi
interface AuthContextValues {
  isAuthenticated: boolean
  isInitialized: boolean
  user: UserPublic | null
  setIsAuthenticated: (auth: boolean) => void
  setUser: (user: UserPublic | null) => void
}

export const AuthContext = createContext<AuthContextValues | null>(null)