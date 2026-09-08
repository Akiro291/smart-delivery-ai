<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Клиенты</h1>
      <p class="text-gray-500 text-sm mt-1">Пользователи платформы с ролью «Клиент»</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="client in clients" :key="client.id" class="card card-hover p-6">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-full bg-gradient-to-br from-brand-400 to-brand-600 text-white font-bold flex items-center justify-center text-lg flex-shrink-0">
            {{ initials(client.full_name || client.email) }}
          </div>
          <div class="min-w-0">
            <h3 class="font-semibold text-gray-800 truncate">{{ client.full_name || 'Без имени' }}</h3>
            <p class="text-xs text-gray-500 truncate">{{ client.email }}</p>
          </div>
          <span :class="client.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'" class="badge ml-auto flex-shrink-0">
            <span class="h-1.5 w-1.5 rounded-full bg-current" />
            {{ client.is_active ? 'Активен' : 'Неактивен' }}
          </span>
        </div>
        <div v-if="client.phone" class="mt-4 pt-4 border-t border-gray-50 text-sm text-gray-500 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.3a1 1 0 01.97.76l.8 3.2a1 1 0 01-.53 1.13l-1.9.95a12 12 0 005.42 5.42l.95-1.9a1 1 0 011.13-.53l3.2.8a1 1 0 01.76.97V17a2 2 0 01-2 2h-1C9.7 19 3 12.3 3 4V3a2 2 0 012-2z" />
          </svg>
          {{ client.phone }}
        </div>
      </div>
    </div>

    <UiSpinner v-if="isLoading" label="Загрузка…" />
    <div v-else-if="clients.length === 0" class="card">
      <UiEmptyState icon="👥" title="Клиентов пока нет" description="Клиенты появятся после первой регистрации" />
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

interface UserRow {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  is_active: boolean
}

const authStore = useAuthStore()
const clients = ref<UserRow[]>([])
const isLoading = ref(true)
const apiBase = useRuntimeConfig().public.apiBase

onMounted(async () => {
  try {
    clients.value = (await $fetch(`${apiBase}/users/?role=CUSTOMER&limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as UserRow[]
  } catch {
    clients.value = []
  } finally {
    isLoading.value = false
  }
})

function initials(name: string) {
  const parts = name.replace(/@.*/, '').split(/[\s._-]+/).filter(Boolean)
  return ((parts[0]?.[0] || '?') + (parts[1]?.[0] || '')).toUpperCase()
}
</script>
