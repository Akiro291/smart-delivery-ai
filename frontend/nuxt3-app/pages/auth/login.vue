<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded shadow">
      <div>
        <h2 class="text-center text-3xl font-bold">Вход</h2>
      </div>
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium">Email</label>
          <input v-model="email" type="email" required
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Пароль</label>
          <input v-model="password" type="password" required
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
      <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
      <p class="text-center text-sm">Нет аккаунта? <NuxtLink to="/auth/register" class="text-blue-600">Регистрация</NuxtLink></p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    const response = await useApi().postForm('/auth/login', new URLSearchParams({
      username: email.value,
      password: password.value,
    }))
    localStorage.setItem('token', response.access_token)
    navigateTo('/dashboard')
  } catch (e: any) {
    if (e.response) {
      const data = e.response._data || e.response.data
      if (data?.detail === 'Incorrect email or password') {
        error.value = 'Неверный email или пароль'
      } else if (data?.detail === 'Inactive user') {
        error.value = 'Аккаунт заблокирован'
      } else {
        error.value = data?.detail || `HTTP ${e.response.status}`
      }
    } else {
      error.value = e.message || 'Нет подключения к серверу'
    }
  } finally {
    loading.value = false
  }
}
</script>
