<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Аналитика</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500 mb-2">Выручка (доставленные)</h3>
        <p class="text-3xl font-bold text-green-600">{{ formatMoney(stats?.completed_revenue) }} ₽</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500 mb-2">Всего заказов</h3>
        <p class="text-3xl font-bold">{{ stats?.total || 0 }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500 mb-2">Активных заказов</h3>
        <p class="text-3xl font-bold text-blue-600">{{ stats?.active || 0 }}</p>
      </div>
    </div>

    <div class="bg-white p-6 rounded shadow">
      <h3 class="text-lg font-semibold mb-4">Заказы по статусам</h3>
      <div class="space-y-3">
        <div v-for="item in statusRows" :key="item.status" class="flex items-center gap-4">
          <span class="w-32 text-sm text-gray-600">{{ item.label }}</span>
          <div class="flex-1 bg-gray-100 rounded-full h-4 overflow-hidden">
            <div class="h-4 bg-blue-500 rounded-full" :style="{ width: item.percent + '%' }" />
          </div>
          <span class="w-10 text-right text-sm font-medium">{{ item.count }}</span>
        </div>
      </div>
    </div>

    <div class="bg-white p-6 rounded shadow">
      <h3 class="text-lg font-semibold mb-4">Заказы по дням (последние 14)</h3>
      <div class="flex items-end gap-2 h-48">
        <div v-for="(day, i) in chartData" :key="i" class="flex-1 flex flex-col items-center gap-1">
          <div
            :style="{ height: chartBarHeight(day.count) }"
            class="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
            :title="`${day.count} заказов`"
          />
          <span class="text-xs text-gray-500">{{ day.label }}</span>
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

const STATUS_LABELS: Record<string, string> = {
  PENDING: 'Ожидает',
  CONFIRMED: 'Подтверждён',
  ASSIGNED: 'Назначен',
  IN_PROGRESS: 'В пути',
  COMPLETED: 'Доставлен',
  CANCELLED: 'Отменён',
}

const ordersStore = useOrdersStore()
const stats = ref<{ total: number; by_status: Record<string, number>; completed_revenue: number; active: number } | null>(null)
const orders = ref<Order[]>([])

onMounted(async () => {
  const [statsData, ordersData] = await Promise.all([
    ordersStore.fetchStats(),
    ordersStore.fetchOrders(0, 200),
  ])
  stats.value = statsData
  orders.value = (ordersData as unknown as Order[]) || []
})

const statusRows = computed(() => {
  const byStatus = stats.value?.by_status || {}
  const total = Object.values(byStatus).reduce((a, b) => a + b, 0) || 1
  return Object.keys(STATUS_LABELS).map((status) => ({
    status,
    label: STATUS_LABELS[status],
    count: byStatus[status] || 0,
    percent: Math.round(((byStatus[status] || 0) / total) * 100),
  }))
})

const chartData = computed(() => {
  const days = new Map<string, number>()
  for (let i = 13; i >= 0; i--) {
    const d = new Date()
    d.setDate(d.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    days.set(key, 0)
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
  return count === 0 ? '4px' : Math.max(8, Math.round((count / maxCount.value) * 160)) + 'px'
}

function formatMoney(value: number | undefined) {
  return Number(value || 0).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
