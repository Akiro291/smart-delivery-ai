<template>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Каталог</h1>
        <NuxtLink to="/customer/cart" class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
          Корзина ({{ cartStore.totalQuantity }})
        </NuxtLink>
      </div>

      <div class="flex gap-2 flex-wrap">
        <button
          @click="selectedCategory = ''"
          :class="selectedCategory === '' ? 'bg-purple-600 text-white' : 'bg-white text-gray-700'"
          class="px-4 py-2 rounded shadow text-sm hover:bg-purple-50"
        >
          Все
        </button>
        <button
          v-for="cat in categories"
          :key="cat"
          @click="selectedCategory = cat"
          :class="selectedCategory === cat ? 'bg-purple-600 text-white' : 'bg-white text-gray-700'"
          class="px-4 py-2 rounded shadow text-sm hover:bg-purple-50"
        >
          {{ cat }}
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="product in filteredProducts" :key="product.id" class="bg-white p-6 rounded shadow">
          <h3 class="text-lg font-semibold mb-1">{{ product.name }}</h3>
          <p class="text-gray-500 text-sm min-h-[40px]">{{ product.description || 'Без описания' }}</p>
          <p class="text-xl font-bold mt-3 text-purple-600">{{ formatMoney(product.price) }} ₽</p>
          <button
            @click="addToCart(product)"
            :disabled="!product.is_available || adding"
            class="mt-4 w-full px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50"
          >
            {{ product.is_available ? 'В корзину' : 'Нет в наличии' }}
          </button>
        </div>
      </div>
      <div v-if="filteredProducts.length === 0" class="text-center py-12 text-gray-500">
        Товары не найдены
      </div>
    </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

interface Product {
  id: number
  name: string
  description: string | null
  price: number
  category: string | null
  is_available: boolean
}

const apiBase = useRuntimeConfig().public.apiBase
const authStore = useAuthStore()
const cartStore = useCartStore()
const products = ref<Product[]>([])
const categories = ref<string[]>([])
const selectedCategory = ref('')
const adding = ref(false)

const filteredProducts = computed(() =>
  selectedCategory.value ? products.value.filter((p) => p.category === selectedCategory.value) : products.value,
)

onMounted(async () => {
  try {
    const [productsData] = await Promise.all([$fetch(`${apiBase}/products/`), cartStore.fetchCart()])
    products.value = (productsData as Product[]).filter((p) => p.is_available)
    categories.value = [...new Set(products.value.map((p) => p.category).filter(Boolean))] as string[]
  } catch {
    products.value = []
  }
})

async function addToCart(product: Product) {
  adding.value = true
  try {
    await cartStore.addToCart(product.id, 1)
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка добавления в корзину')
  } finally {
    adding.value = false
  }
}

function formatMoney(value: number) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
