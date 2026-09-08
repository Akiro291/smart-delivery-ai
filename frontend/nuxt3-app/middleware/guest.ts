// Гостевой middleware: авторизованного пользователя уводим с auth-страниц на его дашборд
export default defineNuxtRouteMiddleware((to) => {
  if (!to.path.startsWith('/auth/')) return

  if (import.meta.client) {
    const token = localStorage.getItem('token')
    if (token) {
      const role = localStorage.getItem('user_role')
      const { useRoleHome } = useRoleHomeModule()
      return navigateTo(useRoleHome(role))
    }
  }
})

// Локальный helper, чтобы не зависеть от автоимпортов внутри middleware
function useRoleHomeModule() {
  const ROLE_HOME: Record<string, string> = {
    ADMIN: '/admin',
    MANAGER: '/dashboard',
    COURIER: '/courier',
    CUSTOMER: '/customer',
  }
  return {
    useRoleHome: (role?: string | null) => (role ? ROLE_HOME[role] || '/customer' : '/auth/login'),
  }
}
