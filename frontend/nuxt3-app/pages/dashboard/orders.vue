<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Заказы</h1>
      <select v-model="statusFilter" @change="load" class="border rounded px-3 py-2 text-sm">
        <option value="">Все статусы</option>
        <option value="PENDING">Ожидает</option>
        <option value="CONFIRMED">Подтверждён</option>
        <option value="ASSIGNED">Назначен</option>
        <option value="IN_PROGRESS">В пути</option>
        <option value="COMPLETED">Доставлен</option>
        <option value="CANCELLED">Отменён</option>
      </select>
    </div>
    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Клиент</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Сумма</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Курьер</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Назначить</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="order in ordersStore.orders" :key="order.id">
            <td class="px-6 py-4">#{{ order.id }}</td>
            <td class="px-6 py-4">{{ order.customer_name || `#${order.customer_id}` }}</td>
            <td class="px-6 py-4">
              <span :class="orderStatusClass(order.status)" class="px-2 py-1 rounded text-sm">
                {{ statusLabel(order.status) }}
              </span>
            </td>
            <td class="px-6 py-4">{{ formatMoney(order.total_amount) }} ₽</td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ order.courier_name || '—' }}</td>
            <td class="px-6 py-4">
              <select
                :value="order.courier_id || ''"
                :disabled="['COMPLETED', 'CANCELLED'].includes(order.status)"
                @change="onAssign(order.id, $event)"
                class="border rounded px-2 py-1 text-xs"
              >
                <option value="">— не назначен —</option>
                <option v-for="courier in couriers" :key="courier.id" :value="courier.id">
                  {{ courier.full_name || courier.email }}
                </option>
              </select>
            </td>
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
definePageMeta({ middleware: 'manager', layout: 'manager' })

interface UserRow {
  id: number
  email: string
  full_name: string | null
}

const ordersStore = useOrdersStore()
const authStore = useAuthStore()
const statusFilter = ref('')
const couriers = ref<UserRow[]>([])
const apiBase = useRuntimeConfig().public.apiBase

const STATUS_TRANSITIONS: Record<string, string[]> = {
  PENDING: ['CONFIRMED', 'CANCELLED'],
  CONFIRMED: ['ASSIGNED', 'CANCELLED'],
  ASSIGNED: ['IN_PROGRESS', 'CANCELLED'],
  IN_PROGRESS: ['COMPLETED', 'CANCELLED'],
  COMPLETED: [],
  CANCELLED: [],
}

onMounted(load)

async function load() {
  await ordersStore.fetchOrders(0, 100, statusFilter.value || undefined)
  if (couriers.value.length === 0) {
    try {
      couriers.value = (await $fetch(`${apiBase}/users/?role=COURIER&limit=100`, {
        headers: { Authorization: `Bearer ${authStore.token}` },
      })) as UserRow[]
    } catch {
      couriers.value = []
    }
  }
}

async function onAssign(orderId: number, event: Event) {
  const courierId = Number((event.target as HTMLSelectElement).value)
  if (!courierId) return
  try {
    await ordersStore.assignCourier(orderId, courierId)
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка назначения курьера')
    await load()
  }
}

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
</script>
