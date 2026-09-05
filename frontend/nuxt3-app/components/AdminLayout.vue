<template>
  <div class="min-h-screen bg-gray-100">
    <AdminSidebar :collapsed="sidebarCollapsed" @update:collapsed="sidebarCollapsed = $event" />
    <div class="lg:ml-[280px] transition-all duration-300">
      <AdminHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const sidebarCollapsed = ref(false)
</script>