<template>
  <div :class="gradient" class="rounded-xl p-5 text-white shadow-card relative overflow-hidden">
    <div class="absolute -right-3 -top-3 text-6xl opacity-10 select-none">{{ icon }}</div>
    <p class="text-sm font-medium text-white/70">{{ label }}</p>
    <p class="text-3xl font-bold mt-1 tracking-tight">{{ value }}</p>
    <p v-if="hint" class="text-xs text-white/60 mt-1">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    label: string
    value: string | number
    icon: string
    hint?: string
    tone?: 'indigo' | 'emerald' | 'amber' | 'cyan' | 'red' | 'violet'
  }>(),
  { tone: 'indigo' },
)

const gradients: Record<string, string> = {
  indigo: 'bg-gradient-to-br from-brand-600 to-brand-800',
  emerald: 'bg-gradient-to-br from-emerald-500 to-emerald-700',
  amber: 'bg-gradient-to-br from-amber-500 to-orange-600',
  cyan: 'bg-gradient-to-br from-cyan-500 to-sky-700',
  red: 'bg-gradient-to-br from-rose-500 to-red-700',
  violet: 'bg-gradient-to-br from-violet-500 to-purple-700',
}

const gradient = computed(() => gradients[props.tone])
</script>
