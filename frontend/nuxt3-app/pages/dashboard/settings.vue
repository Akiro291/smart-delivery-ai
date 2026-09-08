<template>
  <div class="space-y-6 max-w-lg">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Профиль организации</h1>
      <p class="text-gray-500 text-sm mt-1">Аккаунт менеджера</p>
    </div>

    <div class="card p-6 space-y-5">
      <div>
        <label class="label">Email</label>
        <input type="email" :value="authStore.user?.email || ''" disabled class="input bg-gray-50" />
      </div>
      <div>
        <label class="label">Полное имя</label>
        <input v-model="fullName" type="text" class="input" />
      </div>
      <div>
        <label class="label">Телефон</label>
        <input v-model="phone" type="tel" class="input" />
      </div>
      <UiAlert v-if="saved" text="Профиль обновлён" tone="success" />
      <UiButton :loading="isSaving" @click="save">Сохранить изменения</UiButton>
    </div>

    <div class="card p-6">
      <h3 class="font-semibold text-gray-800 mb-4">Информация о системе</h3>
      <dl class="space-y-3 text-sm">
        <div class="flex justify-between py-1.5 border-b border-gray-50">
          <dt class="text-gray-500">Платформа</dt>
          <dd class="font-medium">Smart Delivery AI</dd>
        </div>
        <div class="flex justify-between py-1.5 border-b border-gray-50">
          <dt class="text-gray-500">Версия API</dt>
          <dd class="font-medium">v1 (/api/v1)</dd>
        </div>
        <div class="flex justify-between py-1.5">
          <dt class="text-gray-500">Всего заказов</dt>
          <dd class="font-medium">{{ statsTotal ?? '—' }}</dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

const authStore = useAuthStore()
const ordersStore = useOrdersStore()
const apiBase = useRuntimeConfig().public.apiBase
const fullName = ref(authStore.user?.full_name || '')
const phone = ref(authStore.user?.phone || '')
const isSaving = ref(false)
const saved = ref(false)
const statsTotal = ref<number | null>(null)

onMounted(async () => {
  authStore.fetchUser()
  const stats = await ordersStore.fetchStats()
  statsTotal.value = stats?.total ?? null
})

async function save() {
  if (!authStore.user) return
  isSaving.value = true
  saved.value = false
  try {
    await $fetch(`${apiBase}/users/${authStore.user.id}`, {
      method: 'PUT',
      body: { full_name: fullName.value || null, phone: phone.value || null },
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await authStore.fetchUser()
    saved.value = true
    setTimeout(() => (saved.value = false), 3000)
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка сохранения')
  } finally {
    isSaving.value = false
  }
}
</script>
