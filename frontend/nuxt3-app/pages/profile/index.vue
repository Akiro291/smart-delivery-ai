<template>
  <div class="space-y-6 max-w-lg">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Профиль</h1>
      <p class="text-gray-500 text-sm mt-1">Ваши данные в системе</p>
    </div>

    <div class="card overflow-hidden">
      <div class="bg-gradient-to-r from-brand-600 to-brand-800 px-6 py-8 text-white flex items-center gap-4">
        <div class="h-16 w-16 rounded-2xl bg-white/15 backdrop-blur flex items-center justify-center text-2xl font-bold border border-white/20">
          {{ initial }}
        </div>
        <div>
          <p class="font-bold text-lg">{{ user.full_name || 'Без имени' }}</p>
          <p class="text-white/60 text-sm">{{ user.email }}</p>
        </div>
      </div>
      <div class="p-6 space-y-4">
        <div class="flex items-center justify-between py-2 border-b border-gray-50">
          <span class="text-sm text-gray-500">Email</span>
          <span class="text-sm font-medium">{{ user.email || '—' }}</span>
        </div>
        <div class="flex items-center justify-between py-2 border-b border-gray-50">
          <span class="text-sm text-gray-500">Телефон</span>
          <span class="text-sm font-medium">{{ user.phone || '—' }}</span>
        </div>
        <div class="flex items-center justify-between py-2">
          <span class="text-sm text-gray-500">Роль</span>
          <span class="badge bg-brand-50 text-brand-700">{{ roleLabel(user.role) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const user = ref({ email: '', full_name: null as string | null, phone: null as string | null, role: '' })
const isLoading = ref(true)

const initial = computed(() => (user.value.full_name || user.value.email || 'U')[0]?.toUpperCase())

function roleLabel(role: string) {
  const labels: Record<string, string> = {
    ADMIN: 'Администратор',
    MANAGER: 'Менеджер',
    COURIER: 'Курьер',
    CUSTOMER: 'Клиент',
  }
  return labels[role] || role
}

onMounted(async () => {
  try {
    user.value = (await useApi().get('/auth/me')) as typeof user.value
  } catch {
    navigateTo('/auth/login')
  } finally {
    isLoading.value = false
  }
})
</script>
