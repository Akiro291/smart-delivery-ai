<template>
  <header class="sticky top-0 z-20 bg-white border-b border-gray-200 h-16 flex items-center px-4 gap-4">
    <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 rounded hover:bg-gray-100">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    <h1 class="text-xl font-semibold text-gray-800">Кабинет курьера</h1>
    <div class="flex items-center gap-4 ml-auto">
      <div class="relative group">
        <button class="flex items-center gap-2 p-2 rounded hover:bg-gray-100">
          <div class="w-8 h-8 bg-green-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
            {{ initial }}
          </div>
          <span class="hidden md:block text-sm text-gray-700">{{ userName }}</span>
        </button>
        <div class="hidden group-hover:block absolute right-0 mt-2 w-48 bg-white rounded shadow-lg border z-50">
          <NuxtLink to="/courier/profile" class="block px-4 py-2 hover:bg-gray-50">Профиль</NuxtLink>
          <button @click="logout" class="w-full text-left px-4 py-2 hover:bg-gray-50 text-red-600">Выйти</button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
defineEmits(['toggle-sidebar'])

const userName = localStorage.getItem('user_name') || 'Курьер'
const initial = computed(() => (userName || 'K')[0]?.toUpperCase() || 'K')

async function logout() {
  const authStore = useAuthStore()
  await authStore.logout()
  navigateTo('/auth/login')
}
</script>
