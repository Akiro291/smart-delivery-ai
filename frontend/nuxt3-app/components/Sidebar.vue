<template>
  <!-- Mobile overlay -->
  <div
    v-if="mobileOpen && !mobileCollapsed"
    class="fixed inset-0 z-40 bg-black/50 lg:hidden"
    @click="closeMobile"
  />

  <!-- Mobile sidebar -->
  <div
    :class="[
      'fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 transform transition-transform duration-300 ease-in-out lg:hidden',
      mobileOpen ? 'translate-x-0' : '-translate-x-full'
    ]"
  >
    <div class="flex items-center justify-between px-4 h-16 border-b border-slate-700">
      <span class="text-white font-bold text-lg">Smart Delivery</span>
      <button @click="closeMobile" class="text-gray-400 hover:text-white">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <nav class="px-2 py-4 space-y-1">
      <SidebarItem v-for="item in menuItems" :key="item.label" :item="item" :active="route.path === item.to"
        @click="closeMobile" />
    </nav>
  </div>

  <!-- Desktop sidebar -->
  <aside :class="[
    'fixed inset-y-0 left-0 z-30 bg-slate-900 transition-all duration-300 ease-in-out hidden lg:flex lg:flex-col',
    collapsed ? 'w-16' : 'w-64'
  ]">
    <div class="flex items-center justify-between px-4 h-16 border-b border-slate-700">
      <span v-if="!collapsed" class="text-white font-bold text-lg truncate">Smart Delivery</span>
      <button v-if="!collapsed" @click="collapse" class="text-gray-400 hover:text-white">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
      </button>
      <button v-else @click="collapse" class="text-gray-400 hover:text-white">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
    <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
      <SidebarItem v-for="item in menuItems" :key="item.label" :item="item" :active="route.path === item.to"
        :collapsed="collapsed" />
    </nav>
  </aside>
</template>

<script setup lang="ts">
defineProps<{ collapsed: boolean }>()
const emit = defineEmits(['update:collapsed'])
const route = useRoute()
const mobileOpen = ref(false)
const mobileCollapsed = ref(false)

const emitCollapse = (val: boolean) => emit('update:collapsed', val)

const collapse = () => emitCollapse(!collapsed.value)
const openMobile = () => { mobileOpen.value = true; mobileCollapsed.value = false }
const closeMobile = () => { mobileOpen.value = false }

interface MenuItem {
  label: string
  to: string
  icon: string
}

const menuItems: MenuItem[] = [
  { label: 'Dashboard', to: '/dashboard', icon: '📦' },
  { label: 'Товары', to: '/dashboard/products', icon: '🛒' },
  { label: 'Заказы', to: '/dashboard/orders', icon: '📋' },
  { label: 'Клиенты', to: '/dashboard/clients', icon: '👥' },
  { label: 'Курьеры', to: '/dashboard/couriers', icon: '🚚' },
  { label: 'Аналитика', to: '/dashboard/analytics', icon: '📊' },
  { label: 'AI помощник', to: '/dashboard/ai', icon: '🤖' },
  { label: 'Настройки', to: '/dashboard/settings', icon: '⚙' },
]
</script>
