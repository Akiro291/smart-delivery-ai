<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Дашборд</h1>
    <div v-if="stats" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Всего заказов</h3>
        <p class="text-3xl font-bold mt-2">{{ stats.total }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Доставлено</h3>
        <p class="text-3xl font-bold mt-2 text-green-600">{{ stats.by_status.COMPLETED || 0 }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Активных</h3>
        <p class="text-3xl font-bold mt-2 text-blue-600">{{ stats.active }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Выручка</h3>
        <p class="text-3xl font-bold mt-2">{{ formatMoney(stats.completed_revenue) }} ₽</p>
      </div>
    </div>
    <div v-else class="text-gray-500">Загрузка статистики...</div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-lg font-semibold mb-4">Последние заказы</h3>
        <div v-if="recentOrders.length === 0" class="text-gray-500">Заказов пока нет</div>
        <div v-else class="space-y-3">
          <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between py-2 border-b">
            <NuxtLink :to="`/orders`" class="hover:underline">Заказ #{{ order.id }}</NuxtLink>
            <span :class="orderStatusClass(order.status)" class="px-2 py-1 rounded text-xs">
              {{ statusLabel(order.status) }}
            </span>
          </div>
        </div>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-lg font-semibold mb-4">Быстрые действия</h3>
        <div class="grid grid-cols-2 gap-4">
          <NuxtLink to="/dashboard/orders" class="p-4 bg-blue-50 rounded hover:bg-blue-100 text-center">
            <div class="text-2xl mb-1">&#x1F4CB;</div>
            <div class="text-sm font-medium">Заказы</div>
          </NuxtLink>
          <NuxtLink to="/dashboard/products" class="p-4 bg-green-50 rounded hover:bg-green-100 text-center">
            <div class="text-2xl mb-1">&#x1F6D2;</div>
            <div class="text-sm font-medium">Товары</div>
          </NuxtLink>
          <NuxtLink to="/dashboard/clients" class="p-4 bg-purple-50 rounded hover:bg-purple-100 text-center">
            <div class="text-2xl mb-1">&#x1F465;</div>
            <div class="text-sm font-medium">Клиенты</div>
          </NuxtLink>
          <NuxtLink to="/dashboard/ai" class="p-4 bg-yellow-50 rounded hover:bg-yellow-100 text-center">
            <div class="text-2xl mb-1">&#x1F916;</div>
            <div class="text-sm font-medium">AI</div>
          </NuxtLink>
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
}

const ordersStore = useOrdersStore()
const stats = ref<{ total: number; by_status: Record<string, number>; completed_revenue: number; active: number } | null>(null)
const recentOrders = ref<Order[]>([])

onMounted(async () => {
  const [statsData, ordersData] = await Promise.all([
    ordersStore.fetchStats(),
    ordersStore.fetchOrders(0, 5),
  ])
  stats.value = statsData
  recentOrders.value = ordersData as unknown as Order[]
})

function orderStatusClass(status: string) {
  const map: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    CONFIRMED: 'bg-blue-100 text-blue-800',
    ASSIGNED: 'bg-indigo-100 text-indigo-800',
    IN_PROGRESS: 'bg-cyan-100 text-cyan-800',
    COMPLETED: 'bg-green-100 text-green-800',
    CANCELLED: 'bg-red-100 text-red-800',
  }
  return map[status] || 'bg-gray-100 text-gray-800'
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    PENDING: 'Ожидает',
    CONFIRMED: 'Подтверждён',
    ASSIGNED: 'Назначен',
    IN_PROGRESS: 'В пути',
    COMPLETED: 'Доставлен',
    CANCELLED: 'Отменён',
  }
  return labels[status] || status
}

function formatMoney(value: number) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
