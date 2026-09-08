<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Профиль</h1>
    <div class="bg-white p-8 rounded shadow max-w-md">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-500">Email</label>
          <p class="mt-1 text-lg">{{ user.email || 'не указан' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-500">Имя</label>
          <p class="mt-1 text-lg">{{ user.full_name || 'не указано' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-500">Телефон</label>
          <p class="mt-1 text-lg">{{ user.phone || 'не указан' }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-500">Роль</label>
          <p class="mt-1 text-lg">{{ user.role || '-' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const user = ref({ email: '', full_name: null as string | null, phone: null as string | null, role: '' })

onMounted(async () => {
  try {
    const data = await useApi().get('/auth/me')
    user.value = data as typeof user.value
  } catch {
    navigateTo('/auth/login')
  }
})
</script>
