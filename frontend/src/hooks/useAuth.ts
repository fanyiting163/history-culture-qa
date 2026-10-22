import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'

export function useAuth() {
  const store = useAuthStore()
  const { loggedIn } = storeToRefs(store)

  function logout() {
    store.setToken(null)
  }

  return { loggedIn, logout }
}
