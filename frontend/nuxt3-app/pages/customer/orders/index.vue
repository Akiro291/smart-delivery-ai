<template>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Мои заказы</h1>
      <div v-if="ordersStore.isLoading" class="text-gray-500">Загрузка...</div>
      <div v-else-if="ordersStore.orders.length" class="space-y-4">
        <div v-for="order in ordersStore.orders" :key="order.id" class="bg-white p-6 rounded shadow">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold">Заказ #{{ order.id }}</h3>
            <span :class="statusClass(order.status)" class="px-3 py-1 rounded text-xs">{{ statusLabel(order.status) }}</span>
          </div>
          <p class="text-sm text-gray-500">
            {{ order.from_address }} → {{ order.to_address }}
          </p>
          <div class="flex justify-between items-center mt-3">
            <p class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</p>
            <p class="font-bold">{{ formatMoney(order.total_amount) }} ₽</p>
          </div>
        </div>
      </div>
      <div v-else class="bg-white p-12 rounded shadow text-center text-gray-500">
        Заказов пока нет.
        <NuxtLink to="/customer" class="text-purple-600 hover:underline">Создать первый заказ</NuxtLink>
      </div>
    </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders())

function statusClass(status: string) {
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

function formatDate(value: string | null) {
  if (!value) return ''
  return new Date(value).toLocaleString('ru-RU', { dateStyle: 'short', timeStyle: 'short' })
}

function formatMoney(value: number | string) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
