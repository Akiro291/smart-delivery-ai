<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Профиль организации</h1>
    <div class="bg-white rounded shadow p-6 max-w-lg">
      <h3 class="text-lg font-semibold mb-4">Данные аккаунта</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Email</label>
          <input type="email" :value="authStore.user?.email || ''" disabled
            class="mt-1 block w-full px-3 py-2 border rounded bg-gray-50 text-gray-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Полное имя</label>
          <input v-model="fullName" type="text"
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Телефон</label>
          <input v-model="phone" type="text"
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button @click="save" :disabled="isSaving"
          class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
        </button>
        <p v-if="saved" class="text-green-600 text-sm">Профиль обновлён</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const fullName = ref(authStore.user?.full_name || '')
const phone = ref(authStore.user?.phone || '')
const isSaving = ref(false)
const saved = ref(false)

onMounted(() => {
  authStore.fetchUser()
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
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка сохранения')
  } finally {
    isSaving.value = false
  }
}
</script>
