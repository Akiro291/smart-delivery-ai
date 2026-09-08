<template>
  <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Панель курьера</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">Активных</h3>
          <p class="text-3xl font-bold mt-2 text-blue-600">{{ activeCount }}</p>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">Доставлено</h3>
          <p class="text-3xl font-bold mt-2 text-green-600">{{ completedCount }}</p>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">Назначено</h3>
          <p class="text-3xl font-bold mt-2 text-yellow-600">{{ assignedCount }}</p>
        </div>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-lg font-semibold mb-4">Мои текущие заказы</h3>
        <div v-if="ordersStore.isLoading" class="text-gray-500">Загрузка...</div>
        <div v-else-if="activeOrders.length" class="space-y-3">
          <NuxtLink
            v-for="order in activeOrders"
            :key="order.id"
            to="/courier/orders"
            class="flex items-center justify-between p-4 border rounded hover:bg-gray-50"
          >
            <div>
              <p class="font-medium">Заказ #{{ order.id }}</p>
              <p class="text-sm text-gray-500">{{ order.from_address }} → {{ order.to_address }}</p>
            </div>
            <span class="px-3 py-1 rounded text-xs bg-blue-100 text-blue-800">{{ statusLabel(order.status) }}</span>
          </NuxtLink>
        </div>
        <div v-else class="text-gray-500">Активных заказов нет</div>
      </div>
    </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'courier'], layout: 'courier' })

const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders(0, 100))

const activeOrders = computed(() =>
  ordersStore.orders.filter((o) => !['COMPLETED', 'CANCELLED'].includes(o.status)),
)
const activeCount = computed(() => activeOrders.value.length)
const completedCount = computed(() => ordersStore.orders.filter((o) => o.status === 'COMPLETED').length)
const assignedCount = computed(() => ordersStore.orders.filter((o) => o.status === 'ASSIGNED').length)

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
</script>
