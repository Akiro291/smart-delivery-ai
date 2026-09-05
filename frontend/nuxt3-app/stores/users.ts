// User store
import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  role: 'CUSTOMER' | 'COURIER' | 'ADMIN'
  is_active: boolean
  is_superuser: boolean
  created_at: string | null
}

interface UserState {
  users: User[]
  currentUser: User | null
  isLoading: boolean
  error: string | null
}

export const useUsersStore = defineStore('users', {
  state: (): UserState => ({
    users: [],
    currentUser: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    getUserById: (state) => (id: number) => {
      return state.users.find((u) => u.id === id)
    },
  },

  actions: {
    async fetchUsers(skip = 0, limit = 100, role?: string) {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const query: Record<string, string | number> = { skip, limit }
        if (role) query.role = role

        const users = await $fetch(`${apiBase}/users/`, {
          method: 'GET',
          query,
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.users = users as User[]
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch users'
      } finally {
        this.isLoading = false
      }
    },

    async fetchUser(userId: number) {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const user = await $fetch(`${apiBase}/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.currentUser = user as User
        return user
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch user'
        return null
      } finally {
        this.isLoading = false
      }
    },

    async updateUserRole(userId: number, role: string) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const user = await $fetch(`${apiBase}/users/${userId}/role`, {
          method: 'PUT',
          body: { role },
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        const index = this.users.findIndex((u) => u.id === userId)
        if (index !== -1) {
          this.users[index] = user as User
        }
        return user
      } catch (err: any) {
        this.error = err.message || 'Failed to update user role'
        throw err
      }
    },

    async toggleUserStatus(userId: number, isActive: boolean) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const user = await $fetch(`${apiBase}/users/${userId}/status`, {
          method: 'PUT',
          body: { is_active: isActive },
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        const index = this.users.findIndex((u) => u.id === userId)
        if (index !== -1) {
          this.users[index] = user as User
        }
        return user
      } catch (err: any) {
        this.error = err.message || 'Failed to toggle user status'
        throw err
      }
    },
  },
})
