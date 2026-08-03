<template>
  <CustomerLayout>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Мой профиль</h1>
      <div class="bg-white p-6 rounded shadow max-w-lg">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <p class="mt-1 text-gray-900">user@example.com</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Имя</label>
            <p class="mt-1 text-gray-900">Иван Петров</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Телефон</label>
            <p class="mt-1 text-gray-900">+7 999 123-45-67</p>
          </div>
          <button class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
            Редактировать
          </button>
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script setup lang="ts">
</script>
