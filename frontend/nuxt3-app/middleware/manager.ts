// Ролевой middleware для панели менеджера (/dashboard/**): MANAGER или ADMIN
export default defineNuxtRouteMiddleware(() => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')

    if (!token) {
      return navigateTo('/auth/login')
    }

    if (role !== 'MANAGER' && role !== 'ADMIN') {
      const ROLE_HOME: Record<string, string> = {
        COURIER: '/courier',
        CUSTOMER: '/customer',
      }
      return navigateTo((role && ROLE_HOME[role]) || '/auth/login')
    }
  }
})
