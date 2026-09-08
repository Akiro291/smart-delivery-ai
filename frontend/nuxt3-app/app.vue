<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
// Реалтайм-события доставки (WebSocket), только для авторизованных клиентов
const trackingStore = useTrackingStore()

onMounted(() => {
  if (localStorage.getItem('token')) {
    trackingStore.initWs()
  }
})
</script>
