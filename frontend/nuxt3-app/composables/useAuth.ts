// Auth composable
import { useAuthStore } from '~/stores/auth'

export const useAuth = () => {
  const authStore = useAuthStore()

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const userRole = computed(() => authStore.userRole)
  const isAdmin = computed(() => authStore.isAdmin)
  const isCourier = computed(() => authStore.isCourier)
  const isCustomer = computed(() => authStore.isCustomer)
  const userName = computed(() => authStore.userName)

  const login = async (email: string, password: string) => {
    return await authStore.login(email, password)
  }

  const register = async (full_name: string, email: string, password: string, phone?: string) => {
    return await authStore.register(full_name, email, password, phone)
  }

  const logout = async () => {
    await authStore.logout()
    await navigateTo('/auth/login')
  }

  const refreshToken = async () => {
    return await authStore.refreshAccessToken()
  }

  const init = async () => {
    await authStore.init()
  }

  const requestRoleChange = async (role: 'COURIER' | 'ADMIN', reason?: string) => {
    return await authStore.requestRoleChange(role, reason)
  }

  const getMyRoleRequest = async () => {
    return await authStore.getMyRoleRequest()
  }

  return {
    isAuthenticated,
    userRole,
    isAdmin,
    isCourier,
    isCustomer,
    userName,
    login,
    register,
    logout,
    refreshToken,
    init,
    requestRoleChange,
    getMyRoleRequest,
  }
}
