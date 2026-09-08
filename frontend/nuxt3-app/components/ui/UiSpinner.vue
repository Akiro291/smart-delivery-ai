<template>
  <div class="flex flex-col items-center justify-center py-14 animate-fade-in" aria-live="polite">
    <svg class="animate-spin h-8 w-8 text-brand-600" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
    <p v-if="label" class="text-sm text-gray-500 mt-3">{{ label }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ label?: string }>(), { label: '' })
</script>
