// API client plugin
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  return {
    provide: {
      api: {
        baseURL: config.public.apiBase || 'http://localhost:8000/api/v1',
      },
    },
  }
})
