<template>
  <div class="max-w-sm mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold tracking-tight">Сброс пароля</h1>
      <p class="text-gray-500 text-sm mt-1.5">Отправим одноразовый токен на ваш email</p>
    </div>

    <template v-if="!sent">
      <form @submit.prevent="handleReset" class="space-y-5">
        <div>
          <label class="label" for="email">Email</label>
          <input id="email" v-model="email" type="email" required autocomplete="email" class="input" placeholder="you@company.com" />
        </div>
        <UiAlert v-if="error" :text="error" @dismiss="error = ''" />
        <UiButton type="submit" block :loading="loading">Отправить токен</UiButton>
      </form>
    </template>

    <template v-else>
      <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-5 text-sm text-emerald-800">
        ✅ Если email зарегистрирован, токен отправлен. Проверьте почту — срок действия токена 1 час.
      </div>
      <div class="mt-6">
        <label class="label" for="token">Токен из письма</label>
        <input id="token" v-model="token" type="text" class="input font-mono text-xs" placeholder="eyJ..." />
      </div>
      <div class="mt-4">
        <label class="label" for="newPassword">Новый пароль</label>
        <input id="newPassword" v-model="newPassword" type="password" minlength="8" class="input" placeholder="Минимум 8 символов" />
      </div>
      <UiAlert v-if="confirmError" :text="confirmError" class="mt-4" @dismiss="confirmError = ''" />
      <UiButton class="mt-5" block :loading="confirming" :disabled="!token || !newPassword" @click="confirmReset">
        Сменить пароль
      </UiButton>
    </template>

    <p class="text-center text-sm text-gray-500 mt-8">
      <NuxtLink to="/auth/login" class="font-semibold text-brand-600 hover:text-brand-700">&larr; Назад ко входу</NuxtLink>
    </p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'guest', layout: 'auth' })

const apiBase = useRuntimeConfig().public.apiBase
const email = ref('')
const loading = ref(false)
const error = ref('')
const sent = ref(false)
const token = ref('')
const newPassword = ref('')
const confirming = ref(false)
const confirmError = ref('')

async function handleReset() {
  loading.value = true
  error.value = ''
  try {
    await $fetch(`${apiBase}/auth/reset-password`, { method: 'POST', body: { email: email.value } })
    sent.value = true
  } catch (e: any) {
    if (e.response?.status === 429) error.value = 'Слишком много запросов. Попробуйте позже.'
    else error.value = e.response?.data?.detail || 'Не удалось отправить запрос'
  } finally {
    loading.value = false
  }
}

async function confirmReset() {
  confirming.value = true
  confirmError.value = ''
  try {
    await $fetch(`${apiBase}/auth/reset-password/confirm`, {
      method: 'POST',
      body: { token: token.value.trim(), new_password: newPassword.value },
    })
    navigateTo('/auth/login')
  } catch (e: any) {
    confirmError.value = e.response?.data?.detail || 'Не удалось сменить пароль'
  } finally {
    confirming.value = false
  }
}

useHead({ title: 'Сброс пароля — Smart Delivery AI' })
</script>
