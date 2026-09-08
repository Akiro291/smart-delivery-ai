<template>
  <div class="space-y-8">
    <!-- Приветствие -->
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Здравствуйте, {{ authStore.userName }}! 👋</h1>
      <p class="text-gray-500 text-sm mt-1">Сводка по платформе на сегодня</p>
    </div>

    <!-- Статистика -->
    <div v-if="stats" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <UiStat label="Всего заказов" :value="stats.total" icon="📦" tone="indigo" hint="за всё время" />
      <UiStat label="Доставлено" :value="stats.by_status.COMPLETED || 0" icon="✅" tone="emerald" hint="успешно закрыто" />
      <UiStat label="Активных" :value="stats.active" icon="🚚" tone="amber" hint="в работе сейчас" />
      <UiStat label="Выручка" :value="formatMoney(stats.completed_revenue) + ' ₽'" icon="💰" tone="violet" hint="по доставленным" />
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <div v-for="i in 4" :key="i" class="h-28 rounded-xl bg-gray-100 animate-pulse" />
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- Последние заказы -->
      <div class="lg:col-span-3">
        <div class="card">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="font-semibold text-gray-800">Последние заказы</h3>
            <NuxtLink to="/dashboard/orders" class="text-sm font-medium text-brand-600 hover:text-brand-700">
              Все заказы →
            </NuxtLink>
          </div>
          <div v-if="recentOrders.length" class="divide-y divide-gray-50">
            <NuxtLink
              v-for="order in recentOrders"
              :key="order.id"
              to="/dashboard/orders"
              class="flex items-center justify-between px-6 py-4 hover:bg-gray-50/70 transition-colors"
            >
              <div class="min-w-0">
                <p class="font-medium text-gray-800 text-sm">Заказ #{{ order.id }}</p>
                <p class="text-xs text-gray-500 truncate mt-0.5">{{ order.from_address }} → {{ order.to_address }}</p>
              </div>
              <div class="flex items-center gap-3 flex-shrink-0 ml-4">
                <span class="font-semibold text-sm hidden sm:block">{{ formatMoney(order.total_amount) }} ₽</span>
                <UiStatusBadge :status="order.status" />
              </div>
            </NuxtLink>
          </div>
          <UiSpinner v-else-if="isLoading" label="Загрузка заказов…" />
          <UiEmptyState v-else icon="📦" title="Заказов пока нет" description="Первые заказы появятся здесь сразу после оформления">
            <NuxtLink to="/dashboard/orders" class="btn-primary">Перейти к заказам</NuxtLink>
          </UiEmptyState>
        </div>
      </div>

      <!-- Распределение по статусам -->
      <div class="lg:col-span-2 space-y-6">
        <div class="card p-6">
          <h3 class="font-semibold text-gray-800 mb-5">По статусам</h3>
          <div class="space-y-3.5">
            <div v-for="row in statusRows" :key="row.status" class="flex items-center gap-3">
              <span class="w-24 text-xs text-gray-500 flex-shrink-0">{{ row.label }}</span>
              <div class="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-700" :class="row.bar" :style="{ width: row.percent + '%' }" />
              </div>
              <span class="w-8 text-right text-xs font-bold text-gray-700">{{ row.count }}</span>
            </div>
          </div>
        </div>

        <div class="card p-6">
          <h3 class="font-semibold text-gray-800 mb-4">Быстрые действия</h3>
          <div class="grid grid-cols-2 gap-3">
            <NuxtLink v-for="action in quickActions" :key="action.to" :to="action.to" class="group flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-100 hover:border-brand-200 hover:bg-brand-50/50 transition-all">
              <span class="text-2xl group-hover:scale-110 transition-transform">{{ action.icon }}</span>
              <span class="text-xs font-medium text-gray-600 group-hover:text-brand-700">{{ action.label }}</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

interface Order {
  id: number
  status: string
  total_amount: number
  from_address: string
  to_address: string
}

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
const stats = ref<{ total: number; by_status: Record<string, number>; completed_revenue: number; active: number } | null>(null)
const recentOrders = ref<Order[]>([])
const isLoading = ref(true)

onMounted(async () => {
  const [statsData, ordersData] = await Promise.all([
    ordersStore.fetchStats(),
    ordersStore.fetchOrders(0, 6),
  ])
  stats.value = statsData
  recentOrders.value = (ordersData as unknown as Order[]) || []
  isLoading.value = false
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

const quickActions = [
  { icon: '📋', label: 'Заказы', to: '/dashboard/orders' },
  { icon: '🛒', label: 'Товары', to: '/dashboard/products' },
  { icon: '👥', label: 'Клиенты', to: '/dashboard/clients' },
  { icon: '🤖', label: 'AI-чат', to: '/dashboard/ai' },
]
</script>
