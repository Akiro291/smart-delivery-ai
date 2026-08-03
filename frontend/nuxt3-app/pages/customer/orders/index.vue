<template>
  <CustomerLayout>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Мои заказы</h1>
      <div class="space-y-4">
        <div class="bg-white p-6 rounded shadow">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold">Заказ #1001</h3>
            <span class="px-3 py-1 rounded text-xs bg-blue-100 text-blue-800">В пути</span>
          </div>
          <p class="text-sm text-gray-500">Стандартная доставка &#x2022; 299 ₽</p>
          <p class="text-sm text-gray-500 mt-2">Ожидается: завтра</p>
        </div>
        <div class="bg-white p-6 rounded shadow">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-semibold">Заказ #998</h3>
            <span class="px-3 py-1 rounded text-xs bg-green-100 text-green-800">Доставлен</span>
          </div>
          <p class="text-sm text-gray-500">Экспресс доставка &#x2022; 599 ₽</p>
          <p class="text-sm text-gray-500 mt-2">Доставлен: 01.08.2026</p>
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script setup lang="ts">
</script>
