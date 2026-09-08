export function useApi() {
  const config = useRuntimeConfig()
  const API_BASE = config.public.apiBase || 'http://localhost:8000/api/v1'
  const _token = () => (import.meta.client ? localStorage.getItem('token') : null)
  return {
    async get(path: string, options: Record<string, unknown> = {}) {
      const token = _token()
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
      const token = _token()
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
    async postForm(path: string, body: URLSearchParams | FormData) {
      const token = _token()
      return await $fetch(path, {
        baseURL: API_BASE,
        method: 'POST',
        body,
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      })
    },
    async put(path: string, body: unknown, options: Record<string, unknown> = {}) {
      const token = _token()
      return await $fetch(path, {
        baseURL: API_BASE,
        method: 'PUT',
        body,
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
          ...options.headers,
        },
        ...options,
      })
    },
    async patch(path: string, body: unknown, options: Record<string, unknown> = {}) {
      const token = _token()
      return await $fetch(path, {
        baseURL: API_BASE,
        method: 'PATCH',
        body,
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
          ...options.headers,
        },
        ...options,
      })
    },
    async delete(path: string, options: Record<string, unknown> = {}) {
      const token = _token()
      return await $fetch(path, {
        baseURL: API_BASE,
        method: 'DELETE',
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
          ...options.headers,
        },
        ...options,
      })
    },
  }
}
