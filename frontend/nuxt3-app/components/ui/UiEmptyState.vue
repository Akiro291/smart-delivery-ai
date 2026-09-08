<template>
  <div class="flex flex-col items-center justify-center py-14 text-center animate-fade-in">
    <div class="w-16 h-16 rounded-2xl bg-gray-100 flex items-center justify-center text-3xl mb-4">
      {{ icon }}
    </div>
    <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
    <p v-if="description" class="text-sm text-gray-500 mt-1 max-w-sm">{{ description }}</p>
    <div v-if="$slots.default" class="mt-5">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    icon?: string
    title: string
    description?: string
  }>(),
  { icon: '📭' },
)
</script>
