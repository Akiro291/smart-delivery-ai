<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded shadow">
      <h2 class="text-center text-3xl font-bold">Сброс пароля</h2>
      <form @submit.prevent="handleReset" class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Email</label>
          <input v-model="email" type="email" required
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {{ loading ? 'Отправка...' : 'Отправить' }}
        </button>
      </form>
      <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
      <p class="text-center text-sm"><NuxtLink to="/auth/login" class="text-blue-600">← Назад ко входу</NuxtLink></p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const email = ref('')
const loading = ref(false)
const error = ref('')

async function handleReset() {
  loading.value = true
  error.value = ''
  try {
    await $fetch('/api/v1/auth/reset-password', {
      method: 'POST',
      body: { email: email.value },
    })
    error.value = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Ошибка'
  } finally {
    loading.value = false
  }
}
</script>
