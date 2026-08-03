export default defineNuxtRouteMiddleware((to) => {
  // Не перенаправляем со страниц авторизации
  if (to.path.startsWith('/auth/')) return

  if (import.meta.client) {
    const token = localStorage.getItem('token')
    if (token) {
      const role = localStorage.getItem('user_role')
      // Перенаправляем на дашборд по роли
      if (role === 'ADMIN') {
        return navigateTo('/admin')
      } else if (role === 'COURIER') {
        return navigateTo('/courier')
      } else {
        return navigateTo('/customer')
      }
    }
  }
})
