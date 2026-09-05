export function useApi() {
  const config = useRuntimeConfig()
  const API_BASE = config.public.apiBase || 'http://localhost:8000/api/v1'
  return {
    async get(path: string, options: Record<string, unknown> = {}) {
      const token = import.meta.client ? localStorage.getItem('token') : null
      const res = await $fetch(path, {
        baseURL: API_BASE,
        headers: {
          ...options.headers,
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        ...options,
      })
      return res
    },
    async post(path: string, body: unknown, options: Record<string, unknown> = {}) {
      const token = import.meta.client ? localStorage.getItem('token') : null
      const res = await $fetch(path, {
        baseURL: API_BASE,
        method: 'POST',
        body,
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
          ...options.headers,
        },
        ...options,
      })
      return res
    },
    async postForm(path: string, body: URLSearchParams) {
      return await $fetch(path, {
        baseURL: API_BASE,
        method: 'POST',
        body,
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
    },
  }
}
