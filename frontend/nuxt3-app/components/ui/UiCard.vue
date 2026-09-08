<template>
  <div :class="['card', hover ? 'card-hover' : '', padding ? '' : 'p-6']">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hover?: boolean
  padding?: boolean
}>()
</script>
