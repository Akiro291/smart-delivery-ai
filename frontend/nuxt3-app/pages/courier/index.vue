<template>
  <CourierLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Мои заказы</h1>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">Активных</h3>
          <p class="text-3xl font-bold mt-2 text-blue-600">3</p>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">Выполнено сегодня</h3>
          <p class="text-3xl font-bold mt-2 text-green-600">5</p>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <h3 class="text-sm text-gray-500">В ожидании</h3>
          <p class="text-3xl font-bold mt-2 text-yellow-600">1</p>
        </div>
      </div>
      <div class="bg-white p-6 rounded shadow">
        <h3 class="text-lg font-semibold mb-4">Текущие заказы</h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between p-4 border rounded">
            <div>
              <p class="font-medium">Заказ #1001</p>
              <p class="text-sm text-gray-500">ул. Ленина, 10 → ул. Мира, 5</p>
            </div>
            <span class="px-3 py-1 rounded text-xs bg-blue-100 text-blue-800">В пути</span>
          </div>
          <div class="flex items-center justify-between p-4 border rounded">
            <div>
              <p class="font-medium">Заказ #1002</p>
              <p class="text-sm text-gray-500">ул. Пушкина, 3 → ул. Колхозная, 12</p>
            </div>
            <span class="px-3 py-1 rounded text-xs bg-yellow-100 text-yellow-800">Ожидает</span>
          </div>
        </div>
      </div>
    </div>
  </CourierLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'courier'], layout: 'courier' })
</script>
