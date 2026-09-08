<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Управление ролями</h1>
      <select v-model="statusFilter" @change="load" class="border rounded px-3 py-2 text-sm">
        <option value="">Все заявки</option>
        <option value="PENDING">Ожидают</option>
        <option value="APPROVED">Одобрены</option>
        <option value="REJECTED">Отклонены</option>
      </select>
    </div>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Пользователь</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Желаемая роль</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Причина</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="req in requests" :key="req.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 text-sm">
              <div>{{ req.user_full_name || 'Без имени' }}</div>
              <div class="text-gray-500">{{ req.user_email }}</div>
            </td>
            <td class="px-6 py-4">
              <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                {{ roleLabel(req.requested_role) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500">{{ req.reason || '—' }}</td>
            <td class="px-6 py-4">
              <span
                :class="{
                  'bg-yellow-100 text-yellow-800': req.status === 'PENDING',
                  'bg-green-100 text-green-800': req.status === 'APPROVED',
                  'bg-red-100 text-red-800': req.status === 'REJECTED',
                }"
                class="px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ statusLabel(req.status) }}
              </span>
            </td>
            <td class="px-6 py-4 text-sm space-x-2">
              <template v-if="req.status === 'PENDING'">
                <button @click="review(req.id, 'approve')" class="px-3 py-1 bg-green-600 text-white rounded text-xs hover:bg-green-700">
                  Одобрить
                </button>
                <button @click="review(req.id, 'reject')" class="px-3 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700">
                  Отклонить
                </button>
              </template>
              <span v-else class="text-gray-400 text-xs">Обработана</span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="requests.length === 0" class="p-8 text-center text-gray-500">Заявок нет</div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface RoleRequest {
  id: number
  user_id: number
  requested_role: string
  status: string
  reason: string | null
  user_email: string | null
  user_full_name: string | null
}

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const requests = ref<RoleRequest[]>([])
const statusFilter = ref('')

onMounted(load)

async function load() {
  try {
    const query = statusFilter.value ? `?status_filter=${statusFilter.value}` : ''
    requests.value = (await $fetch(`${apiBase}/users/role-requests${query}`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as RoleRequest[]
  } catch {
    requests.value = []
  }
}

async function review(requestId: number, action: 'approve' | 'reject') {
  try {
    await $fetch(`${apiBase}/users/role-requests/${requestId}/${action}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await load()
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка обработки заявки')
  }
}

function roleLabel(role: string) {
  const labels: Record<string, string> = {
    COURIER: 'Курьер',
    MANAGER: 'Менеджер',
    ADMIN: 'Админ',
    CUSTOMER: 'Клиент',
  }
  return labels[role] || role
}

function statusLabel(status: string) {
  const labels: Record<string, string> = {
    PENDING: 'Ожидает',
    APPROVED: 'Одобрена',
    REJECTED: 'Отклонена',
  }
  return labels[status] || status
}
</script>
