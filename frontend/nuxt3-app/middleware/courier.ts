// Ролевой middleware для COURIER-страниц
export default defineNuxtRouteMiddleware(() => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')

    if (!token) {
      return navigateTo('/auth/login')
    }

    if (role !== 'COURIER') {
      const ROLE_HOME: Record<string, string> = {
        ADMIN: '/admin',
        MANAGER: '/dashboard',
        CUSTOMER: '/customer',
      }
      return navigateTo((role && ROLE_HOME[role]) || '/auth/login')
    }
  }
})
