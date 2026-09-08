<template>
  <div class="min-h-screen grid lg:grid-cols-2">
    <!-- Брендированная панель -->
    <div class="auth-panel relative hidden lg:flex flex-col justify-between p-12 text-white overflow-hidden">
      <div class="absolute inset-0 bg-grid opacity-30" />
      <div class="relative">
        <NuxtLink to="/" class="flex items-center gap-2.5">
          <div class="h-10 w-10 rounded-xl bg-white/10 backdrop-blur flex items-center justify-center border border-white/20">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="text-lg font-bold tracking-tight">Smart Delivery</span>
        </NuxtLink>
      </div>
      <div class="relative max-w-md">
        <h2 class="text-4xl font-extrabold leading-tight tracking-tight">
          Доставка под контролем.<br />Без хаоса.
        </h2>
        <p class="mt-5 text-white/70 leading-relaxed">
          Живой трекинг заказов, управление курьерами и AI-ассистент — всё в одном окне.
        </p>
        <ul class="mt-8 space-y-3.5 text-sm">
          <li v-for="point in points" :key="point" class="flex items-center gap-3">
            <span class="h-5 w-5 rounded-full bg-emerald-400/20 border border-emerald-300/40 flex items-center justify-center flex-shrink-0">
              <svg class="h-3 w-3 text-emerald-300" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </span>
            {{ point }}
          </li>
        </ul>
      </div>
      <p class="relative text-xs text-white/40">© {{ year }} Smart Delivery AI</p>
    </div>

    <!-- Форма -->
    <div class="flex flex-col items-center justify-center p-6 sm:p-12 bg-white">
      <div class="w-full max-w-md animate-fade-up">
        <NuxtLink to="/" class="lg:hidden flex items-center justify-center gap-2.5 mb-10">
          <div class="h-9 w-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
            <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="text-lg font-bold">Smart Delivery</span>
        </NuxtLink>
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()

const points = [
  'Real-time трекинг через WebSocket',
  'Четыре роли: админ, менеджер, курьер, клиент',
  'AI-ассистент и прогноз времени доставки',
  'Уведомления: email, Telegram, in-app',
]
</script>
