<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Управление ролями</h1>
        <p class="text-gray-500 text-sm mt-1">Заявки пользователей на смену роли</p>
      </div>
      <select v-model="statusFilter" @change="load" class="input !w-auto">
        <option value="">Все заявки</option>
        <option value="PENDING">Ожидают</option>
        <option value="APPROVED">Одобрены</option>
        <option value="REJECTED">Отклонены</option>
      </select>
    </div>

    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table-base">
          <thead>
            <tr>
              <th>Пользователь</th>
              <th>Желаемая роль</th>
              <th>Причина</th>
              <th>Статус</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="req in requests" :key="req.id">
              <td>
                <div class="font-medium text-gray-800">{{ req.user_full_name || 'Без имени' }}</div>
                <div class="text-xs text-gray-400">{{ req.user_email }}</div>
              </td>
              <td>
                <span class="badge bg-brand-50 text-brand-700 border border-brand-100">{{ roleLabel(req.requested_role) }}</span>
              </td>
              <td class="text-gray-500 max-w-56"><span class="line-clamp-2">{{ req.reason || '—' }}</span></td>
              <td>
                <span :class="requestBadgeClass(req.status)" class="badge">{{ requestLabel(req.status) }}</span>
              </td>
              <td>
                <div v-if="req.status === 'PENDING'" class="flex gap-2">
                  <button @click="review(req.id, 'approve')" class="btn-primary !px-3 !py-1.5 !text-xs">Одобрить</button>
                  <button @click="review(req.id, 'reject')" class="btn-secondary !px-3 !py-1.5 !text-xs !text-red-600 hover:!bg-red-50">Отклонить</button>
                </div>
                <span v-else class="text-xs text-gray-300">Обработана</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <UiSpinner v-if="isLoading" label="Загрузка…" />
      <div v-else-if="requests.length === 0">
        <UiEmptyState icon="🔑" title="Заявок нет" description="Новые заявки на смену роли появятся здесь" />
      </div>
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
const isLoading = ref(true)

onMounted(load)

async function load() {
  isLoading.value = true
  try {
    const query = statusFilter.value ? `?status_filter=${statusFilter.value}` : ''
    requests.value = (await $fetch(`${apiBase}/users/role-requests${query}`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as RoleRequest[]
  } catch {
    requests.value = []
  } finally {
    isLoading.value = false
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

function requestLabel(status: string) {
  const labels: Record<string, string> = { PENDING: 'Ожидает', APPROVED: 'Одобрена', REJECTED: 'Отклонена' }
  return labels[status] || status
}

function requestBadgeClass(status: string) {
  const classes: Record<string, string> = {
    PENDING: 'bg-amber-100 text-amber-800',
    APPROVED: 'bg-emerald-100 text-emerald-800',
    REJECTED: 'bg-red-100 text-red-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-700'
}
</script>
