<template>
  <div class="space-y-6">
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/products" class="text-blue-600 hover:underline">&larr; Назад к товарам</NuxtLink>
      <h1 class="text-2xl font-bold text-gray-800">Товар</h1>
    </div>
    <div v-if="product" class="bg-white rounded shadow p-6 max-w-2xl">
      <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
      <p class="text-gray-500 mb-4">{{ product.category || 'Без категории' }}</p>
      <p class="text-gray-700 mb-6">{{ product.description || 'Без описания' }}</p>
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-gray-50 p-4 rounded">
          <p class="text-sm text-gray-500">Цена</p>
          <p class="text-xl font-bold">{{ formatPrice(product.price) }}</p>
        </div>
        <div class="bg-gray-50 p-4 rounded">
          <p class="text-sm text-gray-500">На складе</p>
          <p class="text-xl font-bold">{{ product.stock_quantity ?? '∞' }} шт</p>
        </div>
      </div>
      <div class="flex gap-2 mt-6">
        <button
          @click="toggleAvailability"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {{ product.is_available ? 'Скрыть из каталога' : 'Вернуть в каталог' }}
        </button>
      </div>
    </div>
    <div v-else-if="isLoading" class="text-center py-12 text-gray-500">Загрузка...</div>
    <div v-else class="text-center py-12 text-gray-500">Товар не найден</div>
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

const route = useRoute()
const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const productId = Number(route.params.id)
const product = ref<Product | null>(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    product.value = (await $fetch(`${apiBase}/products/${productId}`)) as Product
  } catch {
    product.value = null
  } finally {
    isLoading.value = false
  }
})

async function toggleAvailability() {
  if (!product.value) return
  try {
    product.value = (await $fetch(`${apiBase}/products/${productId}`, {
      method: 'PUT',
      body: { is_available: !product.value.is_available },
      headers: { Authorization: `Bearer ${authStore.token}`, 'Content-Type': 'application/json' },
    })) as Product
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка обновления товара')
  }
}

function formatPrice(price: number) {
  return Number(price).toLocaleString('ru-RU', { maximumFractionDigits: 2 }) + ' ₽'
}
</script>
