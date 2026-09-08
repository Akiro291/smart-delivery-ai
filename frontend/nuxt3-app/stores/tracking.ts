// Tracking store: real-time координаты и статусы доставки
import { defineStore } from 'pinia'

interface TrackingState {
  // order_id -> последнее событие tracking
  byOrder: Record<number, { lat: number | null; lon: number | null; progress: number; estimated: number | null }>
  lastOrderEvent: { type: string; orderId: number; status?: string } | null
}

export const useTrackingStore = defineStore('tracking', {
  state: (): TrackingState => ({
    byOrder: {},
    lastOrderEvent: null,
  }),

  getters: {
    getTracking: (state) => (orderId: number) => state.byOrder[orderId] || null,
  },

  actions: {
    handleWsEvent(event: { type: string; payload: Record<string, unknown> }) {
      const payload = event.payload || {}
      if (event.type === 'tracking.updated') {
        const orderId = Number(payload.order_id)
        if (!orderId) return
        this.byOrder[orderId] = {
          lat: (payload.lat as number | null) ?? null,
          lon: (payload.lon as number | null) ?? null,
          progress: Number(payload.progress || 0),
          estimated: (payload.estimated_delivery_time as number | null) ?? null,
        }
      } else if (event.type === 'order.status_changed' || event.type === 'order.assigned') {
        const orderId = Number(payload.order_id)
        if (!orderId) return
        this.lastOrderEvent = { type: event.type, orderId, status: payload.status as string }
      }
    },

    // Подключение к WebSocket-событиям (вызывать один раз на клиенте)
    initWs() {
      if (import.meta.server) return
      const $ws = (useNuxtApp().$ws as { on?: (l: unknown) => () => void } | undefined)
      if (!$ws?.on) return
      $ws.on((event: { type: string; payload: Record<string, unknown> }) => {
        this.handleWsEvent(event)
      })
    },
  },
})
