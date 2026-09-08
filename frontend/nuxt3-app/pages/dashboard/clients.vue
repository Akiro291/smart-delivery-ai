<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Клиенты</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="client in clients" :key="client.id" class="bg-white p-6 rounded shadow">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-lg">
            {{ initials(client.full_name || client.email) }}
          </div>
          <div>
            <h3 class="font-semibold">{{ client.full_name || 'Без имени' }}</h3>
            <p class="text-sm text-gray-500">{{ client.email }}</p>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t flex justify-between text-sm">
          <span class="text-gray-500">Статус: {{ client.is_active ? 'активен' : 'неактивен' }}</span>
          <span v-if="client.phone" class="text-gray-500">{{ client.phone }}</span>
        </div>
      </div>
    </div>
    <div v-if="clients.length === 0" class="text-center py-12 text-gray-500">Клиентов пока нет</div>
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
const apiBase = useRuntimeConfig().public.apiBase

onMounted(async () => {
  try {
    clients.value = (await $fetch(`${apiBase}/users/?role=CUSTOMER&limit=100`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as UserRow[]
  } catch {
    clients.value = []
  }
})

function initials(name: string) {
  const parts = name.replace(/@.*/, '').split(/[\s._-]+/).filter(Boolean)
  return (parts[0]?.[0] || '?') + (parts[1]?.[0] || '')
}
</script>
