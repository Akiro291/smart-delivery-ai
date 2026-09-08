// Ролевой middleware для CUSTOMER-страниц
export default defineNuxtRouteMiddleware(() => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')

    if (!token) {
      return navigateTo('/auth/login')
    }

    if (role !== 'CUSTOMER') {
      // Уводим на дашборд своей роли (не на /customer — иначе цикл)
      const ROLE_HOME: Record<string, string> = {
        ADMIN: '/admin',
        MANAGER: '/dashboard',
        COURIER: '/courier',
      }
      return navigateTo((role && ROLE_HOME[role]) || '/auth/login')
    }
  }
})
