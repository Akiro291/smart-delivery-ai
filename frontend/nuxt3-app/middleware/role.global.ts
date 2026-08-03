// Global role middleware - redirects users based on their role
export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    const role = localStorage.getItem('user_role')
    
    if (!token) return
    
    // Redirect admin to /admin, courier to /courier, customer to /customer
    if (to.path === '/dashboard') {
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
