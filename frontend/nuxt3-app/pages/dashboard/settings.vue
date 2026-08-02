<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <h1 class="text-2xl font-bold text-gray-800">Настройки</h1>
        <div class="bg-white rounded shadow p-6 max-w-lg">
          <h3 class="text-lg font-semibold mb-4">Основные</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium">Название компании</label>
              <input type="text" placeholder="Smart Delivery"
                class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium">Email</label>
              <input type="email" placeholder="admin@smartdelivery.ai"
                class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium">Часовой пояс</label>
              <select class="mt-1 block w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option>UTC+3 (Москва)</option>
                <option>UTC+5 (Екатеринбург)</option>
                <option>UTC+7 (Новосибирск)</option>
                <option>UTC+10 (Владивосток)</option>
              </select>
            </div>
            <button class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Сохранить</button>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
</script>
