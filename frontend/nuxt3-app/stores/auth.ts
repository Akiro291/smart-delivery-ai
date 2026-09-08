// Auth store
import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  role: 'CUSTOMER' | 'COURIER' | 'MANAGER' | 'ADMIN'
  is_active: boolean
  is_superuser: boolean
  created_at: string | null
}

interface AuthState {
  token: string | null
  refreshToken: string | null
  user: User | null
  isLoading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: import.meta.client ? localStorage.getItem('token') : null,
    refreshToken: import.meta.client ? localStorage.getItem('refresh_token') : null,
    user: import.meta.client ? (() => {
      const userStr = localStorage.getItem('user_data')
      if (userStr) {
        try { return JSON.parse(userStr) } catch { return null }
      }
      return null
    })() : null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
    isAdmin: (state) => state.user?.role === 'ADMIN',
    isManager: (state) => state.user?.role === 'MANAGER',
    isCourier: (state) => state.user?.role === 'COURIER',
    isCustomer: (state) => state.user?.role === 'CUSTOMER',
    userName: (state) => state.user?.full_name || state.user?.email?.split('@')[0] || '',
  },

  actions: {
    async login(email: string, password: string) {
      this.isLoading = true
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)

        const apiBase = useRuntimeConfig().public.apiBase
        const response = await $fetch(`${apiBase}/auth/login`, {
          method: 'POST',
          body: formData,
        })

        this.token = response.access_token
        this.refreshToken = response.refresh_token
        this.user = response.user as User

        if (import.meta.client) {
          localStorage.setItem('token', this.token!)
          localStorage.setItem('refresh_token', this.refreshToken!)
          localStorage.setItem('user_role', this.user!.role)
          localStorage.setItem('user_id', String(this.user!.id))
          localStorage.setItem('user_name', this.user!.full_name || this.user!.email)
          localStorage.setItem('user_data', JSON.stringify(this.user))
        }

        return response
      } finally {
        this.isLoading = false
      }
    },

    async register(full_name: string, email: string, password: string, phone?: string) {
      this.isLoading = true
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        console.log('Register API URL:', `${apiBase}/auth/register`)
        const response = await $fetch(`${apiBase}/auth/register`, {
          method: 'POST',
          body: {
            full_name,
            email,
            password,
            phone: phone || null,
          },
          onError(error: any) {
            console.error('$fetch error:', error)
          }
        })

        this.token = response.access_token
        this.refreshToken = response.refresh_token
        this.user = response.user as User

        if (import.meta.client) {
          localStorage.setItem('token', this.token!)
          localStorage.setItem('refresh_token', this.refreshToken!)
          localStorage.setItem('user_role', this.user!.role)
          localStorage.setItem('user_id', String(this.user!.id))
          localStorage.setItem('user_name', this.user!.full_name || this.user!.email)
          localStorage.setItem('user_data', JSON.stringify(this.user))
        }

        return response
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      this.token = null
      this.refreshToken = null
      this.user = null

      if (import.meta.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_role')
        localStorage.removeItem('user_id')
        localStorage.removeItem('user_name')
        localStorage.removeItem('user_data')
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) return false

      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const response = await $fetch(`${apiBase}/auth/refresh`, {
          method: 'POST',
          body: { refresh_token: this.refreshToken },
        })

        this.token = response.access_token
        this.refreshToken = response.refresh_token

        if (import.meta.client) {
          localStorage.setItem('token', this.token!)
          localStorage.setItem('refresh_token', this.refreshToken!)
        }

        return true
      } catch {
        await this.logout()
        return false
      }
    },

    async fetchUser() {
      if (!this.token) return

      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const user = await $fetch(`${apiBase}/auth/me`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })

        this.user = user as User

        if (import.meta.client) {
          localStorage.setItem('user_role', user.role)
          localStorage.setItem('user_name', user.full_name || user.email)
          localStorage.setItem('user_data', JSON.stringify(user))
        }
      } catch {
        await this.refreshAccessToken()
      }
    },

    async init() {
      if (this.token && import.meta.client) {
        await this.fetchUser()
      }
    },

    async requestRoleChange(role: 'COURIER' | 'ADMIN', reason?: string) {
      const apiBase = useRuntimeConfig().public.apiBase
      return await $fetch(`${apiBase}/users/role-request`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
        body: {
          requested_role: role,
          reason: reason || null,
        },
      })
    },

    async getMyRoleRequest() {
      const apiBase = useRuntimeConfig().public.apiBase
      return await $fetch(`${apiBase}/users/me/role-request`, {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      })
    },
  },
})
