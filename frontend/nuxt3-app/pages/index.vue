<template>
  <div class="min-h-screen bg-white">
    <!-- Шапка -->
    <header class="fixed top-0 inset-x-0 z-50 backdrop-blur-lg bg-white/80 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-2.5">
            <div class="h-9 w-9 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-glow">
              <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span class="text-lg font-bold tracking-tight">Smart <span class="text-gradient">Delivery</span></span>
          </div>
          <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-gray-600">
            <a href="#features" class="hover:text-gray-900 transition-colors">Возможности</a>
            <a href="#roles" class="hover:text-gray-900 transition-colors">Для кого</a>
            <a href="#stack" class="hover:text-gray-900 transition-colors">Технологии</a>
          </nav>
          <div class="flex items-center gap-3">
            <NuxtLink to="/auth/login" class="btn-ghost">Войти</NuxtLink>
            <NuxtLink to="/auth/register" class="btn-primary hidden sm:inline-flex">Начать бесплатно</NuxtLink>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero -->
    <section class="relative overflow-hidden bg-grid pt-32 pb-24">
      <div class="absolute inset-0 bg-gradient-to-b from-brand-50/60 via-transparent to-transparent" />
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 border border-brand-200 text-brand-700 text-xs font-semibold mb-8 animate-fade-up">
          <span class="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Real-time трекинг · AI-ассистент · Open API
        </div>
        <h1 class="text-5xl md:text-7xl font-extrabold tracking-tight leading-[1.05] animate-fade-up" style="animation-delay: 0.05s">
          Доставка под контролем.<br />
          <span class="text-gradient">Без хаоса.</span>
        </h1>
        <p class="mt-6 text-lg md:text-xl text-gray-600 max-w-2xl mx-auto animate-fade-up" style="animation-delay: 0.1s">
          SaaS-платформа для курьерской логистики: заказы, курьеры, клиенты и аналитика —
          в одном окне, с живым трекингом и AI-помощником.
        </p>
        <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-up" style="animation-delay: 0.15s">
          <NuxtLink to="/auth/register" class="btn-primary text-base px-8 py-3.5 shadow-glow">
            Попробовать бесплатно
            <svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </NuxtLink>
          <a href="#features" class="btn-secondary text-base px-8 py-3.5">Как это работает</a>
        </div>

        <!-- Макет дашборда -->
        <div class="mt-16 max-w-4xl mx-auto animate-fade-up" style="animation-delay: 0.25s">
          <div class="rounded-2xl border border-gray-200 bg-white shadow-card-hover overflow-hidden">
            <div class="flex items-center gap-1.5 px-4 py-3 bg-gray-50 border-b border-gray-100">
              <span class="h-3 w-3 rounded-full bg-red-400" />
              <span class="h-3 w-3 rounded-full bg-amber-400" />
              <span class="h-3 w-3 rounded-full bg-emerald-400" />
              <span class="ml-3 text-xs text-gray-400 font-medium">smart-delivery — дашборд</span>
            </div>
            <div class="grid grid-cols-3 gap-4 p-6 md:p-8">
              <div class="rounded-xl bg-gradient-to-br from-brand-600 to-brand-800 text-white p-4 text-left">
                <p class="text-xs text-white/60">Заказов сегодня</p>
                <p class="text-2xl font-bold mt-1">128</p>
              </div>
              <div class="rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-700 text-white p-4 text-left">
                <p class="text-xs text-white/60">Доставлено</p>
                <p class="text-2xl font-bold mt-1">94</p>
              </div>
              <div class="rounded-xl bg-gradient-to-br from-amber-500 to-orange-600 text-white p-4 text-left">
                <p class="text-xs text-white/60">В пути</p>
                <p class="text-2xl font-bold mt-1">31</p>
              </div>
              <div class="col-span-3 rounded-xl border border-gray-100 bg-gray-50/60 p-4">
                <div class="flex items-center justify-between mb-3">
                  <span class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Живой трекинг</span>
                  <span class="text-xs text-emerald-600 font-medium flex items-center gap-1.5">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" /> онлайн
                  </span>
                </div>
                <div class="space-y-2.5">
                  <div v-for="(row, i) in trackingRows" :key="i" class="flex items-center gap-3">
                    <span class="text-xs text-gray-400 w-12">#{{ 1000 + i }}</span>
                    <div class="flex-1 h-2 rounded-full bg-gray-200 overflow-hidden">
                      <div
                        class="h-full rounded-full bg-gradient-to-r from-brand-500 to-violet-500 transition-all duration-1000"
                        :style="{ width: row.progress + '%' }"
                      />
                    </div>
                    <span class="text-xs font-medium text-gray-600 w-10 text-right">{{ row.progress }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Возможности -->
    <section id="features" class="py-24 bg-gray-50/60">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <p class="text-sm font-semibold text-brand-600 uppercase tracking-widest mb-3">Возможности</p>
          <h2 class="text-3xl md:text-4xl font-bold tracking-tight">Всё, что нужно сервису доставки</h2>
          <p class="mt-4 text-gray-600">От корзины до аналитики — без внешних клеёв и ручных таблиц.</p>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div v-for="feature in features" :key="feature.title" class="card card-hover p-7">
            <div class="h-12 w-12 rounded-xl flex items-center justify-center text-2xl mb-5" :class="feature.bg">
              {{ feature.icon }}
            </div>
            <h3 class="text-lg font-bold mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600 text-sm leading-relaxed">{{ feature.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Роли -->
    <section id="roles" class="py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <p class="text-sm font-semibold text-brand-600 uppercase tracking-widest mb-3">Для кого</p>
          <h2 class="text-3xl md:text-4xl font-bold tracking-tight">Четыре роли — четыре личных кабинета</h2>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="role in roles" :key="role.title" class="card card-hover p-6 text-center">
            <div class="text-4xl mb-4">{{ role.icon }}</div>
            <h3 class="font-bold">{{ role.title }}</h3>
            <p class="text-sm text-gray-600 mt-2">{{ role.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Стек -->
    <section id="stack" class="py-24 bg-gray-900 text-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm font-semibold text-brand-400 uppercase tracking-widest mb-3">Технологии</p>
        <h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-12">Современный стек, продуманная архитектура</h2>
        <div class="flex flex-wrap justify-center gap-3">
          <span v-for="tech in stack" :key="tech" class="px-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm font-medium hover:bg-white/10 transition-colors">
            {{ tech }}
          </span>
        </div>
        <p class="mt-10 text-gray-400 text-sm max-w-xl mx-auto">
          Модульный монолит: слои API → Services → Repositories → DB, готовность к выделению микросервисов при росте.
        </p>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-24">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="auth-panel rounded-3xl px-8 py-16 text-center text-white relative overflow-hidden">
          <div class="absolute inset-0 bg-grid opacity-40" />
          <div class="relative">
            <h2 class="text-3xl md:text-4xl font-bold tracking-tight">Готовы навести порядок в доставке?</h2>
            <p class="mt-4 text-white/70 max-w-lg mx-auto">Регистрация занимает минуту. Клиентский кабинет доступен сразу.</p>
            <NuxtLink to="/auth/register" class="mt-8 inline-flex btn bg-white text-brand-700 hover:bg-brand-50 text-base px-8 py-3.5 font-semibold">
              Создать аккаунт
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Подвал -->
    <footer class="border-t border-gray-100 py-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
        <div class="flex items-center gap-2">
          <div class="h-6 w-6 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
            <svg class="h-3.5 w-3.5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="font-semibold text-gray-700">Smart Delivery AI</span>
        </div>
        <p>© {{ year }} — учебно-портфельный проект</p>
        <div class="flex gap-6">
          <a href="https://github.com/Akiro291/smart-delivery-ai" target="_blank" rel="noopener" class="hover:text-gray-900 transition-colors">GitHub</a>
          <a href="http://localhost:8000/docs" target="_blank" rel="noopener" class="hover:text-gray-900 transition-colors">API Docs</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()

const trackingRows = [
  { progress: 82 },
  { progress: 45 },
  { progress: 64 },
  { progress: 23 },
]

const features = [
  {
    icon: '⚡',
    bg: 'bg-amber-100',
    title: 'Real-time трекинг',
    text: 'WebSocket + Redis pub/sub: координаты курьера, прогресс доставки и смена статусов прилетают мгновенно.',
  },
  {
    icon: '🛒',
    bg: 'bg-emerald-100',
    title: 'Каталог и корзина',
    text: 'Товары с категориями и изображениями, корзина с серверным пересчётом суммы и фиксацией цен при checkout.',
  },
  {
    icon: '🤖',
    bg: 'bg-brand-100',
    title: 'AI-ассистент',
    text: 'Помощник отвечает по заказам клиента, прогнозирует время доставки. Эвристики без ключа, OpenAI — при наличии.',
  },
  {
    icon: '📊',
    bg: 'bg-cyan-100',
    title: 'Аналитика',
    text: 'Сводки по статусам, выручка по доставленным заказам, заказы по дням — данные только из API.',
  },
  {
    icon: '🔔',
    bg: 'bg-violet-100',
    title: 'Уведомления',
    text: 'In-app уведомления обо всех событиях, email и Telegram через Celery-воркера при настроенных каналах.',
  },
  {
    icon: '🔐',
    bg: 'bg-rose-100',
    title: 'Безопасность',
    text: 'JWT access+refresh, bcrypt, RBAC на 4 роли, rate limiting, заявки на смену роли с апрувом админа.',
  },
]

const roles = [
  { icon: '👑', title: 'Администратор', text: 'Пользователи, роли, настройки, весь каталог' },
  { icon: '📋', title: 'Менеджер', text: 'Заказы, назначение курьеров, аналитика' },
  { icon: '🚚', title: 'Курьер', text: 'Свои заказы, смена статусов, передача геолокации' },
  { icon: '🛍️', title: 'Клиент', text: 'Каталог, корзина, оформление и отслеживание' },
]

const stack = [
  'FastAPI', 'SQLAlchemy 2.0 async', 'PostgreSQL', 'Alembic', 'Celery', 'RabbitMQ',
  'Redis', 'WebSocket', 'Nuxt 3', 'TypeScript', 'Tailwind CSS', 'Pinia', 'Docker', 'GitHub Actions',
]

useHead({ title: 'Smart Delivery AI — платформа управления доставкой' })
</script>
