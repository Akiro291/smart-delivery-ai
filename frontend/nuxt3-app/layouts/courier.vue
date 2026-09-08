<template>
  <div class="min-h-screen bg-gray-50">
    <layout-app-sidebar
      ref="sidebarRef"
      v-model:collapsed="sidebarCollapsed"
      :items="menuItems"
      title="Кабинет курьера"
      palette="green"
    />
    <div class="lg:ml-[264px] flex flex-col min-h-screen transition-all duration-300" :class="sidebarCollapsed ? 'lg:ml-[76px]' : 'lg:ml-[264px]'">
      <layout-app-header
        :title="pageTitle"
        subtitle="Рабочее место курьера"
        profile-link="/courier/profile"
        @toggle-sidebar="sidebarRef?.openMobile()"
      />
      <main class="flex-1 p-4 sm:p-6 max-w-7xl w-full mx-auto">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const sidebarCollapsed = ref(false)
const sidebarRef = ref()
const route = useRoute()

const menuItems = [
  { label: 'Обзор', to: '/courier', icon: '📊' },
  { label: 'Мои заказы', to: '/courier/orders', icon: '📦' },
  { label: 'Профиль', to: '/courier/profile', icon: '👤' },
]

const pageTitle = computed(() => {
  const current = menuItems.find((i) => i.to === route.path)
  return current?.label || 'Обзор'
})
</script>
