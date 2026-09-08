// Глобальный ролевой middleware: перенаправляет с индекса дашборда на панель роли
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')

    if (!token) return

    const ROLE_HOME: Record<string, string> = {
      ADMIN: '/admin',
      MANAGER: '/dashboard',
      COURIER: '/courier',
      CUSTOMER: '/customer',
    }

    if (to.path === '/dashboard') {
      return navigateTo((role && ROLE_HOME[role]) || '/customer')
    }
  }
})
