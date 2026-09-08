<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Управление заказами</h1>
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
          <tr v-for="order in orders" :key="order.id">
            <td class="px-6 py-4">#{{ order.id }}</td>
            <td class="px-6 py-4">{{ order.customer_name || `#${order.customer_id}` }}</td>
            <td class="px-6 py-4">
              <span :class="statusClass(order.status)" class="px-2 py-1 rounded text-sm">{{ statusLabel(order.status) }}</span>
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
      <div v-if="!isLoading && orders.length === 0" class="p-8 text-center text-gray-500">Заказов пока нет</div>
      <div v-if="isLoading" class="p-8 text-center text-gray-500">Загрузка...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface Order {
  id: number
  customer_id: number
  customer_name: string | null
  courier_id: number | null
  courier_name: string | null
  status: string
  total_amount: number
}

interface UserRow {
  id: number
  email: string
  full_name: string | null
}

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const orders = ref<Order[]>([])
const couriers = ref<UserRow[]>([])
const isLoading = ref(true)

onMounted(load)

async function load() {
  isLoading.value = true
  try {
    orders.value = (await $fetch(`${apiBase}/orders/?limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as Order[]
    couriers.value = (await $fetch(`${apiBase}/users/?role=COURIER&limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as UserRow[]
  } catch {
    orders.value = []
  } finally {
    isLoading.value = false
  }
}

async function onAssign(orderId: number, event: Event) {
  const courierId = Number((event.target as HTMLSelectElement).value)
  if (!courierId) return
  try {
    await $fetch(`${apiBase}/orders/${orderId}/assign`, {
      method: 'POST',
      body: { courier_id: courierId },
      headers: { Authorization: `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
    })
    await load()
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка назначения курьера')
    await load()
  }
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
