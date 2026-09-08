<template>
  <div class="space-y-6 max-w-lg">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Настройки системы</h1>
      <p class="text-gray-500 text-sm mt-1">Информация о платформе</p>
    </div>

    <div class="card p-6">
      <h3 class="font-semibold text-gray-800 mb-4">Состояние платформы</h3>
      <dl class="space-y-1 text-sm">
        <div class="flex justify-between py-2.5 border-b border-gray-50">
          <dt class="text-gray-500">Платформа</dt>
          <dd class="font-medium">Smart Delivery AI</dd>
        </div>
        <div class="flex justify-between py-2.5 border-b border-gray-50">
          <dt class="text-gray-500">Версия API</dt>
          <dd class="font-medium">v1 (/api/v1)</dd>
        </div>
        <div class="flex justify-between py-2.5 border-b border-gray-50">
          <dt class="text-gray-500">Всего пользователей</dt>
          <dd class="font-medium">{{ counts.total }}</dd>
        </div>
        <div class="flex justify-between py-2.5 border-b border-gray-50">
          <dt class="text-gray-500">Всего заказов</dt>
          <dd class="font-medium">{{ stats?.total || 0 }}</dd>
        </div>
        <div class="flex justify-between py-2.5">
          <dt class="text-gray-500">Выручка по доставленным</dt>
          <dd class="font-medium text-emerald-600">{{ formatMoney(stats?.completed_revenue) }} ₽</dd>
        </div>
      </dl>
      <p class="text-xs text-gray-400 mt-6 leading-relaxed">
        Управление настройками окружения (ключи, SMTP, Telegram-токен) выполняется через backend/.env.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const counts = ref({ total: 0, customers: 0, couriers: 0, admins: 0 })
const stats = ref<{ total: number; completed_revenue: number } | null>(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    counts.value = (await $fetch(`${apiBase}/users/count`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as typeof counts.value
  } catch {}
  try {
    stats.value = (await $fetch(`${apiBase}/orders/stats/summary`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })) as { total: number; completed_revenue: number }
  } catch {}
  isLoading.value = false
})
</script>
