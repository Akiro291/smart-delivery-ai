<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">Курьеры</h1>
          <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Добавить</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="courier in couriers" :key="courier.id" class="bg-white p-6 rounded shadow">
            <div class="flex items-center gap-4">
              <div :class="courierBadgeClass(courier)" class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold">
                {{ courier.initials }}
              </div>
              <div>
                <h3 class="font-semibold">{{ courier.name }}</h3>
                <p :class="courierOnlineTextClass(courier)">
                  {{ courierText(courier) }}
                </p>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t flex justify-between text-sm">
              <span class="text-gray-500">Доставок: {{ courier.deliveries }}</span>
              <span class="text-gray-500">Рейтинг: {{ courier.rating }} ⭐</span>
            </div>
          </div>
        </div>
        <div v-if="couriers.length === 0" class="text-center py-12 text-gray-500">Курьеров пока нет</div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface Courier {
  id: number
  name: string
  initials: string
  online: boolean
  deliveries: number
  rating: number
}

const couriers = ref<Courier[]>([
  { id: 1, name: 'Алексей Козлов', initials: 'АК', online: true, deliveries: 156, rating: 4.8 },
  { id: 2, name: 'Дмитрий Волков', initials: 'ДВ', online: true, deliveries: 132, rating: 4.9 },
  { id: 3, name: 'Сергей Новиков', initials: 'СН', online: false, deliveries: 89, rating: 4.5 },
])

function courierBadgeClass(c: Courier) {
  if (c.online) return 'bg-green-100 text-green-600'
  return 'bg-gray-100 text-gray-600'
}

function courierOnlineTextClass(c: Courier) {
  if (c.online) return 'text-green-600'
  return 'text-gray-500'
}

function courierText(c: Courier) {
  if (c.online) return 'Онлайн'
  return 'Оффлайн'
}
</script>
