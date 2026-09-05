<template>
  <div class="auth-layout">
    <div class="auth-container">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// Auth layout - provides consistent styling for auth pages
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background-muted, #f5f5f5);
  padding: 1rem;
}

.auth-container {
  width: 100%;
  max-width: 480px;
  background-color: var(--color-background, #ffffff);
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 2rem;
}

@media (max-width: 640px) {
  .auth-container {
    padding: 1rem;
  }
}
</style>
