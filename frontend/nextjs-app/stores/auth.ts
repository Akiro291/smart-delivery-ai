// Auth store
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),
  
  actions: {
    setUser(user: User | null) {
      this.user = user
    },
    setToken(token: string | null) {
      this.token = token
    },
    setAuthenticated(authenticated: boolean) {
      this.isAuthenticated = authenticated
    },
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    }
  }
})