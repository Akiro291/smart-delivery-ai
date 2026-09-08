<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Здравствуйте, {{ authStore.userName }}! 🚚</h1>
      <p class="text-gray-500 text-sm mt-1">Ваш рабочий день на одном экране</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
      <UiStat label="Активных заказов" :value="activeCount" icon="🚚" tone="cyan" hint="нужно доставить" />
      <UiStat label="Доставлено" :value="completedCount" icon="✅" tone="emerald" hint="закрытых заказов" />
      <UiStat label="Назначено" :value="assignedCount" icon="📥" tone="amber" hint="ждут начала работы" />
    </div>

    <div class="card">
      <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
        <h3 class="font-semibold text-gray-800">Текущие заказы</h3>
        <NuxtLink to="/courier/orders" class="text-sm font-medium text-brand-600 hover:text-brand-700">Все заказы →</NuxtLink>
      </div>
      <div v-if="activeOrders.length" class="divide-y divide-gray-50">
        <NuxtLink
          v-for="order in activeOrders"
          :key="order.id"
          to="/courier/orders"
          class="flex items-center justify-between px-6 py-4 hover:bg-gray-50/70 transition-colors"
        >
          <div class="min-w-0">
            <p class="font-medium text-gray-800 text-sm">Заказ #{{ order.id }}</p>
            <p class="text-xs text-gray-500 truncate mt-0.5">{{ order.from_address }} → {{ order.to_address }}</p>
          </div>
          <UiStatusBadge :status="order.status" />
        </NuxtLink>
      </div>
      <UiSpinner v-else-if="ordersStore.isLoading" label="Загрузка…" />
      <UiEmptyState v-else icon="🎉" title="Активных заказов нет" description="Как только менеджер назначит заказ, он появится здесь" />
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'courier'], layout: 'courier' })

const authStore = useAuthStore()
const ordersStore = useOrdersStore()

onMounted(() => ordersStore.fetchOrders(0, 100))

const activeOrders = computed(() => ordersStore.orders.filter((o) => !['COMPLETED', 'CANCELLED'].includes(o.status)))
const activeCount = computed(() => activeOrders.value.length)
const completedCount = computed(() => ordersStore.orders.filter((o) => o.status === 'COMPLETED').length)
const assignedCount = computed(() => ordersStore.orders.filter((o) => o.status === 'ASSIGNED').length)
</script>
