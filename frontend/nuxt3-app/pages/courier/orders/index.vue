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
          <p class="text-sm text-gray-500">{{ order.from_address }} → {{ order.to_address }}</p>
          <p v-if="order.description" class="text-sm text-gray-500 mt-1">{{ order.description }}</p>
          <div class="flex items-center justify-between mt-4">
            <p class="font-bold">{{ formatMoney(order.total_amount) }} ₽</p>
            <div class="flex gap-2" v-if="canChangeStatus(order)">
              <button
                v-for="next in nextStatuses(order.status)"
                :key="next"
                @click="changeStatus(order, next)"
                :class="next === 'CANCELLED' ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'"
                class="px-4 py-2 text-white rounded text-sm"
              >
                {{ actionLabel(next) }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="bg-white p-12 rounded shadow text-center text-gray-500">Заказов пока нет</div>
    </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'courier'], layout: 'courier' })

const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders())

const NEXT: Record<string, string[]> = {
  ASSIGNED: ['IN_PROGRESS', 'CANCELLED'],
  IN_PROGRESS: ['COMPLETED'],
}

function canChangeStatus(order: { status: string }) {
  return Boolean(NEXT[order.status]?.length)
}

function nextStatuses(status: string) {
  return NEXT[status] || []
}

async function changeStatus(order: { id: number; status: string }, next: string) {
  try {
    await ordersStore.updateOrder(order.id, { status: next })
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка смены статуса')
  }
}

function actionLabel(status: string) {
  const labels: Record<string, string> = {
    IN_PROGRESS: 'Начать доставку',
    COMPLETED: 'Завершить',
    CANCELLED: 'Отменить',
  }
  return labels[status] || status
}

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

function formatMoney(value: number | string) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
