<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <h1 class="text-2xl font-bold text-gray-800">AI помощник</h1>
        <div class="bg-white rounded shadow p-6">
          <div ref="chatRef" class="space-y-4 h-96 overflow-y-auto mb-4">
            <div v-for="(msg, i) in messages" :key="i" class="flex" :class="msgUserRoleClass(msg)">
              <div :class="msgBoxClass(msg)" class="max-w-md px-4 py-3 rounded-lg">
                {{ msg.text }}
              </div>
            </div>
          </div>
          <div class="flex gap-2">
            <input v-model="input" @keyup.enter="sendMessage" placeholder="Спросите AI..."
              class="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
            <button @click="sendMessage" :disabled="!input.trim()"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
              Отправить
            </button>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const input = ref('')
const chatRef = ref<HTMLElement | null>(null)

interface Message {
  role: string
  text: string
}

const messages = ref<Message[]>([
  { role: 'ai', text: 'Привет! Я AI помощник Smart Delivery. Чем могу помочь?' },
])

function msgUserRoleClass(msg: Message) {
  return msg.role === 'user' ? 'justify-end' : 'justify-start'
}

function msgBoxClass(msg: Message) {
  if (msg.role === 'user') {
    return 'bg-blue-600 text-white'
  }
  return 'bg-gray-100 text-gray-800'
}

async function sendMessage() {
  if (!input.value.trim()) return
  messages.value.push({ role: 'user', text: input.value })
  const userMsg = input.value
  input.value = ''

  try {
    const response = await $fetch('/api/v1/ai/chat', {
      method: 'POST',
      body: { message: userMsg },
    })
    messages.value.push({ role: 'ai', text: response.reply })
  } catch {
    messages.value.push({ role: 'ai', text: 'Ошибка подключения к AI' })
  }

  nextTick(() => {
    if (chatRef.value) {
      chatRef.value.scrollTop = chatRef.value.scrollHeight
    }
  })
}
</script>
