<template>
  <div class="min-h-screen bg-gray-50">
    <CustomerSidebar :collapsed="sidebarCollapsed" @update:collapsed="sidebarCollapsed = $event" />
    <div :class="[sidebarCollapsed ? 'lg:ml-[280px]' : 'lg:ml-[280px]']" class="transition-all duration-300">
      <CustomerHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'] })

const sidebarCollapsed = ref(false)
</script>
