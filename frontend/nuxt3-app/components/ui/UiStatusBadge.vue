<template>
  <span :class="badge" class="badge">
    <span v-if="dot" class="h-1.5 w-1.5 rounded-full bg-current opacity-70" />
    {{ label }}
  </span>
</template>

<script setup lang="ts">
import { ORDER_STATUS_META } from '~/composables/useOrderStatus'

const props = withDefaults(
  defineProps<{
    status: string
    dot?: boolean
  }>(),
  { dot: true },
)

const meta = computed(() => ORDER_STATUS_META[props.status] || { label: props.status, class: 'bg-gray-100 text-gray-700' })
const label = computed(() => meta.value.label)
const badge = computed(() => meta.value.class)
</script>
