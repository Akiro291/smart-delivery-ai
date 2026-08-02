<template>
  <NuxtLink :to="item.to" :class="[
    'flex items-center gap-3 px-3 py-2 rounded transition-colors',
    active
      ? 'bg-blue-600 text-white'
      : 'text-gray-300 hover:bg-slate-800 hover:text-white'
  ]">
    <span class="text-xl flex-shrink-0">{{ item.icon }}</span>
    <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
    <span v-else class="sr-only">{{ item.label }}</span>
  </NuxtLink>
</template>

<script setup lang="ts">
interface MenuItem {
  label: string
  to: string
  icon: string
}

defineProps<{
  item: MenuItem
  active: boolean
  collapsed?: boolean
}>()
</script>
