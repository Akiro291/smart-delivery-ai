<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Мои заказы</h1>
      <p class="text-gray-500 text-sm mt-1">Меняйте статусы по мере выполнения</p>
    </div>

    <div v-if="ordersStore.orders.length" class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <div v-for="order in ordersStore.orders" :key="order.id" class="card card-hover p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-bold text-gray-800">Заказ #{{ order.id }}</h3>
          <UiStatusBadge :status="order.status" />
        </div>
        <div class="space-y-2.5 text-sm">
          <div class="flex items-center gap-2.5 text-gray-600">
            <span class="h-2 w-2 rounded-full bg-brand-500 flex-shrink-0" />
            <span class="truncate">{{ order.from_address }}</span>
          </div>
          <div class="flex items-center gap-2.5 text-gray-600">
            <span class="h-2 w-2 rounded-full bg-emerald-500 flex-shrink-0" />
            <span class="truncate">{{ order.to_address }}</span>
          </div>
        </div>
        <p v-if="order.description" class="text-xs text-gray-400 mt-3 line-clamp-2">{{ order.description }}</p>

        <div v-if="canChangeStatus(order)" class="flex gap-2 mt-5 pt-4 border-t border-gray-50">
          <button
            v-for="next in nextStatuses(order.status)"
            :key="next"
            @click="changeStatus(order, next)"
            :class="next === 'CANCELLED' ? 'btn-secondary !text-red-600 hover:!bg-red-50' : 'btn-primary flex-1'"
          >
            {{ actionLabel(next) }}
          </button>
        </div>
        <div v-else class="mt-5 pt-4 border-t border-gray-50 flex justify-between items-center">
          <span class="text-xs text-gray-400">{{ formatDate(order.created_at) }}</span>
          <span class="font-bold">{{ formatMoney(order.total_amount) }} ₽</span>
        </div>
      </div>
    </div>

    <UiSpinner v-else-if="ordersStore.isLoading" label="Загрузка…" />
    <div v-else class="card">
      <UiEmptyState icon="📦" title="Заказов пока нет" description="Назначенные вам заказы появятся здесь" />
    </div>
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
</script>
