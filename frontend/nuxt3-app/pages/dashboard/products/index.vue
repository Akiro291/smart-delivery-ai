<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Товары</h1>
        <p class="text-gray-500 text-sm mt-1">Каталог платформы</p>
      </div>
      <div class="flex gap-2">
        <button @click="load" class="btn-secondary">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Обновить
        </button>
        <NuxtLink to="/dashboard/products/create" class="btn-primary">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Добавить
        </NuxtLink>
      </div>
    </div>

    <div v-if="products.length" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5">
      <div v-for="item in products" :key="item.id" class="card card-hover overflow-hidden group">
        <div class="h-32 bg-gradient-to-br from-brand-50 to-violet-50 flex items-center justify-center text-4xl group-hover:scale-105 transition-transform duration-300 relative">
          📦
          <span
            :class="item.is_available ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-200 text-gray-500'"
            class="badge absolute top-3 right-3"
          >
            {{ item.is_available ? 'Доступен' : 'Скрыт' }}
          </span>
        </div>
        <NuxtLink :to="`/dashboard/products/${item.id}`" class="block p-5">
          <h3 class="font-semibold text-gray-800 text-sm truncate">{{ item.name }}</h3>
          <p class="text-xs text-gray-400 mt-0.5">{{ item.category || 'Без категории' }}</p>
          <div class="flex items-center justify-between mt-3">
            <span class="font-bold text-gray-900">{{ formatMoney(item.price) }} ₽</span>
            <span class="text-xs text-gray-400">склад: {{ item.stock_quantity ?? '∞' }}</span>
          </div>
        </NuxtLink>
      </div>
    </div>

    <UiSpinner v-if="isLoading" label="Загрузка…" />
    <div v-else-if="products.length === 0" class="card">
      <UiEmptyState icon="🛒" title="Товаров пока нет" description="Создайте первый товар каталога">
        <NuxtLink to="/dashboard/products/create" class="btn-primary">Создать товар</NuxtLink>
      </UiEmptyState>
    </div>
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
</script>
