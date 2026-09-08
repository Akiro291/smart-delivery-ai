// Возвращает домашнюю страницу для роли пользователя
export const ROLE_HOME: Record<string, string> = {
  ADMIN: '/admin',
  MANAGER: '/dashboard',
  COURIER: '/courier',
  CUSTOMER: '/customer',
}

export function useRoleHome(role?: string | null): string {
  if (!role) return '/auth/login'
  return ROLE_HOME[role] || '/customer'
}
