<template>
  <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-black/50 lg:hidden" @click="closeMobile" />

  <div :class="['fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 transform transition-transform duration-300 ease-in-out lg:hidden', mobileOpen ? 'translate-x-0' : '-translate-x-full']">
    <div class="flex items-center justify-between px-4 h-16 border-b border-slate-700">
      <span class="text-white font-bold text-lg">Smart Delivery</span>
      <button @click="closeMobile" class="text-gray-400 hover:text-white">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    <nav class="px-2 py-4 space-y-1">
      <SidebarItem v-for="item in menuItems" :key="item.label" :item="item" :active="route.path === item.to" @click="closeMobile" />
    </nav>
  </div>

  <aside :class="['fixed inset-y-0 left-0 z-30 bg-slate-900 transition-all duration-300 ease-in-out hidden lg:flex lg:flex-col', collapsed ? 'w-16' : 'w-64']">
    <div class="flex items-center justify-between px-4 h-16 border-b border-slate-700">
      <span v-if="!collapsed" class="text-white font-bold text-lg truncate">Smart Delivery</span>
      <button @click="collapse" class="text-gray-400 hover:text-white">
        <svg v-if="!collapsed" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
        </svg>
      </button>
    </div>
    <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
      <SidebarItem v-for="item in menuItems" :key="item.label" :item="item" :active="route.path === item.to" :collapsed="collapsed" />
    </nav>
  </aside>
</template>

<script setup lang="ts">
const props = defineProps<{ collapsed: boolean }>()
const emit = defineEmits(['update:collapsed'])
const route = useRoute()
const mobileOpen = ref(false)

const emitCollapse = (val: boolean) => emit('update:collapsed', val)
const collapse = () => emitCollapse(!props.collapsed)
const openMobile = () => { mobileOpen.value = true }
const closeMobile = () => { mobileOpen.value = false }

interface MenuItem {
  label: string
  to: string
  icon: string
}

const menuItems: MenuItem[] = [
  { label: 'Панель', to: '/admin', icon: '\uD83D\uDCCA' },
  { label: 'Пользователи', to: '/admin/users', icon: '\uD83D\uDC65' },
  { label: 'Роли', to: '/admin/roles', icon: '\uD83D\uDD11' },
  { label: 'Заказы', to: '/admin/orders', icon: '\uD83D\uDCCB' },
  { label: 'Товары', to: '/admin/products', icon: '\uD83D\uDED2' },
  { label: 'Курьеры', to: '/admin/couriers', icon: '\uD83D\uDE9A' },
  { label: 'Настройки', to: '/admin/settings', icon: '\u2699' },
]
</script>
