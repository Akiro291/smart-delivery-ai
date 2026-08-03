<template>
  <AdminLayout>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Курьеры</h1>
      <div class="bg-white p-6 rounded shadow overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Имя</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Телефон</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in couriers" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.full_name || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.phone || '-' }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="user.is_active ? 'text-green-600' : 'text-red-600'">
                  {{ user.is_active ? 'Активен' : 'Неактивен' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="couriers.length === 0" class="p-6 text-center text-gray-500">
          Курьеров пока нет
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface User {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  is_active: boolean
}

const authStore = useAuthStore()
const couriers = ref<User[]>([])

async function fetchCouriers() {
  try {
    couriers.value = await $fetch('/api/v1/users/?role=COURIER&limit=100', {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
  } catch (e) {
    console.error('Error fetching couriers:', e)
  }
}

onMounted(fetchCouriers)
</script>
