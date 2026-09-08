<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Каталог</h1>
        <p class="text-gray-500 text-sm mt-1">Выберите товары и оформите доставку</p>
      </div>
      <NuxtLink to="/customer/cart" class="btn-primary self-start sm:self-auto">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.3 2.3c-.6.6-.2 1.7.7 1.7H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 012 2z" />
        </svg>
        Корзина · {{ cartStore.totalQuantity }}
      </NuxtLink>
    </div>

    <!-- Категории -->
    <div class="flex gap-2 flex-wrap">
      <button
        @click="selectedCategory = ''"
        :class="selectedCategory === '' ? 'bg-brand-600 text-white shadow-sm' : 'card text-gray-700 hover:border-brand-200'"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
      >
        Все
      </button>
      <button
        v-for="cat in categories"
        :key="cat"
        @click="selectedCategory = cat"
        :class="selectedCategory === cat ? 'bg-brand-600 text-white shadow-sm' : 'card hover:border-brand-200'"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
      >
        {{ cat }}
      </button>
    </div>

    <!-- Товары -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <div v-for="product in filteredProducts" :key="product.id" class="card card-hover overflow-hidden group">
        <div class="h-36 bg-gradient-to-br from-brand-50 to-violet-50 flex items-center justify-center text-5xl group-hover:scale-105 transition-transform duration-300">
          {{ productEmoji }}
        </div>
        <div class="p-5">
          <div class="flex items-start justify-between gap-2">
            <h3 class="font-semibold text-gray-800 text-sm leading-snug">{{ product.name }}</h3>
          </div>
          <p class="text-xs text-gray-400 mt-0.5">{{ product.category || 'Без категории' }}</p>
          <p class="text-sm text-gray-600 mt-2 line-clamp-2 min-h-[40px]">{{ product.description || 'Без описания' }}</p>
          <div class="flex items-center justify-between mt-4">
            <span class="text-lg font-bold text-gray-900">{{ formatMoney(product.price) }} ₽</span>
            <button
              @click="addToCart(product)"
              :disabled="!product.is_available || adding"
              class="h-9 w-9 rounded-lg bg-brand-600 text-white flex items-center justify-center hover:bg-brand-700 active:scale-95 transition-all disabled:opacity-40"
              :title="product.is_available ? 'Добавить в корзину' : 'Нет в наличии'"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <UiSpinner v-if="isLoading" label="Загрузка каталога…" />
    <div v-if="!isLoading && filteredProducts.length === 0" class="card">
      <UiEmptyState icon="🔍" title="Товары не найдены" description="В этой категории пока пусто">
        <button class="btn-secondary" @click="selectedCategory = ''">Показать все</button>
      </UiEmptyState>
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
const cartStore = useCartStore()
const products = ref<Product[]>([])
const categories = ref<string[]>([])
const selectedCategory = ref('')
const adding = ref(false)
const isLoading = ref(true)

const filteredProducts = computed(() =>
  selectedCategory.value ? products.value.filter((p) => p.category === selectedCategory.value) : products.value,
)

const productEmoji = computed(() => {
  const emojis = ['📦', '🎁', '🥡', '🧺', '🍞']
  return emojis[Math.min(filteredProducts.value.length, emojis.length - 1)]
})

onMounted(async () => {
  try {
    const [productsData] = await Promise.all([$fetch(`${apiBase}/products/?limit=100`), cartStore.fetchCart()])
    products.value = (productsData as Product[]).filter((p) => p.is_available)
    categories.value = [...new Set(products.value.map((p) => p.category).filter(Boolean))] as string[]
  } catch {
    products.value = []
  } finally {
    isLoading.value = false
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
</script>
