import { AuthContext } from "provider/authContext"
import { useContext } from "react"
import invariant from 'tiny-invariant'

export const useAuthContext = () => {
  const context = useContext(AuthContext)
  invariant(context, 'useAuthContext must be used within an AuthProvider')
  return context
}