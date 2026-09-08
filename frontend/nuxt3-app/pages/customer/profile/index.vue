<template>
  <div class="space-y-6 max-w-lg">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Мой профиль</h1>
      <p class="text-gray-500 text-sm mt-1">Личные данные аккаунта</p>
    </div>

    <div class="card overflow-hidden">
      <div class="bg-gradient-to-r from-brand-600 to-brand-800 px-6 py-8 text-white flex items-center gap-4">
        <div class="h-16 w-16 rounded-2xl bg-white/15 backdrop-blur flex items-center justify-center text-2xl font-bold border border-white/20">
          {{ initial }}
        </div>
        <div>
          <p class="font-bold text-lg">{{ authStore.user?.full_name || 'Без имени' }}</p>
          <p class="text-white/60 text-sm">{{ authStore.user?.email }}</p>
        </div>
      </div>
      <div class="p-6 space-y-5">
        <div>
          <label class="label">Email</label>
          <input type="email" :value="authStore.user?.email || ''" disabled class="input bg-gray-50" />
        </div>
        <div>
          <label class="label">Имя</label>
          <input v-model="fullName" type="text" class="input" />
        </div>
        <div>
          <label class="label">Телефон</label>
          <input v-model="phone" type="tel" class="input" />
        </div>
        <UiAlert v-if="saved" text="Профиль обновлён" tone="success" />
        <UiButton :loading="isSaving" @click="save">Сохранить изменения</UiButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const fullName = ref(authStore.user?.full_name || '')
const phone = ref(authStore.user?.phone || '')
const isSaving = ref(false)
const saved = ref(false)

const initial = computed(() => (authStore.user?.full_name || authStore.user?.email || 'U')[0]?.toUpperCase())

onMounted(async () => {
  await authStore.fetchUser()
  fullName.value = authStore.user?.full_name || ''
  phone.value = authStore.user?.phone || ''
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
