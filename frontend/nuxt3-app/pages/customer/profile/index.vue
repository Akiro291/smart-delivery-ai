<template>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Мой профиль</h1>
      <div class="bg-white p-6 rounded shadow max-w-lg">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <p class="mt-1 text-gray-900">{{ authStore.user?.email || '-' }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Имя</label>
            <input v-model="fullName" type="text" class="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Телефон</label>
            <input v-model="phone" type="text" class="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <button
            @click="save"
            :disabled="isSaving"
            class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50"
          >
            {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
          </button>
          <p v-if="saved" class="text-green-600 text-sm">Профиль обновлён</p>
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
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка сохранения')
  } finally {
    isSaving.value = false
  }
}
</script>
