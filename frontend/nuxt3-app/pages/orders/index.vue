<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Заказы</h1>
        <p class="text-gray-500 text-sm mt-1">Все заказы, доступные вашей роли</p>
      </div>
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
        <div class="flex items-center justify-between mt-5 pt-4 border-t border-gray-50">
          <span class="text-xs text-gray-400">{{ formatDate(order.created_at) }}</span>
          <span class="font-bold">{{ formatMoney(order.total_amount) }} ₽</span>
        </div>
      </div>
    </div>

    <UiSpinner v-else-if="ordersStore.isLoading" label="Загрузка…" />
    <div v-else class="card">
      <UiEmptyState icon="📦" title="Заказов пока нет" description="Здесь появятся заказы, доступные вашей роли" />
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders())
</script>
