<template>
  <div>
    <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-gray-900/60 backdrop-blur-sm lg:hidden" @click="closeMobile" />

    <!-- Мобильный сайдбар -->
    <transition name="slide">
      <div
        v-if="mobileOpen"
        :class="palette.sidebar"
        class="fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out lg:hidden flex flex-col"
      >
        <div class="flex items-center justify-between px-5 h-16 border-b border-white/10">
          <BrandMark :subtitle="title" light />
          <button @click="closeMobile" class="text-white/50 hover:text-white transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <NuxtLink
            v-for="item in items"
            :key="item.to"
            :to="item.to"
            :class="linkClasses(route.path === item.to)"
            class="flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors"
            @click="closeMobile"
          >
            <span class="text-lg w-6 text-center">{{ item.icon }}</span>
            {{ item.label }}
          </NuxtLink>
        </nav>
      </div>
    </transition>

    <!-- Десктопный сайдбар -->
    <aside
      :class="palette.sidebar"
      class="fixed inset-y-0 left-0 z-30 transition-all duration-300 ease-in-out hidden lg:flex lg:flex-col"
      :style="{ width: collapsed ? '76px' : '264px' }"
    >
      <div class="flex items-center justify-between px-4 h-16 border-b border-white/10 flex-shrink-0">
        <BrandMark :subtitle="title" light :compact="collapsed" />
        <button v-if="!collapsed" @click="$emit('update:collapsed', true)" class="text-white/40 hover:text-white transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
      </div>
      <button
        v-if="collapsed"
        @click="$emit('update:collapsed', false)"
        class="absolute -right-9 top-5 h-8 w-8 rounded-lg bg-white shadow-card border border-gray-200 text-gray-500 hover:text-gray-800 flex items-center justify-center"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
        </svg>
      </button>

      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <NuxtLink
          v-for="item in items"
          :key="item.to"
          :to="item.to"
          :class="linkClasses(route.path === item.to)"
          class="flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :title="collapsed ? item.label : undefined"
        >
          <span class="text-lg w-6 text-center flex-shrink-0">{{ item.icon }}</span>
          <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
          <span v-else class="sr-only">{{ item.label }}</span>
        </NuxtLink>
      </nav>

      <div class="px-3 pb-4 flex-shrink-0">
        <div v-if="!collapsed" :class="palette.footer" class="rounded-lg px-4 py-3 text-xs">
          <p class="font-semibold">{{ userName }}</p>
          <p class="opacity-60 mt-0.5">{{ roleLabel }}</p>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
export interface MenuItem {
  label: string
  to: string
  icon: string
}

const props = defineProps<{
  items: MenuItem[]
  title: string
  palette?: 'slate' | 'purple' | 'green'
  collapsed: boolean
}>()

defineEmits(['update:collapsed'])

const route = useRoute()
const mobileOpen = ref(false)
const authStore = useAuthStore()

const userName = computed(() => authStore.userName || '—')
const roleLabel = computed(() => {
  const map: Record<string, string> = {
    ADMIN: 'Администратор',
    MANAGER: 'Менеджер',
    COURIER: 'Курьер',
    CUSTOMER: 'Клиент',
  }
  return map[authStore.userRole || ''] || ''
})

const palettes: Record<string, { sidebar: string; footer: string }> = {
  slate: {
    sidebar: 'bg-gradient-to-b from-slate-900 to-slate-950 text-slate-300',
    footer: 'bg-white/5 text-white',
  },
  purple: {
    sidebar: 'bg-gradient-to-b from-purple-900 to-purple-950 text-purple-200',
    footer: 'bg-white/10 text-white',
  },
  green: {
    sidebar: 'bg-gradient-to-b from-emerald-900 to-emerald-950 text-emerald-200',
    footer: 'bg-white/10 text-white',
  },
}

const palette = computed(() => palettes[props.palette || 'slate'])

function linkClasses(active: boolean) {
  return active
    ? 'bg-white text-gray-900 shadow-card'
    : `${palette.value.sidebar.includes('purple') ? 'hover:bg-white/10 hover:text-white' : palette.value.sidebar.includes('emerald') ? 'hover:bg-white/10 hover:text-white' : 'hover:bg-white/5 hover:text-white'}`
}

function closeMobile() {
  mobileOpen.value = false
}

defineExpose({ openMobile: () => (mobileOpen.value = true) })
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
