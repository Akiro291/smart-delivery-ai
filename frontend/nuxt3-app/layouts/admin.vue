<template>
  <div class="min-h-screen bg-gray-50">
    <layout-app-sidebar
      ref="sidebarRef"
      v-model:collapsed="sidebarCollapsed"
      :items="menuItems"
      title="Админ-панель"
      palette="slate"
    />
    <div class="lg:ml-[264px] flex flex-col min-h-screen transition-all duration-300" :class="sidebarCollapsed ? 'lg:ml-[76px]' : 'lg:ml-[264px]'">
      <layout-app-header
        :title="pageTitle"
        subtitle="Управление платформой"
        profile-link="/profile"
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
  { label: 'Панель', to: '/admin', icon: '📊' },
  { label: 'Пользователи', to: '/admin/users', icon: '👥' },
  { label: 'Роли', to: '/admin/roles', icon: '🔑' },
  { label: 'Заказы', to: '/admin/orders', icon: '📋' },
  { label: 'Товары', to: '/admin/products', icon: '🛒' },
  { label: 'Курьеры', to: '/admin/couriers', icon: '🚚' },
  { label: 'Настройки', to: '/admin/settings', icon: '⚙️' },
]

const pageTitle = computed(() => {
  const current = menuItems.find((i) => i.to === route.path)
  return current?.label || 'Панель'
})
</script>
