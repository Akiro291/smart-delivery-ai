<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <h1 class="text-2xl font-bold text-gray-800">Дашборд</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500">Заказов</h3>
            <p class="text-3xl font-bold mt-2">{{ stats.orders }}</p>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500">Доставлено</h3>
            <p class="text-3xl font-bold mt-2 text-green-600">{{ stats.completed }}</p>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500">В пути</h3>
            <p class="text-3xl font-bold mt-2 text-blue-600">{{ stats.inProgress }}</p>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500">Клиентов</h3>
            <p class="text-3xl font-bold mt-2">{{ stats.clients }}</p>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-lg font-semibold mb-4">Последние заказы</h3>
            <div v-if="recentOrders.length === 0" class="text-gray-500">Заказов пока нет</div>
            <div v-else class="space-y-3">
              <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between py-2 border-b">
                <span>Заказ #{{ order.id }}</span>
                <span :class="orderStatusClass(order)" class="px-2 py-1 rounded text-xs">{{ order.status }}</span>
              </div>
            </div>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-lg font-semibold mb-4">Быстрые действия</h3>
            <div class="grid grid-cols-2 gap-4">
              <NuxtLink to="/dashboard/orders" class="p-4 bg-blue-50 rounded hover:bg-blue-100 text-center">
                <div class="text-2xl mb-1">📋</div>
                <div class="text-sm font-medium">Заказы</div>
              </NuxtLink>
              <NuxtLink to="/dashboard/products" class="p-4 bg-green-50 rounded hover:bg-green-100 text-center">
                <div class="text-2xl mb-1">🛒</div>
                <div class="text-sm font-medium">Товары</div>
              </NuxtLink>
              <NuxtLink to="/dashboard/clients" class="p-4 bg-purple-50 rounded hover:bg-purple-100 text-center">
                <div class="text-2xl mb-1">👥</div>
                <div class="text-sm font-medium">Клиенты</div>
              </NuxtLink>
              <NuxtLink to="/dashboard/ai" class="p-4 bg-yellow-50 rounded hover:bg-yellow-100 text-center">
                <div class="text-2xl mb-1">🤖</div>
                <div class="text-sm font-medium">AI</div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface Order {
  id: number
  status: string
}

const stats = ref({ orders: 12, completed: 8, inProgress: 3, clients: 24 })
const recentOrders = ref<Order[]>([
  { id: 1001, status: 'PENDING' },
  { id: 1002, status: 'IN_PROGRESS' },
  { id: 1003, status: 'COMPLETED' },
])

function orderStatusClass(order: Order) {
  const map: Record<string, string> = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    IN_PROGRESS: 'bg-blue-100 text-blue-800',
    COMPLETED: 'bg-green-100 text-green-800',
    CANCELLED: 'bg-red-100 text-red-800',
  }
  return map[order.status] || 'bg-gray-100 text-gray-800'
}
</script>
