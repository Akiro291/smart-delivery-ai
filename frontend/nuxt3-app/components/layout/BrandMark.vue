<template>
  <div class="flex items-center" :class="compact ? 'justify-center' : 'gap-2.5 px-1'">
    <div :class="compact ? 'h-9 w-9' : 'h-9 w-9'" class="rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center flex-shrink-0">
      <svg :class="compact ? 'h-4 w-4' : 'h-5 w-5'" class="text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    </div>
    <div v-if="!compact" class="leading-tight">
      <p class="text-white font-bold text-sm tracking-tight">Smart Delivery</p>
      <p class="text-white/40 text-[10px] uppercase tracking-wider">{{ subtitle }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ subtitle?: string; light?: boolean; compact?: boolean }>(), {
  subtitle: 'Панель управления',
})
</script>
