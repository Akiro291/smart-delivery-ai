<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded shadow">
      <div>
        <h2 class="text-center text-3xl font-bold">Регистрация</h2>
        <p class="text-center text-gray-500 text-sm mt-2">Smart Delivery AI</p>
      </div>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium">Имя</label>
          <input v-model="fullName" type="text" required
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Email</label>
          <input v-model="email" type="email" required
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Телефон</label>
          <input v-model="phone" type="tel"
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium">Пароль</label>
          <input v-model="password" type="password" required minlength="6"
            class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <button type="submit" :disabled="loading"
          class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>
      <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
      <p class="text-center text-sm">Уже есть аккаунт? <NuxtLink to="/auth/login" class="text-blue-600">Войти</NuxtLink></p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const authStore = useAuthStore()
const fullName = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const error = ref('')

async function handleRegister() {
  error.value = ''
  try {
    await authStore.register(fullName.value, email.value, password.value, phone.value || undefined)
    
    const role = authStore.user?.role
    if (role === 'ADMIN') {
      return navigateTo('/admin')
    } else if (role === 'COURIER') {
      return navigateTo('/courier')
    } else {
      return navigateTo('/customer')
    }
  } catch (e: any) {
    console.error('Register error:', e)
    console.error('Error response:', e.response)
    console.error('Error statusCode:', e.statusCode)
    console.error('Error message:', e.message)
    console.error('Error status:', e.status)
    
    let errorMessage = ''
    
    if (e.response?.data?.detail) {
      const detail = e.response.data.detail
      console.error('Detail:', detail)
      if (detail === 'Email already registered') {
        errorMessage = 'Email уже зарегистрирован'
      } else if (typeof detail === 'string') {
        errorMessage = detail
      } else {
        errorMessage = JSON.stringify(detail)
      }
    } else if (e.statusCode === 401 || e.status === 401) {
      errorMessage = 'Ошибка авторизации (401). Проверьте настройки CORS или SECRET_KEY.'
    } else if (e.statusCode || e.status) {
      errorMessage = `Ошибка сервера (${e.statusCode || e.status}). Проверьте консоль разработчика (F12) для деталей.`
    } else if (e.message?.includes('fetch') || e.message?.includes('network') || e.message?.includes('NetworkError')) {
      errorMessage = 'Не удалось подключиться к серверу. Убедитесь, что backend запущен на порту 8000.'
    } else {
      errorMessage = `Произошла ошибка: ${e.message || 'Неизвестная ошибка'}`
    }
    
    error.value = errorMessage
  }
}
</script>
