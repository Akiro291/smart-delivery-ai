export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/auth/login')
    }
  }
})
