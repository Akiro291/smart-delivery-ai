<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Курьеры</h1>
      <p class="text-gray-500 text-sm mt-1">Список курьеров платформы (админ)</p>
    </div>

    <div class="card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="table-base">
          <thead>
            <tr>
              <th>Курьер</th>
              <th>Email</th>
              <th>Телефон</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in couriers" :key="user.id">
              <td class="font-medium text-gray-800">{{ user.full_name || 'Без имени' }}</td>
              <td class="text-gray-500">{{ user.email }}</td>
              <td class="text-gray-500">{{ user.phone || '—' }}</td>
              <td>
                <span :class="user.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'" class="badge">
                  <span class="h-1.5 w-1.5 rounded-full bg-current" />
                  {{ user.is_active ? 'Активен' : 'Неактивен' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <UiSpinner v-if="isLoading" label="Загрузка…" />
      <div v-else-if="couriers.length === 0">
        <UiEmptyState icon="🚚" title="Курьеров нет" description="Заявки на роль курьера одобряются в разделе «Роли»" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface UserRow {
  id: number
  email: string
  full_name: string | null
  phone: string | null
  is_active: boolean
}

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const couriers = ref<UserRow[]>([])
const isLoading = ref(true)

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
</script>
