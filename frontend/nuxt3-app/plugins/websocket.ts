// WebSocket plugin: единое соединение с подписками и переподключением
export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const apiBase = (config.public.apiBase as string) || 'http://localhost:8000/api/v1'
  const wsUrl = (config.public.wsUrl as string) || apiBase.replace(/^http/, 'ws') + '/ws'

  let socket: WebSocket | null = null
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null
  let reconnectDelay = 1000
  const listeners = new Set<(event: { type: string; payload: Record<string, unknown> }) => void>()

  function connect() {
    if (import.meta.server) return
    const token = localStorage.getItem('token')
    if (!token || socket) return

    socket = new WebSocket(`${wsUrl}?token=${encodeURIComponent(token)}`)

    socket.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data)
        listeners.forEach((listener) => listener(parsed))
      } catch {
        // ignore malformed frames
      }
    }

    socket.onclose = () => {
      socket = null
      scheduleReconnect()
    }

    socket.onerror = () => {
      socket?.close()
    }
  }

  function scheduleReconnect() {
    if (reconnectTimer) return
    reconnectTimer = setTimeout(() => {
      reconnectTimer = null
      reconnectDelay = Math.min(reconnectDelay * 2, 30000)
      connect()
    }, reconnectDelay)
  }

  nuxtApp.provide('ws', {
    connect,
    on(listener: (event: { type: string; payload: Record<string, unknown> }) => void) {
      listeners.add(listener)
      connect()
      return () => listeners.delete(listener)
    },
    close() {
      socket?.close()
      socket = null
      if (reconnectTimer) {
        clearTimeout(reconnectTimer)
        reconnectTimer = null
      }
    },
  })
})
