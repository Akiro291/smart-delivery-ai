<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Мои заказы</h1>
      <p class="text-gray-500 text-sm mt-1">История и текущие доставки</p>
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
        <div class="flex items-center justify-between mt-5 pt-4 border-t border-gray-50">
          <span class="text-xs text-gray-400">{{ formatDate(order.created_at) }}</span>
          <span class="font-bold text-gray-900">{{ formatMoney(order.total_amount) }} ₽</span>
        </div>
      </div>
    </div>

    <UiSpinner v-else-if="ordersStore.isLoading" label="Загрузка заказов…" />
    <div v-else class="card">
      <UiEmptyState icon="📦" title="Заказов пока нет" description="Оформите первый заказ через каталог">
        <NuxtLink to="/customer" class="btn-primary">Перейти в каталог</NuxtLink>
      </UiEmptyState>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders())
</script>
