<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Курьеры</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="courier in couriers" :key="courier.id" class="bg-white p-6 rounded shadow">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold text-lg">
            {{ initials(courier.full_name || courier.email) }}
          </div>
          <div>
            <h3 class="font-semibold">{{ courier.full_name || 'Без имени' }}</h3>
            <p class="text-sm" :class="courier.is_active ? 'text-green-600' : 'text-red-500'">
              {{ courier.is_active ? 'Активен' : 'Неактивен' }}
            </p>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t flex justify-between text-sm">
          <span class="text-gray-500">{{ courier.email }}</span>
          <span v-if="courier.phone" class="text-gray-500">{{ courier.phone }}</span>
        </div>
      </div>
    </div>
    <div v-if="couriers.length === 0" class="text-center py-12 text-gray-500">Курьеров пока нет</div>
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
const apiBase = useRuntimeConfig().public.apiBase

onMounted(async () => {
  try {
    couriers.value = (await $fetch(`${apiBase}/users/?role=COURIER&limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as UserRow[]
  } catch {
    couriers.value = []
  }
})

function initials(name: string) {
  const parts = name.replace(/@.*/, '').split(/[\s._-]+/).filter(Boolean)
  return (parts[0]?.[0] || '?') + (parts[1]?.[0] || '')
}
</script>
