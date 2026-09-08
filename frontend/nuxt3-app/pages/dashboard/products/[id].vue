<template>
  <div class="space-y-6 max-w-2xl">
    <div>
      <NuxtLink to="/dashboard/products" class="text-sm font-medium text-brand-600 hover:text-brand-700 inline-flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        К товарам
      </NuxtLink>
      <h1 class="text-2xl font-bold tracking-tight mt-2">{{ product?.name || 'Товар' }}</h1>
    </div>

    <div v-if="product" class="card overflow-hidden">
      <div class="h-40 bg-gradient-to-br from-brand-50 to-violet-50 flex items-center justify-center text-6xl">
        📦
      </div>
      <div class="p-6 sm:p-8">
        <div class="flex items-start justify-between gap-4 mb-6">
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wider font-medium">{{ product.category || 'Без категории' }}</p>
            <p class="text-gray-600 mt-2">{{ product.description || 'Без описания' }}</p>
          </div>
          <span :class="product.is_available ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-200 text-gray-500'" class="badge flex-shrink-0">
            {{ product.is_available ? 'Доступен' : 'Скрыт' }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div class="rounded-xl bg-gray-50 p-5">
            <p class="text-xs text-gray-500 font-medium">Цена</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">{{ formatMoney(product.price) }} ₽</p>
          </div>
          <div class="rounded-xl bg-gray-50 p-5">
            <p class="text-xs text-gray-500 font-medium">На складе</p>
            <p class="text-2xl font-bold text-gray-900 mt-1">{{ product.stock_quantity ?? '∞' }} шт</p>
          </div>
        </div>

        <div class="flex gap-3 mt-8">
          <UiButton @click="toggleAvailability">
            {{ product.is_available ? 'Скрыть из каталога' : 'Вернуть в каталог' }}
          </UiButton>
        </div>
      </div>
    </div>

    <UiSpinner v-else-if="isLoading" label="Загрузка…" />
    <div v-else class="card">
      <UiEmptyState icon="❓" title="Товар не найден" description="Возможно, он был удалён">
        <NuxtLink to="/dashboard/products" class="btn-secondary">К списку товаров</NuxtLink>
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
</script>
