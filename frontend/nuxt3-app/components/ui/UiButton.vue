<template>
  <button :type="type" :disabled="disabled || loading" :class="[classes]">
    <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  type?: 'button' | 'submit'
  disabled?: boolean
  loading?: boolean
  block?: boolean
}>()

const variantClasses: Record<string, string> = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  danger: 'btn-danger',
  ghost: 'btn-ghost',
}

const classes = computed(() => [
  variantClasses[props.variant || 'primary'],
  props.block ? 'w-full' : '',
])
</script>
