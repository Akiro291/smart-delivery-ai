<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Курьеры</h1>
      <p class="text-gray-500 text-sm mt-1">Список всех курьеров платформы</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
      <div v-for="courier in couriers" :key="courier.id" class="card card-hover p-6">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 text-white font-bold flex items-center justify-center text-lg flex-shrink-0">
            {{ initials(courier.full_name || courier.email) }}
          </div>
          <div class="min-w-0">
            <h3 class="font-semibold text-gray-800 truncate">{{ courier.full_name || 'Без имени' }}</h3>
            <p class="text-xs text-gray-500 truncate">{{ courier.email }}</p>
          </div>
          <span :class="courier.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'" class="badge ml-auto flex-shrink-0">
            <span class="h-1.5 w-1.5 rounded-full bg-current" />
            {{ courier.is_active ? 'Активен' : 'Неактивен' }}
          </span>
        </div>
        <div v-if="courier.phone" class="mt-4 pt-4 border-t border-gray-50 text-sm text-gray-500 flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.3a1 1 0 01.97.76l.8 3.2a1 1 0 01-.53 1.13l-1.9.95a12 12 0 005.42 5.42l.95-1.9a1 1 0 011.13-.53l3.2.8a1 1 0 01.76.97V17a2 2 0 01-2 2h-1C9.7 19 3 12.3 3 4V3a2 2 0 012-2z" />
          </svg>
          {{ courier.phone }}
        </div>
      </div>
    </div>

    <UiSpinner v-if="isLoading" label="Загрузка…" />
    <div v-else-if="couriers.length === 0" class="card">
      <UiEmptyState icon="🚚" title="Курьеров пока нет" description="Курьеры появятся после регистрации и одобрения заявки на роль" />
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
const couriers = ref<UserRow[]>([])
const isLoading = ref(true)
const apiBase = useRuntimeConfig().public.apiBase

onMounted(async () => {
  try {
    couriers.value = (await $fetch(`${apiBase}/users/?role=COURIER&limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as UserRow[]
  } catch {
    couriers.value = []
  } finally {
    isLoading.value = false
  }
})

function initials(name: string) {
  const parts = name.replace(/@.*/, '').split(/[\s._-]+/).filter(Boolean)
  return ((parts[0]?.[0] || '?') + (parts[1]?.[0] || '')).toUpperCase()
}
</script>
