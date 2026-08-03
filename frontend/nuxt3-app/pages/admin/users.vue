<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Пользователи</h1>
      <div class="flex gap-2">
        <button @click="fetchUsers" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Обновить</button>
      </div>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Всего</p>
        <p class="text-2xl font-bold">{{ counts.total }}</p>
      </div>
      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Клиенты</p>
        <p class="text-2xl font-bold text-blue-600">{{ counts.customers }}</p>
      </div>
      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Курьеры</p>
        <p class="text-2xl font-bold text-green-600">{{ counts.couriers }}</p>
      </div>
      <div class="bg-white p-4 rounded shadow">
        <p class="text-sm text-gray-500">Админы</p>
        <p class="text-2xl font-bold text-red-600">{{ counts.admins }}</p>
      </div>
    </div>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Имя</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Телефон</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Роль</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.full_name || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.email }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.phone || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="roleBadgeClass(user.role)">{{ roleLabel(user.role) }}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'">
                {{ user.is_active ? 'Активен' : 'Неактивен' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm space-x-2">
              <select v-model="tempRole[user.id]" class="border rounded px-2 py-1 text-xs">
                <option value="CUSTOMER">Клиент</option>
                <option value="COURIER">Курьер</option>
                <option value="ADMIN">Админ</option>
              </select>
              <button @click="changeRole(user.id)" class="px-2 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700">
                Изменить
              </button>
              <button @click="toggleUserStatus(user)" :class="user.is_active ? 'text-red-600' : 'text-green-600'">
                {{ user.is_active ? 'Деактивировать' : 'Активировать' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="users.length === 0" class="p-6 text-center text-gray-500">
        Пользователей пока нет
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
  is_superuser: boolean
}

const authStore = useAuthStore()

const users = ref<User[]>([])
const counts = ref({ total: 0, customers: 0, couriers: 0, admins: 0 })
const tempRole = ref<Record<number, string>>({})

function roleBadgeClass(role: string) {
  const classes = {
    ADMIN: 'px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium',
    COURIER: 'px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium',
    CUSTOMER: 'px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium',
  }
  return classes[role] || 'px-2 py-1 bg-gray-100 text-gray-800 rounded-full text-xs'
}

function roleLabel(role: string) {
  const labels = {
    ADMIN: 'Админ',
    COURIER: 'Курьер',
    CUSTOMER: 'Клиент',
  }
  return labels[role] || role
}

const apiBase = useRuntimeConfig().public.apiBase

async function fetchUsers() {
  console.log('Auth token:', authStore.token?.substring(0, 20) + '...')
  try {
    const [usersData, countsData] = await Promise.all([
      $fetch(`${apiBase}/users/?limit=100`, {
        headers: { Authorization: `Bearer ${authStore.token}` },
      }),
      $fetch(`${apiBase}/users/count`, {
        headers: { Authorization: `Bearer ${authStore.token}` },
      }),
    ])
    console.log('Users data:', usersData)
    console.log('Counts data:', countsData)
    
    // Ensure phone field exists
    users.value = (usersData as User[]).map(u => ({
      ...u,
      phone: u.phone || null,
    }))
    counts.value = countsData as typeof counts.value
  } catch (e: any) {
    console.error('Error fetching users:', e)
    console.error('Error response:', e.response)
    console.error('Error status:', e.statusCode)
    if (e.response) {
      e.response.text().then(text => {
        console.error('Response text:', text)
      })
    }
  }
}

async function changeRole(userId: number) {
  const newRole = tempRole.value[userId]
  if (!newRole) return

  try {
    await $fetch(`${apiBase}/users/${userId}/role`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: { role: newRole },
    })
    await fetchUsers()
    delete tempRole.value[userId]
    await authStore.fetchUser()
    navigateTo('/admin')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при изменении роли')
  }
}

async function toggleUserStatus(user: User) {
  try {
    await $fetch(`${apiBase}/users/${user.id}/status`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: { is_active: !user.is_active },
    })
    await fetchUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при изменении статуса')
  }
}

onMounted(fetchUsers)
</script>
