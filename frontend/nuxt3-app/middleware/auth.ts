export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/auth/login')
    }
    // Ролевые редиректы на индексах дашбордов обрабатывают role.global.ts и ролевые middleware
    void to
  }
})
