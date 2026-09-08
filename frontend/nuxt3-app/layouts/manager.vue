<template>
  <div class="min-h-screen bg-gray-50">
    <layout-app-sidebar
      ref="sidebarRef"
      v-model:collapsed="sidebarCollapsed"
      :items="menuItems"
      title="Дашборд"
      palette="purple"
    />
    <div class="lg:ml-[264px] flex flex-col min-h-screen transition-all duration-300" :class="sidebarCollapsed ? 'lg:ml-[76px]' : 'lg:ml-[264px]'">
      <layout-app-header
        :title="pageTitle"
        subtitle="Операционная панель"
        profile-link="/dashboard/settings"
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
  { label: 'Обзор', to: '/dashboard', icon: '📊' },
  { label: 'Заказы', to: '/dashboard/orders', icon: '📋' },
  { label: 'Товары', to: '/dashboard/products', icon: '🛒' },
  { label: 'Клиенты', to: '/dashboard/clients', icon: '👥' },
  { label: 'Курьеры', to: '/dashboard/couriers', icon: '🚚' },
  { label: 'Аналитика', to: '/dashboard/analytics', icon: '📈' },
  { label: 'AI', to: '/dashboard/ai', icon: '🤖' },
  { label: 'Профиль', to: '/dashboard/settings', icon: '⚙️' },
]

const pageTitle = computed(() => {
  const current = menuItems.find((i) => i.to === route.path)
  return current?.label || 'Обзор'
})
</script>
