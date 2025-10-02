// src/context/AuthProvider.tsx

import { useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'

import { usersReadMe } from '@client/services/users'
import type { UserPublic } from '@client/schemas'
import { AuthContext } from './authContext'




interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isInitialized, setIsInitialized] = useState(false)
  const [user, setUser] = useState<UserPublic | null>(null)

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        setIsInitialized(true)
        return
      }

      try {
        const me = await usersReadMe()
        setUser(me)
        setIsAuthenticated(true)
      } catch {
        setUser(null)
        setIsAuthenticated(false)
      } finally {
        setIsInitialized(true)
      }
    }

    init()
  }, [])

  const value = useMemo(
    () => ({
      isAuthenticated,
      isInitialized,
      user,
      setIsAuthenticated,
      setUser,
    }),
    [isAuthenticated, isInitialized, user]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

