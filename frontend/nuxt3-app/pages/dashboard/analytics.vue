<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <h1 class="text-2xl font-bold text-gray-800">Аналитика</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500 mb-2">Выручка за месяц</h3>
            <p class="text-3xl font-bold text-green-600">1 245 000 ₽</p>
            <p class="text-sm text-green-500 mt-1">↑ +12.5% к прошлому</p>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500 mb-2">Средний чек</h3>
            <p class="text-3xl font-bold">4 520 ₽</p>
            <p class="text-sm text-green-500 mt-1">↑ +3.2% к прошлому</p>
          </div>
          <div class="bg-white p-6 rounded shadow">
            <h3 class="text-sm text-gray-500 mb-2">Конверсия</h3>
            <p class="text-3xl font-bold text-blue-600">3.8%</p>
            <p class="text-sm text-red-500 mt-1">↓ -0.5% к прошлому</p>
          </div>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-lg font-semibold mb-4">Заказы по дням</h3>
          <div class="flex items-end gap-2 h-48">
            <div v-for="(day, i) in chartData" :key="i" class="flex-1 flex flex-col items-center gap-1">
              <div :style="{ height: chartBarHeight(day.count) }"
                class="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors" />
              <span class="text-xs text-gray-500">{{ day.label }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface ChartDay {
  label: string
  count: number
}

const chartData = ref<ChartDay[]>([
  { label: 'Пн', count: 45 }, { label: 'Вт', count: 52 }, { label: 'Ср', count: 38 },
  { label: 'Чт', count: 65 }, { label: 'Пт', count: 72 }, { label: 'Сб', count: 55 },
  { label: 'Вс', count: 40 },
])

const maxCount = computed(() => Math.max(...chartData.value.map(d => d.count)))

function chartBarHeight(count: number) {
  if (maxCount.value === 0) return '0%'
  return Math.round((count / maxCount.value) * 100) + '%'
}
</script>
