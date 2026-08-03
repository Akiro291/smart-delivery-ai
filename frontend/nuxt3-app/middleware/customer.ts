export default defineNuxtRouteMiddleware(() => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')

    if (!token) {
      return navigateTo('/auth/login')
    }

    if (role !== 'CUSTOMER') {
      return navigateTo('/customer')
    }
  }
})
