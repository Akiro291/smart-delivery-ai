<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">AI помощник</h1>
    <div class="bg-white rounded shadow p-6">
      <div ref="chatRef" class="space-y-4 h-96 overflow-y-auto mb-4">
        <div v-for="(msg, i) in messages" :key="i" class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <div :class="msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'" class="max-w-md px-4 py-3 rounded-lg">
            {{ msg.text }}
          </div>
        </div>
        <div v-if="isSending" class="flex justify-start">
          <div class="bg-gray-100 text-gray-500 max-w-md px-4 py-3 rounded-lg">Печатает...</div>
        </div>
      </div>
      <div class="flex gap-2">
        <input
          v-model="input"
          @keyup.enter="sendMessage"
          placeholder="Спросите о ваших заказах..."
          class="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="sendMessage"
          :disabled="!input.trim() || isSending"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Отправить
        </button>
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

const messages = ref<Message[]>([
  { role: 'ai', text: 'Привет! Я AI помощник Smart Delivery. Могу рассказать о статусе ваших заказов.' },
])

async function sendMessage() {
  if (!input.value.trim() || isSending.value) return
  messages.value.push({ role: 'user', text: input.value })
  const userMsg = input.value
  input.value = ''
  isSending.value = true

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
  }

  nextTick(() => {
    if (chatRef.value) {
      chatRef.value.scrollTop = chatRef.value.scrollHeight
    }
  })
}
</script>
