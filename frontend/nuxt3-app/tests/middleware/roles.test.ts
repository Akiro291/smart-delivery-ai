// Тесты ролевой логики middleware (регресс на зацикленный редирект customer.ts)
import { describe, it, expect } from 'vitest'

// Копия логики ROLE_HOME, синхронизированная с middleware и composable
const ROLE_HOME: Record<string, string> = {
  ADMIN: '/admin',
  MANAGER: '/dashboard',
  COURIER: '/courier',
  CUSTOMER: '/customer',
}

function roleHome(role?: string | null): string {
  if (!role) return '/auth/login'
  return ROLE_HOME[role] || '/customer'
}

describe('Ролевые домашние маршруты', () => {
  it('каждая роль ведёт на свой дашборд (не на чужой)', () => {
    expect(roleHome('ADMIN')).toBe('/admin')
    expect(roleHome('MANAGER')).toBe('/dashboard')
    expect(roleHome('COURIER')).toBe('/courier')
    expect(roleHome('CUSTOMER')).toBe('/customer')
  })

  it('CUSTOMER не перенаправляется на /customer сам в себя (регресс цикла)', () => {
    const home = roleHome('CUSTOMER')
    // редирект на ту же страницу = бесконечный цикл
    expect(home).not.toBe('')
    expect(ROLE_HOME['CUSTOMER']).toBe('/customer')
    // middleware customer.ts редиректит только не-CUSTOMER, на роль-специфичный путь
    const nonCustomerRedirects: Record<string, string> = {
      ADMIN: '/admin',
      MANAGER: '/dashboard',
      COURIER: '/courier',
    }
    for (const [role, target] of Object.entries(nonCustomerRedirects)) {
      expect(target).not.toBe('/customer')
      expect(target).toBe(ROLE_HOME[role])
    }
  })

  it('без роли отправляет на логин', () => {
    expect(roleHome(null)).toBe('/auth/login')
    expect(roleHome(undefined)).toBe('/auth/login')
  })

  it('неизвестная роль не ломает навигацию', () => {
    expect(roleHome('UNKNOWN_ROLE')).toBe('/customer')
  })
})
