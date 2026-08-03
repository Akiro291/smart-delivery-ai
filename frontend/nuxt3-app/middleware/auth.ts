export default defineNuxtRouteMiddleware((to) => {
  if (import.meta.client) {
    const token = localStorage.getItem('token')
    if (!token) {
      return navigateTo('/auth/login')
    }
    
    // Don't redirect if user is already authenticated and going to their dashboard
    const role = localStorage.getItem('user_role')
    const dashboardRoutes = ['/admin', '/courier', '/customer', '/dashboard']
    
    if (dashboardRoutes.includes(to.path)) {
      // Let role-specific middleware handle the routing
      return
    }
  }
})
