// WebSocket plugin
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  return {
    provide: {
      ws: null,
    },
  }
})
