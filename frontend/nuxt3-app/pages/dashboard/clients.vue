<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">Клиенты</h1>
          <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Добавить</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="client in clients" :key="client.id" class="bg-white p-6 rounded shadow">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-lg">
                {{ client.initials }}
              </div>
              <div>
                <h3 class="font-semibold">{{ client.name }}</h3>
                <p class="text-sm text-gray-500">{{ client.email }}</p>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t flex justify-between text-sm">
              <span class="text-gray-500">Заказов: {{ client.orders }}</span>
              <span class="text-gray-500">Последний: {{ client.lastOrder }}</span>
            </div>
          </div>
        </div>
        <div v-if="clients.length === 0" class="text-center py-12 text-gray-500">Клиентов пока нет</div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface Client {
  id: number
  name: string
  email: string
  initials: string
  orders: number
  lastOrder: string
}

const clients = ref<Client[]>([
  { id: 1, name: 'Иван Петров', email: 'ivan@mail.ru', initials: 'ИП', orders: 12, lastOrder: '01.08.2026' },
  { id: 2, name: 'Мария Сидорова', email: 'maria@gmail.com', initials: 'МС', orders: 8, lastOrder: '30.07.2026' },
  { id: 3, name: 'Олег Иванов', email: 'oleg@yandex.ru', initials: 'ОИ', orders: 5, lastOrder: '28.07.2026' },
])
</script>
