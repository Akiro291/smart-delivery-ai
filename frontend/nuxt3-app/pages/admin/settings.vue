<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Настройки системы</h1>
    <div class="bg-white p-6 rounded shadow max-w-2xl">
      <h3 class="text-lg font-semibold mb-4">Информация о системе</h3>
      <dl class="space-y-3 text-sm">
        <div class="flex justify-between border-b pb-2">
          <dt class="text-gray-500">Платформа</dt>
          <dd class="font-medium">Smart Delivery AI</dd>
        </div>
        <div class="flex justify-between border-b pb-2">
          <dt class="text-gray-500">Версия API</dt>
          <dd class="font-medium">v1 (/api/v1)</dd>
        </div>
        <div class="flex justify-between border-b pb-2">
          <dt class="text-gray-500">Всего пользователей</dt>
          <dd class="font-medium">{{ counts.total }}</dd>
        </div>
        <div class="flex justify-between border-b pb-2">
          <dt class="text-gray-500">Всего заказов</dt>
          <dd class="font-medium">{{ stats?.total || 0 }}</dd>
        </div>
      </dl>
      <p class="text-sm text-gray-400 mt-6">
        Управление настройками окружения (ключи, SMTP, Telegram) выполняется через backend/.env.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const counts = ref({ total: 0, customers: 0, couriers: 0, admins: 0 })
const stats = ref<{ total: number } | null>(null)

onMounted(async () => {
  try {
    counts.value = (await $fetch(`${apiBase}/users/count`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as typeof counts.value
  } catch {}
  try {
    stats.value = (await $fetch(`${apiBase}/orders/stats/summary`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as { total: number }
  } catch {}
})
</script>
