<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h1 class="text-5xl font-bold mb-4">Smart Delivery AI</h1>
      <p class="text-xl text-gray-600 mb-8">AI-powered delivery management platform</p>
      <div class="space-x-4">
        <NuxtLink to="/auth/login"
          class="inline-block px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700">Войти</NuxtLink>
        <NuxtLink to="/auth/register"
          class="inline-block px-6 py-3 bg-gray-600 text-white rounded hover:bg-gray-700">Регистрация</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>
