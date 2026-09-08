<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-800">Товары</h1>
      <div class="flex gap-2">
        <button @click="load" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">Обновить</button>
        <NuxtLink to="/dashboard/products/create" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          + Добавить
        </NuxtLink>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="item in products" :key="item.id" class="bg-white p-4 rounded shadow">
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">{{ item.name }}</h3>
          <span
            :class="item.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
            class="px-2 py-1 rounded-full text-xs"
          >
            {{ item.is_available ? 'Доступен' : 'Скрыт' }}
          </span>
        </div>
        <p class="text-sm text-gray-500 mt-1">{{ item.category || 'Без категории' }}</p>
        <p class="text-sm text-gray-600 mt-2 min-h-[40px]">{{ item.description || 'Без описания' }}</p>
        <div class="flex justify-between items-center mt-3">
          <span class="font-bold">{{ formatPrice(item.price) }}</span>
          <span class="text-sm text-gray-500">На складе: {{ item.stock_quantity ?? '∞' }}</span>
        </div>
      </div>
    </div>
    <div v-if="!isLoading && products.length === 0" class="text-center py-12 text-gray-500">Товаров пока нет</div>
    <div v-if="isLoading" class="text-center py-12 text-gray-500">Загрузка...</div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

interface Product {
  id: number
  name: string
  description: string | null
  price: number
  category: string | null
  is_available: boolean
  stock_quantity: number | null
}

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const products = ref<Product[]>([])
const isLoading = ref(true)

onMounted(load)

async function load() {
  isLoading.value = true
  try {
    products.value = (await $fetch(`${apiBase}/products/?limit=100`)) as Product[]
  } catch {
    products.value = []
  } finally {
    isLoading.value = false
  }
}

function formatPrice(price: number) {
  return Number(price).toLocaleString('ru-RU', { maximumFractionDigits: 2 }) + ' ₽'
}
</script>
