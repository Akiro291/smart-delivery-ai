// Notification store
interface NotificationState {
  notifications: Notification[]
  unreadCount: number
  loading: boolean
}

export const useNotificationStore = defineStore('notifications', {
  state: (): NotificationState => ({
    notifications: [],
    unreadCount: 0,
    loading: false
  }),
  
  actions: {
    setNotifications(notifications: Notification[]) {
      this.notifications = notifications
    },
    setUnreadCount(count: number) {
      this.unreadCount = count
    },
    setLoading(loading: boolean) {
      this.loading = loading
    }
  }
})