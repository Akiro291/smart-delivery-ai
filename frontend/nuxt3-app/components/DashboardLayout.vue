<template>
  <div class="min-h-screen bg-gray-100 flex">
    <Sidebar v-model:collapsed="sidebarCollapsed" />
    <div class="flex-1 flex flex-col min-w-0">
      <Header @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue'
import Header from '@/components/Header.vue'

const sidebarCollapsed = ref(false)
</script>
