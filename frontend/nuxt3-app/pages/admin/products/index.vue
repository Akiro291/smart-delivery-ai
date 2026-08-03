<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Товары</h1>
      <NuxtLink to="/admin/products/create" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        + Добавить товар
      </NuxtLink>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <NuxtLink v-for="item in products" :key="item.id" :to="`/admin/products/${item.id}`" class="bg-white p-4 rounded shadow hover:shadow-lg transition-shadow cursor-pointer block">
        <div v-if="item.image_url" class="h-32 bg-gray-100 rounded mb-4 overflow-hidden">
          <img :src="getFullImageUrl(item.image_url)" :alt="item.name" class="w-full h-full object-cover" />
        </div>
        <div v-else class="h-32 bg-gray-200 rounded mb-4 flex items-center justify-center text-4xl">📦</div>
        <h3 class="font-semibold">{{ item.name }}</h3>
        <p class="text-sm text-gray-500">{{ item.category || 'Без категории' }}</p>
        <div class="flex justify-between items-center mt-3">
          <span class="font-bold">{{ formatPrice(item.price) }}</span>
          <span class="text-sm text-gray-500">В наличии: {{ item.stock_quantity }}</span>
        </div>
      </NuxtLink>
    </div>
    <div v-if="products.length === 0" class="text-center py-12 text-gray-500">Товаров пока нет. <NuxtLink to="/admin/products/create" class="text-blue-600 hover:underline">Добавить первый</NuxtLink></div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface Product {
  id: number
  name: string
  category: string | null
  description: string | null
  price: number
  stock_quantity: number
  image_url: string | null
  is_available: boolean
}

const apiBase = useRuntimeConfig().public.apiBase
const authStore = useAuthStore()
const products = ref<Product[]>([])

async function fetchProducts() {
  try {
    products.value = await $fetch(`${apiBase}/products/`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    console.log('Products loaded:', products.value.length)
  } catch (e: any) {
    console.error('Error fetching products:', e)
  }
}

function formatPrice(price: number) {
  return price.toFixed(2) + ' ₽'
}

function getFullImageUrl(imageUrl: string) {
  return `http://localhost:8000${imageUrl}`
}

onMounted(fetchProducts)
</script>
