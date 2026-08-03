<template>
  <AdminLayout>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Управление заказами</h1>
      <div class="bg-white p-6 rounded shadow">
        <p class="text-gray-500">Здесь будет список всех заказов</p>
      </div>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
</script>
