<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Панель администратора</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Пользователей</h3>
        <p class="text-3xl font-bold mt-2">{{ counts.total || 0 }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Клиентов</h3>
        <p class="text-3xl font-bold mt-2 text-blue-600">{{ counts.customers || 0 }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Курьеров</h3>
        <p class="text-3xl font-bold mt-2 text-green-600">{{ counts.couriers || 0 }}</p>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-sm text-gray-500">Админов</h3>
        <p class="text-3xl font-bold mt-2 text-red-600">{{ counts.admins || 0 }}</p>
      </div>
    </div>
    <div class="bg-white p-6 rounded shadow">
      <h3 class="text-lg font-semibold mb-4">Быстрые действия</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <NuxtLink to="/admin/users" class="p-4 bg-purple-50 rounded hover:bg-purple-100 text-center">
          <div class="text-2xl mb-1">&#x1F465;</div>
          <div class="text-sm font-medium">Пользователи</div>
        </NuxtLink>
        <NuxtLink to="/admin/roles" class="p-4 bg-yellow-50 rounded hover:bg-yellow-100 text-center">
          <div class="text-2xl mb-1">&#x1F512;</div>
          <div class="text-sm font-medium">Управление ролями</div>
        </NuxtLink>
        <NuxtLink to="/admin/orders" class="p-4 bg-blue-50 rounded hover:bg-blue-100 text-center">
          <div class="text-2xl mb-1">&#x1F4CB;</div>
          <div class="text-sm font-medium">Заказы</div>
        </NuxtLink>
        <NuxtLink to="/admin/products" class="p-4 bg-green-50 rounded hover:bg-green-100 text-center">
          <div class="text-2xl mb-1">&#x1F6D2;</div>
          <div class="text-sm font-medium">Товары</div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const counts = ref({ total: 0, customers: 0, couriers: 0, admins: 0 })

async function fetchCounts() {
  const token = authStore.token || localStorage.getItem('token')
  if (!token) {
    return navigateTo('/auth/login')
  }
  
  try {
    const data = await $fetch(`${apiBase}/users/count`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    counts.value = data
  } catch (e) {
    console.error('Error fetching counts:', e)
    if (e.statusCode === 401) {
      await authStore.logout()
      navigateTo('/auth/login')
    }
  }
}

onMounted(fetchCounts)
</script>
