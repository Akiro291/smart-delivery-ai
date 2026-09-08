<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold tracking-tight">С возвращением 👋</h1>
      <p class="text-gray-500 text-sm mt-1.5">Войдите, чтобы продолжить работу</p>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-5">
      <div>
        <label class="label" for="email">Email</label>
        <input id="email" v-model="email" type="email" required autocomplete="email" class="input" placeholder="you@company.com" />
      </div>
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <label class="label !mb-0" for="password">Пароль</label>
          <NuxtLink to="/auth/reset-password" class="text-xs font-medium text-brand-600 hover:text-brand-700">Забыли?</NuxtLink>
        </div>
        <input id="password" v-model="password" type="password" required autocomplete="current-password" class="input" placeholder="••••••••" />
      </div>

      <UiAlert v-if="error" :text="error" @dismiss="error = ''" />

      <UiButton type="submit" block :loading="loading">Войти</UiButton>
    </form>

    <p class="text-center text-sm text-gray-500 mt-8">
      Нет аккаунта?
      <NuxtLink to="/auth/register" class="font-semibold text-brand-600 hover:text-brand-700">Создать бесплатно</NuxtLink>
    </p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest', layout: 'auth' })

const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const ROLE_HOME: Record<string, string> = {
  ADMIN: '/admin',
  MANAGER: '/dashboard',
  COURIER: '/courier',
  CUSTOMER: '/customer',
}

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    const role = authStore.user?.role
    return navigateTo((role && ROLE_HOME[role]) || '/customer')
  } catch (e: any) {
    let message = 'Произошла ошибка при входе'
    if (e.response?.data?.detail) {
      const detail = e.response.data.detail
      if (detail === 'Incorrect email or password') message = 'Неверный email или пароль'
      else if (detail === 'Inactive user') message = 'Аккаунт заблокирован. Обратитесь к администратору.'
      else if (detail === 'Too many requests. Try again later.') message = 'Слишком много попыток. Подождите пару минут.'
      else message = detail
    } else if (e.statusCode || e.status) {
      message = `Ошибка сервера (${e.statusCode || e.status}). Проверьте, запущен ли backend.`
    } else if (e.message?.includes('fetch') || e.message?.includes('network')) {
      message = 'Не удалось подключиться к серверу. Backend должен быть запущен на порту 8000.'
    }
    error.value = message
  } finally {
    loading.value = false
  }
}

useHead({ title: 'Вход — Smart Delivery AI' })
</script>
