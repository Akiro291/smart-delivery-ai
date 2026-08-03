<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded shadow">
      <div>
        <h2 class="text-center text-3xl font-bold">Вход</h2>
        <p class="text-center text-gray-500 text-sm mt-2">Smart Delivery AI</p>
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

const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    
    const role = authStore.user?.role
    if (role === 'ADMIN') {
      return navigateTo('/admin')
    } else if (role === 'COURIER') {
      return navigateTo('/courier')
    } else {
      return navigateTo('/customer')
    }
  } catch (e: any) {
    console.error('Login error:', e)
    let errorMessage = ''
    
    if (e.response?.data?.detail) {
      const detail = e.response.data.detail
      if (detail === 'Incorrect email or password') {
        errorMessage = 'Неверный email или пароль'
      } else if (detail === 'Inactive user') {
        errorMessage = 'Аккаунт заблокирован'
      } else {
        errorMessage = detail
      }
    } else if (e.statusCode || e.status) {
      errorMessage = `Ошибка сервера (${e.statusCode || e.status}). Проверьте, запущен ли backend.`
    } else if (e.message?.includes('fetch') || e.message?.includes('network')) {
      errorMessage = 'Не удалось подключиться к серверу. Убедитесь, что backend запущен на порту 8000.'
    } else {
      errorMessage = 'Произошла ошибка при входе'
    }
    
    error.value = errorMessage
  }
}
</script>
