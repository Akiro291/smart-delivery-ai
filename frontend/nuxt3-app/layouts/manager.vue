<template>
  <div class="min-h-screen bg-gray-100">
    <Sidebar v-model:collapsed="sidebarCollapsed" />
    <div class="lg:ml-[280px] flex-1 flex flex-col min-w-0">
      <Header @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const sidebarCollapsed = ref(false)
</script>
