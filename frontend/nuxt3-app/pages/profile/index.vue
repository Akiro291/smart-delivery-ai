<template>
  <DashboardLayout>
    <template #default>
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
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const user = ref({ email: '', full_name: null as string | null })

onMounted(async () => {
  try {
    const data = await useApi().get('/auth/me')
    user.value = data
  } catch {
    navigateTo('/auth/login')
  }
})
</script>
