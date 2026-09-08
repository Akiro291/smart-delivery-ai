<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold tracking-tight">Создайте аккаунт</h1>
      <p class="text-gray-500 text-sm mt-1.5">Минута — и вы можете оформить первый заказ</p>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-5">
      <div>
        <label class="label" for="fullName">Имя</label>
        <input id="fullName" v-model="fullName" type="text" required autocomplete="name" class="input" placeholder="Иван Петров" />
      </div>
      <div>
        <label class="label" for="email">Email</label>
        <input id="email" v-model="email" type="email" required autocomplete="email" class="input" placeholder="you@company.com" />
      </div>
      <div>
        <label class="label" for="phone">Телефон <span class="text-gray-400 font-normal">(необязательно)</span></label>
        <input id="phone" v-model="phone" type="tel" autocomplete="tel" class="input" placeholder="+7 999 000-00-00" />
      </div>
      <div>
        <label class="label" for="password">Пароль</label>
        <input id="password" v-model="password" type="password" required minlength="6" autocomplete="new-password" class="input" placeholder="Минимум 6 символов" />
        <div v-if="password" class="mt-2 flex gap-1">
          <div v-for="i in 3" :key="i" class="h-1 flex-1 rounded-full" :class="strengthClass(i)" />
        </div>
        <p v-if="password" class="text-xs mt-1.5" :class="strengthTextClass">{{ strengthLabel }}</p>
      </div>

      <UiAlert v-if="error" :text="error" @dismiss="error = ''" />

      <UiButton type="submit" block :loading="loading">Зарегистрироваться</UiButton>
    </form>

    <p class="text-center text-sm text-gray-500 mt-8">
      Уже есть аккаунт?
      <NuxtLink to="/auth/login" class="font-semibold text-brand-600 hover:text-brand-700">Войти</NuxtLink>
    </p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest', layout: 'auth' })

const authStore = useAuthStore()
const fullName = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const strengthScore = computed(() => {
  const p = password.value
  if (!p) return 0
  let score = 1
  if (p.length >= 8) score++
  if (/[A-ZА-Я]/.test(p) && /[a-zа-я]/.test(p)) score++
  if (/\d/.test(p) || /[^\w\s]/.test(p)) score++
  return Math.min(score, 3)
})

const strengthLabel = computed(() => ['Слабый', 'Слабый', 'Средний', 'Надёжный'][strengthScore.value])
const strengthTextClass = computed(
  () => ['text-gray-400', 'text-red-500', 'text-amber-500', 'text-emerald-600'][strengthScore.value],
)

function strengthClass(step: number) {
  return strengthScore.value >= step ? 'bg-brand-500' : 'bg-gray-200'
}

const ROLE_HOME: Record<string, string> = {
  ADMIN: '/admin',
  MANAGER: '/dashboard',
  COURIER: '/courier',
  CUSTOMER: '/customer',
}

async function handleRegister() {
  error.value = ''
  loading.value = true
  try {
    await authStore.register(fullName.value, email.value, password.value, phone.value || undefined)
    const role = authStore.user?.role
    return navigateTo((role && ROLE_HOME[role]) || '/customer')
  } catch (e: any) {
    let message = 'Произошла ошибка при регистрации'
    if (e.response?.data?.detail) {
      const detail = e.response.data.detail
      if (detail === 'Email already registered') message = 'Этот email уже зарегистрирован'
      else if (typeof detail === 'string') message = detail
      else message = JSON.stringify(detail)
    } else if (e.statusCode || e.status) {
      message = `Ошибка сервера (${e.statusCode || e.status}). Проверьте, запущен ли backend.`
    } else if (e.message?.includes('fetch') || e.message?.includes('NetworkError')) {
      message = 'Не удалось подключиться к серверу. Backend должен быть запущен на порту 8000.'
    }
    error.value = message
  } finally {
    loading.value = false
  }
}

useHead({ title: 'Регистрация — Smart Delivery AI' })
</script>
