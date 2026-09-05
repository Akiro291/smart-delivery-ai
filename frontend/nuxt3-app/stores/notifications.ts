// Notification store
import { defineStore } from 'pinia'

interface Notification {
  id: number
  user_id: number
  title: string
  message: string
  type: string
  status: string
  meta_data: string | null
  created_at: string | null
  updated_at: string | null
}

interface NotificationState {
  notifications: Notification[]
  unreadCount: number
  isLoading: boolean
  error: string | null
}

export const useNotificationsStore = defineStore('notifications', {
  state: (): NotificationState => ({
    notifications: [],
    unreadCount: 0,
    isLoading: false,
    error: null,
  }),

  getters: {
    getNotificationById: (state) => (id: number) => {
      return state.notifications.find((n) => n.id === id)
    },
    getUnreadNotifications: (state) => {
      return state.notifications.filter((n) => n.status !== 'READ')
    },
  },

  actions: {
    async fetchNotifications(skip = 0, limit = 100) {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const notifications = await $fetch(`${apiBase}/notifications/`, {
          method: 'GET',
          query: { skip, limit },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.notifications = notifications as Notification[]
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch notifications'
      } finally {
        this.isLoading = false
      }
    },

    async fetchUnreadCount() {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const count = await $fetch(`${apiBase}/notifications/unread-count`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.unreadCount = count as number
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch unread count'
      }
    },

    async markAsRead(notificationId: number) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        await $fetch(`${apiBase}/notifications/${notificationId}/read`, {
          method: 'PATCH',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        const notification = this.notifications.find((n) => n.id === notificationId)
        if (notification) {
          notification.status = 'READ'
        }
        this.unreadCount = Math.max(0, this.unreadCount - 1)
      } catch (err: any) {
        this.error = err.message || 'Failed to mark notification as read'
      }
    },

    async markAllAsRead() {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        await $fetch(`${apiBase}/notifications/mark-all-read`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.notifications.forEach((n) => {
          n.status = 'READ'
        })
        this.unreadCount = 0
      } catch (err: any) {
        this.error = err.message || 'Failed to mark all notifications as read'
      }
    },

    async createNotification(data: { title: string; message: string; type: string }) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const notification = await $fetch(`${apiBase}/notifications/`, {
          method: 'POST',
          body: data,
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        this.notifications.unshift(notification as Notification)
      } catch (err: any) {
        this.error = err.message || 'Failed to create notification'
      }
    },
  },
})
