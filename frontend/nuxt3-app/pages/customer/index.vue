<template>
  <CustomerLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Каталог услуг</h1>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x1F4E6;</div>
          <h3 class="text-lg font-semibold mb-2">Стандартная доставка</h3>
          <p class="text-gray-500 text-sm">Доставка в течение 1-3 дней</p>
          <p class="text-xl font-bold mt-4 text-purple-600">от 299 ₽</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x26A1;</div>
          <h3 class="text-lg font-semibold mb-2">Экспресс доставка</h3>
          <p class="text-gray-500 text-sm">Доставка в течение 2-4 часов</p>
          <p class="text-xl font-bold mt-4 text-purple-600">от 599 ₽</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x1F3E2;</div>
          <h3 class="text-lg font-semibold mb-2">Корпоративная доставка</h3>
          <p class="text-gray-500 text-sm">Для бизнеса с особыми условиями</p>
          <p class="text-xl font-bold mt-4 text-purple-600">по запросу</p>
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })
</script>
