<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Заказы</h1>
        <p class="text-gray-500 text-sm mt-1">Назначайте курьеров и контролируйте статусы</p>
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
            <tr v-for="order in ordersStore.orders" :key="order.id">
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
      <UiSpinner v-if="ordersStore.isLoading" label="Загрузка…" />
      <div v-else-if="ordersStore.orders.length === 0">
        <UiEmptyState icon="📦" title="Заказов нет" description="По выбранному фильтру ничего не найдено" />
      </div>
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
</script>
