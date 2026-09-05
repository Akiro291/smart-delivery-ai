<template>
  <div>
    <button @click="$emit('toggle-sidebar')" class="lg:hidden p-2 rounded hover:bg-gray-100">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    <span class="hidden lg:block text-xl font-semibold text-gray-800"><slot /></span>
    <div class="flex items-center gap-4 ml-auto">
      <button class="relative p-2 rounded hover:bg-gray-100">
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
      </button>
      <div class="relative group">
        <button class="flex items-center gap-2 p-2 rounded hover:bg-gray-100">
          <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
            {{ initial }}
          </div>
          <span class="hidden md:block text-sm text-gray-700">{{ userName }}</span>
        </button>
        <div class="hidden group-hover:block absolute right-0 mt-2 w-48 bg-white rounded shadow-lg border z-50">
          <NuxtLink to="/profile" class="block px-4 py-2 hover:bg-gray-50">Профиль</NuxtLink>
          <button @click="logout" class="w-full text-left px-4 py-2 hover:bg-gray-50 text-red-600">Выйти</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits(['toggle-sidebar'])

const user = ref({ full_name: null as string | null, email: '' })

onMounted(async () => {
  try {
    const data = await useApi().get('/auth/me')
    user.value = data
  } catch {
    logout()
  }
})

const userName = computed(() => user.value.full_name || user.value.email || 'User')
const initial = computed(() => (user.value.full_name || 'U')[0]?.toUpperCase() || 'U')

function logout() {
  localStorage.removeItem('token')
  navigateTo('/auth/login')
}
</script>
