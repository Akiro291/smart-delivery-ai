<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Аналитика</h1>
      <p class="text-gray-500 text-sm mt-1">Динамика и распределение заказов</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <UiStat label="Выручка (доставленные)" :value="formatMoney(stats?.completed_revenue) + ' ₽'" icon="💰" tone="emerald" />
      <UiStat label="Всего заказов" :value="stats?.total || 0" icon="📦" tone="indigo" />
      <UiStat label="Активных заказов" :value="stats?.active || 0" icon="🚚" tone="amber" />
    </div>

    <div class="card p-6">
      <h3 class="font-semibold text-gray-800 mb-5">Заказы по статусам</h3>
      <div class="space-y-4">
        <div v-for="item in statusRows" :key="item.status" class="flex items-center gap-4">
          <span class="w-28 text-xs text-gray-500 flex-shrink-0">{{ item.label }}</span>
          <div class="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all duration-700" :class="item.bar" :style="{ width: item.percent + '%' }" />
          </div>
          <span class="w-10 text-right text-sm font-bold text-gray-700">{{ item.count }}</span>
        </div>
      </div>
    </div>

    <div class="card p-6">
      <h3 class="font-semibold text-gray-800 mb-6">Заказы по дням (последние 14)</h3>
      <div class="flex items-end gap-1.5 h-48">
        <div v-for="(day, i) in chartData" :key="i" class="flex-1 flex flex-col items-center gap-2 group">
          <div
            :style="{ height: chartBarHeight(day.count) }"
            class="w-full max-w-8 bg-gradient-to-t from-brand-600 to-brand-400 rounded-t-md group-hover:from-brand-700 group-hover:to-brand-500 transition-colors"
            :title="`${day.count} заказов`"
          />
          <span class="text-[10px] text-gray-400">{{ day.label }}</span>
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
  created_at: string | null
}

const STATUS_BARS: Record<string, string> = {
  PENDING: 'bg-amber-400',
  CONFIRMED: 'bg-blue-500',
  ASSIGNED: 'bg-indigo-500',
  IN_PROGRESS: 'bg-cyan-500',
  COMPLETED: 'bg-emerald-500',
  CANCELLED: 'bg-rose-400',
}

const ordersStore = useOrdersStore()
const stats = ref<{ total: number; by_status: Record<string, number>; completed_revenue: number; active: number } | null>(null)
const orders = ref<Order[]>([])
const isLoading = ref(true)

onMounted(async () => {
  const [statsData, ordersData] = await Promise.all([
    ordersStore.fetchStats(),
    ordersStore.fetchOrders(0, 200),
  ])
  stats.value = statsData
  orders.value = (ordersData as unknown as Order[]) || []
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

const chartData = computed(() => {
  const days = new Map<string, number>()
  for (let i = 13; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    days.set(d.toISOString().slice(0, 10), 0)
  }
  for (const order of orders.value) {
    if (!order.created_at) continue
    const key = order.created_at.slice(0, 10)
    if (days.has(key)) days.set(key, (days.get(key) || 0) + 1)
  }
  return Array.from(days.entries()).map(([date, count]) => ({
    label: date.slice(8) + '.' + date.slice(5, 7),
    count,
  }))
})

const maxCount = computed(() => Math.max(1, ...chartData.value.map((d) => d.count)))

function chartBarHeight(count: number) {
  return count === 0 ? '6px' : Math.max(10, Math.round((count / maxCount.value) * 150)) + 'px'
}
</script>
