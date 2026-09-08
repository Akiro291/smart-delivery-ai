<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Заказы</h1>
    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Сумма</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Адрес</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Создан</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="order in ordersStore.orders" :key="order.id">
            <td class="px-6 py-4">#{{ order.id }}</td>
            <td class="px-6 py-4">
              <span :class="orderStatusClass(order.status)" class="px-2 py-1 rounded text-sm">
                {{ statusLabel(order.status) }}
              </span>
            </td>
            <td class="px-6 py-4">{{ formatMoney(order.total_amount) }} ₽</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ order.from_address }} → {{ order.to_address }}</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ formatDate(order.created_at) }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="!ordersStore.isLoading && ordersStore.orders.length === 0" class="p-8 text-center text-gray-500">
        Заказов пока нет
      </div>
      <div v-if="ordersStore.isLoading" class="p-8 text-center text-gray-500">Загрузка...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const ordersStore = useOrdersStore()

onMounted(() => {
  ordersStore.fetchOrders()
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

function formatMoney(value: number | string) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}

function formatDate(value: string | null) {
  if (!value) return '-'
  return new Date(value).toLocaleString('ru-RU', { dateStyle: 'short', timeStyle: 'short' })
}
</script>
