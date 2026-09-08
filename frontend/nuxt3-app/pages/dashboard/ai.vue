<template>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Чат -->
    <div class="lg:col-span-2">
      <div class="card flex flex-col h-[70vh]">
        <div class="flex items-center gap-3 px-6 py-4 border-b border-gray-100">
          <div class="h-10 w-10 rounded-xl bg-gradient-to-br from-brand-500 to-violet-600 flex items-center justify-center text-xl">
            🤖
          </div>
          <div>
            <h3 class="font-semibold text-gray-800 leading-tight">AI-ассистент</h3>
            <p class="text-xs text-gray-400 flex items-center gap-1.5">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-500" /> онлайн
            </p>
          </div>
        </div>
        <div ref="chatRef" class="flex-1 overflow-y-auto p-6 space-y-4">
          <div v-for="(msg, i) in messages" :key="i" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
            <div
              :class="msg.role === 'user'
                ? 'bg-brand-600 text-white rounded-br-sm'
                : 'bg-gray-100 text-gray-800 rounded-bl-sm'"
              class="max-w-md px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-card"
            >
              {{ msg.text }}
            </div>
          </div>
          <div v-if="isSending" class="flex justify-start">
            <div class="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1.5">
              <span v-for="i in 3" :key="i" class="h-2 w-2 rounded-full bg-gray-400 animate-bounce" :style="{ animationDelay: i * 0.15 + 's' }" />
            </div>
          </div>
        </div>
        <div class="p-4 border-t border-gray-100">
          <div class="flex gap-2">
            <input
              v-model="input"
              @keyup.enter="sendMessage"
              placeholder="Спросите о ваших заказах…"
              class="input flex-1"
            />
            <UiButton :loading="isSending" :disabled="!input.trim()" @click="sendMessage">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 19V5m0 0l-7 7m7-7l7 7" />
              </svg>
            </UiButton>
          </div>
        </div>
      </div>
    </div>

    <!-- Подсказки -->
    <div class="space-y-6">
      <div class="card p-6">
        <h3 class="font-semibold text-gray-800 mb-4">Попробуйте спросить</h3>
        <div class="space-y-2">
          <button
            v-for="suggestion in suggestions"
            :key="suggestion"
            @click="askSuggestion(suggestion)"
            class="w-full text-left text-sm px-4 py-3 rounded-lg border border-gray-100 hover:border-brand-200 hover:bg-brand-50/50 text-gray-600 transition-all"
          >
            «{{ suggestion }}»
          </button>
        </div>
      </div>
      <div class="card p-6">
        <h3 class="font-semibold text-gray-800 mb-2">Прогноз доставки</h3>
        <p class="text-sm text-gray-500">AI-прогноз времени доставки по заказу доступен менеджерам и администраторам.</p>
        <NuxtLink to="/dashboard/orders" class="btn-secondary w-full mt-4">К заказам</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth', layout: 'manager' })

interface Message {
  role: string
  text: string
}

const authStore = useAuthStore()
const input = ref('')
const chatRef = ref<HTMLElement | null>(null)
const isSending = ref(false)

const suggestions = ['Где мой заказ?', 'Привет', 'Статус доставки']

const messages = ref<Message[]>([
  {
    role: 'ai',
    text: 'Привет! Я AI-помощник Smart Delivery. Могу рассказать о статусе ваших заказов и прогнозе доставки.',
  },
])

async function sendMessage() {
  if (!input.value.trim() || isSending.value) return
  messages.value.push({ role: 'user', text: input.value })
  const userMsg = input.value
  input.value = ''
  isSending.value = true
  scrollDown()

  try {
    const apiBase = useRuntimeConfig().public.apiBase
    const response = await $fetch(`${apiBase}/ai/chat`, {
      method: 'POST',
      body: { message: userMsg },
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    messages.value.push({ role: 'ai', text: response.reply })
  } catch {
    messages.value.push({ role: 'ai', text: 'Ошибка подключения к AI. Попробуйте ещё раз.' })
  } finally {
    isSending.value = false
    scrollDown()
  }
}

function askSuggestion(text: string) {
  input.value = text
  sendMessage()
}

function scrollDown() {
  nextTick(() => {
    if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight
  })
}
</script>
