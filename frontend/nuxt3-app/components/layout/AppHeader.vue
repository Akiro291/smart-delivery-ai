<template>
  <header class="h-16 bg-white/80 backdrop-blur-lg border-b border-gray-100 flex items-center justify-between px-4 sm:px-6 sticky top-0 z-20">
    <div class="flex items-center gap-3">
      <button class="lg:hidden text-gray-500 hover:text-gray-800 transition-colors" @click="$emit('toggle-sidebar')" aria-label="Меню">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <div>
        <h2 class="font-semibold text-gray-800 leading-tight">{{ title }}</h2>
        <p v-if="subtitle" class="text-xs text-gray-400 hidden sm:block">{{ subtitle }}</p>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <!-- Уведомления -->
      <div class="relative">
        <button
          class="relative h-10 w-10 rounded-full hover:bg-gray-100 flex items-center justify-center text-gray-500 transition-colors"
          @click="panelOpen = !panelOpen"
          aria-label="Уведомления"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2c0 .5-.2 1-.6 1.4L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
          <span
            v-if="notificationsStore.unreadCount > 0"
            class="absolute -top-0.5 -right-0.5 h-5 min-w-5 px-1 rounded-full bg-red-500 text-white text-[10px] font-bold flex items-center justify-center"
          >
            {{ notificationsStore.unreadCount > 9 ? '9+' : notificationsStore.unreadCount }}
          </span>
        </button>

        <transition name="dropdown">
          <div
            v-if="panelOpen"
            class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-card-hover border border-gray-100 z-50 overflow-hidden"
          >
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
              <span class="font-semibold text-sm">Уведомления</span>
              <button
                v-if="notificationsStore.unreadCount > 0"
                class="text-xs text-brand-600 hover:text-brand-700 font-medium"
                @click="notificationsStore.markAllAsRead()"
              >
                Прочитать все
              </button>
            </div>
            <div class="max-h-80 overflow-y-auto divide-y divide-gray-50">
              <div v-if="notificationsStore.isLoading" class="p-6 text-center text-sm text-gray-400">Загрузка…</div>
              <div v-else-if="notificationsStore.notifications.length === 0" class="p-6 text-center text-sm text-gray-400">
                Пока нет уведомлений
              </div>
              <button
                v-for="n in notificationsStore.notifications.slice(0, 8)"
                :key="n.id"
                class="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors flex gap-3"
                :class="n.status !== 'READ' ? 'bg-brand-50/40' : ''"
                @click="openNotification(n)"
              >
                <span class="mt-0.5 flex-shrink-0">{{ n.status === 'READ' ? '📭' : '📬' }}</span>
                <span class="min-w-0">
                  <span class="block text-sm font-medium text-gray-800 truncate">{{ n.title }}</span>
                  <span class="block text-xs text-gray-500 line-clamp-2">{{ n.message }}</span>
                </span>
              </button>
            </div>
          </div>
        </transition>
      </div>

      <!-- Профиль -->
      <div class="relative group">
        <button class="flex items-center gap-2.5 pl-1 pr-2 py-1.5 rounded-full hover:bg-gray-100 transition-colors">
          <div class="h-8 w-8 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white text-sm font-bold flex items-center justify-center">
            {{ initial }}
          </div>
          <span class="hidden md:block text-sm font-medium text-gray-700 max-w-32 truncate">{{ authStore.userName }}</span>
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        <div class="hidden group-hover:block absolute right-0 mt-1 w-48 bg-white rounded-xl shadow-card-hover border border-gray-100 z-50 overflow-hidden">
          <NuxtLink :to="profileLink" class="flex items-center gap-2.5 px-4 py-3 text-sm hover:bg-gray-50 transition-colors">
            <span>👤</span> Профиль
          </NuxtLink>
          <button @click="logout" class="w-full flex items-center gap-2.5 px-4 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors text-left">
            <span>🚪</span> Выйти
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
const props = defineProps<{
  title: string
  subtitle?: string
  profileLink?: string
}>()

defineEmits(['toggle-sidebar'])

const authStore = useAuthStore()
const notificationsStore = useNotificationsStore()
const panelOpen = ref(false)

const initial = computed(() => (authStore.userName || 'U')[0]?.toUpperCase() || 'U')

const profileLink = computed(() => {
  const role = authStore.userRole
  if (role === 'COURIER') return '/courier/profile'
  if (role === 'CUSTOMER') return '/customer/profile'
  if (role === 'ADMIN') return '/profile'
  return '/profile'
})

onMounted(() => {
  notificationsStore.fetchUnreadCount()
  notificationsStore.fetchNotifications()
})

async function openNotification(n: { id: number; status: string }) {
  if (n.status !== 'READ') {
    await notificationsStore.markAsRead(n.id)
  }
}

async function logout() {
  await authStore.logout()
  navigateTo('/auth/login')
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
