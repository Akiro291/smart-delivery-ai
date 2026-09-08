<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Управление заказами</h1>
        <p class="text-gray-500 text-sm mt-1">Все заказы платформы</p>
      </div>
      <select v-model="statusFilter" @change="load" class="input !w-auto">
        <option value="">Все статусы</option>
        <option v-for="(meta, status) in ORDER_STATUS_META" :key="status" :value="status">{{ meta.label }}</option>
      </select>
    </div>

    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table-base">
          <thead>
            <tr>
              <th>ID</th>
              <th>Клиент</th>
              <th>Статус</th>
              <th>Сумма</th>
              <th>Курьер</th>
              <th>Назначить</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id">
              <td class="font-semibold text-gray-800">#{{ order.id }}</td>
              <td class="text-gray-600">{{ order.customer_name || `#${order.customer_id}` }}</td>
              <td><UiStatusBadge :status="order.status" /></td>
              <td class="font-medium">{{ formatMoney(order.total_amount) }} ₽</td>
              <td class="text-gray-500">{{ order.courier_name || '—' }}</td>
              <td>
                <select
                  :value="order.courier_id || ''"
                  :disabled="['COMPLETED', 'CANCELLED'].includes(order.status)"
                  @change="onAssign(order.id, $event)"
                  class="input !w-44 !py-1.5 !text-xs"
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
      </div>
      <UiSpinner v-if="isLoading" label="Загрузка…" />
      <div v-else-if="orders.length === 0">
        <UiEmptyState icon="📦" title="Заказов нет" description="По выбранному фильтру ничего не найдено" />
      </div>
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
const statusFilter = ref('')
const isLoading = ref(true)

onMounted(load)

async function load() {
  isLoading.value = true
  try {
    const q = statusFilter.value ? `&status_filter=${statusFilter.value}` : ''
    orders.value = (await $fetch(`${apiBase}/orders/?limit=100${q}`, {
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
</script>
