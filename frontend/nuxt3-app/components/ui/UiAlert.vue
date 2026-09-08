<template>
  <div :class="[styles]" class="rounded-lg px-4 py-3 text-sm animate-fade-up flex items-start gap-2" role="alert">
    <span class="text-base leading-none mt-0.5">{{ icons }}</span>
    <div class="flex-1">{{ text }}</div>
    <button v-if="dismissible" @click="$emit('dismiss')" class="opacity-50 hover:opacity-100 leading-none">&times;</button>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    text: string
    tone?: 'error' | 'success' | 'info'
    dismissible?: boolean
  }>(),
  { tone: 'error', dismissible: true },
)

defineEmits(['dismiss'])

const styles = computed(() => {
  const map: Record<string, string> = {
    error: 'bg-red-50 text-red-800 border border-red-200',
    success: 'bg-emerald-50 text-emerald-800 border border-emerald-200',
    info: 'bg-brand-50 text-brand-800 border border-brand-200',
  }
  return map[props.tone]
})

const icons = computed(() => {
  const map: Record<string, string> = { error: '⚠️', success: '✅', info: 'ℹ️' }
  return map[props.tone]
})
</script>
