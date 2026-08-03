<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Персонал</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Админы -->
      <div class="bg-white rounded shadow">
        <div class="p-4 border-b bg-red-50">
          <h2 class="text-lg font-semibold text-red-800">Админы</h2>
        </div>
        <div class="p-4">
          <div v-if="admins.length === 0" class="text-center py-8 text-gray-500">
            Нет админов
          </div>
          <table class="min-w-full divide-y divide-gray-200 text-sm">
            <thead>
              <tr>
                <th class="text-left py-2 text-xs font-medium text-gray-500">Имя</th>
                <th class="text-left py-2 text-xs font-medium text-gray-500">Email</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="user in admins" :key="user.id">
                <td class="py-2">{{ user.full_name || '-' }}</td>
                <td class="py-2 text-gray-600">{{ user.email }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Курьеры -->
      <div class="bg-white rounded shadow">
        <div class="p-4 border-b bg-green-50">
          <h2 class="text-lg font-semibold text-green-800">Курьеры</h2>
        </div>
        <div class="p-4">
          <div v-if="couriers.length === 0" class="text-center py-8 text-gray-500">
            Нет курьеров
          </div>
          <table class="min-w-full divide-y divide-gray-200 text-sm">
            <thead>
              <tr>
                <th class="text-left py-2 text-xs font-medium text-gray-500">Имя</th>
                <th class="text-left py-2 text-xs font-medium text-gray-500">Email</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="user in couriers" :key="user.id">
                <td class="py-2">{{ user.full_name || '-' }}</td>
                <td class="py-2 text-gray-600">{{ user.email }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Клиенты с запросами на роль -->
      <div class="bg-white rounded shadow">
        <div class="p-4 border-b bg-yellow-50">
          <h2 class="text-lg font-semibold text-yellow-800">Заявки на роль курьера</h2>
        </div>
        <div class="p-4">
          <div v-if="pendingRequests.length === 0" class="text-center py-8 text-gray-500">
            Нет заявок
          </div>
          <div v-for="req in pendingRequests" :key="req.id" class="mb-4 border rounded p-3">
            <div class="flex justify-between items-start mb-2">
              <div>
                <p class="font-medium text-gray-900">{{ req.user_full_name || 'Без имени' }}</p>
                <p class="text-sm text-gray-600">{{ req.user_email }}</p>
              </div>
              <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">Ожидает</span>
            </div>
            <p v-if="req.reason" class="text-sm text-gray-600 mb-3">{{ req.reason }}</p>
            <div class="flex gap-2">
              <button @click="approveRequest(req)" class="flex-1 px-3 py-1 bg-green-600 text-white rounded text-xs hover:bg-green-700">
                Сделать курьером
              </button>
              <button @click="rejectRequest(req)" class="flex-1 px-3 py-1 bg-gray-600 text-white rounded text-xs hover:bg-gray-700">
                Отклонить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица всех клиентов -->
    <div class="bg-white rounded shadow">
      <div class="p-4 border-b">
        <h2 class="text-lg font-semibold">Все клиенты</h2>
      </div>
      <div class="p-4">
        <table class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Имя</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Телефон</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="user in customers" :key="user.id">
              <td class="px-4 py-3 text-sm">{{ user.full_name || '-' }}</td>
              <td class="px-4 py-3 text-sm text-gray-600">{{ user.email }}</td>
              <td class="px-4 py-3 text-sm text-gray-600">{{ user.phone || '-' }}</td>
              <td class="px-4 py-3 text-sm">
                <select v-model="customerRole[user.id]" class="border rounded px-2 py-1 text-xs mr-2">
                  <option value="CUSTOMER">Клиент</option>
                  <option value="COURIER">Курьер</option>
                </select>
                <button @click="changeUserRole(user.id, customerRole[user.id])" class="px-2 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700">
                  Изменить
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="customers.length === 0" class="text-center py-8 text-gray-500">
          Клиентов пока нет
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface User {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  role: string
  is_active: boolean
}

interface RoleRequest {
  id: number
  user_email: string | null
  user_full_name: string | null
  requested_role: string
  status: string
  reason: string | null
}

const authStore = useAuthStore()
const admins = ref<User[]>([])
const couriers = ref<User[]>([])
const customers = ref<User[]>([])
const pendingRequests = ref<RoleRequest[]>([])
const customerRole = ref<Record<number, string>>({})

const apiBase = useRuntimeConfig().public.apiBase

async function fetchAllData() {
  try {
    const [usersData, requestsData] = await Promise.all([
      $fetch(`${apiBase}/users/?limit=500`, {
        headers: { Authorization: `Bearer ${authStore.token}` },
      }),
      $fetch(`${apiBase}/users/role-requests?status_filter=PENDING`, {
        headers: { Authorization: `Bearer ${authStore.token}` },
      }),
    ])

    const allUsers = usersData as User[]
    admins.value = allUsers.filter(u => u.role === 'ADMIN')
    couriers.value = allUsers.filter(u => u.role === 'COURIER')
    customers.value = allUsers.filter(u => u.role === 'CUSTOMER')
    
    pendingRequests.value = requestsData as RoleRequest[]
  } catch (e) {
    console.error('Error fetching data:', e)
  }
}

async function approveRequest(req: RoleRequest) {
  try {
    await $fetch(`${apiBase}/users/role-requests/${req.id}/approve`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await fetchAllData()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при одобрении')
  }
}

async function rejectRequest(req: RoleRequest) {
  try {
    await $fetch(`${apiBase}/users/role-requests/${req.id}/reject`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await fetchAllData()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при отклонении')
  }
}

async function changeUserRole(userId: number, newRole: string) {
  try {
    await $fetch(`${apiBase}/users/${userId}/role`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: { role: newRole },
    })
    await fetchAllData()
    delete customerRole.value[userId]
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при изменении роли')
  }
}

onMounted(fetchAllData)
</script>
