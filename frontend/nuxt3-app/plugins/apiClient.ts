// apiClient plugin: экспортирует базовые утилиты API для не-Vue контекстов
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const apiBase = (config.public.apiBase as string) || 'http://localhost:8000/api/v1'
  return {
    provide: {
      apiClient: {
        baseURL: apiBase,
        token: () => (import.meta.client ? localStorage.getItem('token') : null),
      },
    },
  }
})
