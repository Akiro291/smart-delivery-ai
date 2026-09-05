// Notification composable
import { useNotificationsStore } from '~/stores/notifications'

export const useNotification = () => {
  const notificationsStore = useNotificationsStore()

  const notifications = computed(() => notificationsStore.notifications)
  const unreadCount = computed(() => notificationsStore.unreadCount)

  const fetchNotifications = async (skip = 0, limit = 100) => {
    await notificationsStore.fetchNotifications(skip, limit)
  }

  const fetchUnreadCount = async () => {
    await notificationsStore.fetchUnreadCount()
  }

  const markAsRead = async (notificationId: number) => {
    await notificationsStore.markAsRead(notificationId)
  }

  const markAllAsRead = async () => {
    await notificationsStore.markAllAsRead()
  }

  const createNotification = async (data: { title: string; message: string; type: string }) => {
    await notificationsStore.createNotification(data)
  }

  return {
    notifications,
    unreadCount,
    fetchNotifications,
    fetchUnreadCount,
    markAsRead,
    markAllAsRead,
    createNotification,
  }
}
