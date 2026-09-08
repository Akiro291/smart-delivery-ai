<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Панель администратора</h1>
      <p class="text-gray-500 text-sm mt-1">Состояние платформы в целом</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <UiStat label="Всего пользователей" :value="counts.total" icon="👥" tone="indigo" />
      <UiStat label="Клиентов" :value="counts.customers" icon="🛍️" tone="cyan" />
      <UiStat label="Курьеров" :value="counts.couriers" icon="🚚" tone="emerald" />
      <UiStat label="Администраторов" :value="counts.admins" icon="👑" tone="red" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card p-6">
        <h3 class="font-semibold text-gray-800 mb-5">Быстрые действия</h3>
        <div class="grid grid-cols-2 gap-3">
          <NuxtLink v-for="action in actions" :key="action.to" :to="action.to" class="group flex flex-col items-center gap-2 p-5 rounded-xl border border-gray-100 hover:border-brand-200 hover:bg-brand-50/50 transition-all">
            <span class="text-2xl group-hover:scale-110 transition-transform">{{ action.icon }}</span>
            <span class="text-xs font-medium text-gray-600 group-hover:text-brand-700">{{ action.label }}</span>
          </NuxtLink>
        </div>
      </div>

      <div class="card p-6">
        <h3 class="font-semibold text-gray-800 mb-5">Заказы платформы</h3>
        <div v-if="stats" class="space-y-3.5">
          <div v-for="row in statusRows" :key="row.status" class="flex items-center gap-3">
            <span class="w-24 text-xs text-gray-500 flex-shrink-0">{{ row.label }}</span>
            <div class="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-700" :class="row.bar" :style="{ width: row.percent + '%' }" />
            </div>
            <span class="w-8 text-right text-xs font-bold text-gray-700">{{ row.count }}</span>
          </div>
        </div>
        <UiSpinner v-else label="Загрузка статистики…" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

const STATUS_BARS: Record<string, string> = {
  PENDING: 'bg-amber-400',
  CONFIRMED: 'bg-blue-500',
  ASSIGNED: 'bg-indigo-500',
  IN_PROGRESS: 'bg-cyan-500',
  COMPLETED: 'bg-emerald-500',
  CANCELLED: 'bg-rose-400',
}

const authStore = useAuthStore()
const ordersStore = useOrdersStore()
const apiBase = useRuntimeConfig().public.apiBase
const counts = ref({ total: 0, customers: 0, couriers: 0, admins: 0 })
const stats = ref<{ by_status: Record<string, number> } | null>(null)

onMounted(async () => {
  const token = authStore.token || localStorage.getItem('token')
  if (!token) return navigateTo('/auth/login')
  try {
    counts.value = (await $fetch(`${apiBase}/users/count`, {
      headers: { Authorization: `Bearer ${token}` },
    })) as typeof counts.value
  } catch {}
  stats.value = await ordersStore.fetchStats()
})

const statusRows = computed(() => {
  const byStatus = stats.value?.by_status || {}
  const total = Object.values(byStatus).reduce((a, b) => a + b, 0) || 1
  return Object.keys(ORDER_STATUS_META).map((status) => ({
    status,
    label: ORDER_STATUS_META[status].label,
    count: byStatus[status] || 0,
    percent: Math.round(((byStatus[status] || 0) / total) * 100),
    bar: STATUS_BARS[status] || 'bg-gray-300',
  }))
})

const actions = [
  { icon: '👥', label: 'Пользователи', to: '/admin/users' },
  { icon: '🔑', label: 'Роли', to: '/admin/roles' },
  { icon: '📋', label: 'Заказы', to: '/admin/orders' },
  { icon: '🛒', label: 'Товары', to: '/admin/products' },
]
</script>
