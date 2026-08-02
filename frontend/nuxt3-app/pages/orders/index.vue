<template>
  <DashboardLayout>
    <template #default>
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
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="order in orders" :key="order.id">
                <td class="px-6 py-4">{{ order.id }}</td>
                <td class="px-6 py-4">
                  <span :class="orderStatusClass(order)" class="px-2 py-1 rounded text-sm">{{ order.status }}</span>
                </td>
                <td class="px-6 py-4">{{ order.total_amount }} ₽</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ order.from_address }} → {{ order.to_address }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="orders.length === 0" class="p-8 text-center text-gray-500">Заказов пока нет</div>
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
  total_amount: number
  from_address: string
  to_address: string
}

const orders = ref<Order[]>([])

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
