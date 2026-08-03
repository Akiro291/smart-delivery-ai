<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex items-center gap-4">
          <NuxtLink to="/dashboard/products" class="text-blue-600 hover:underline">← Назад к товарам</NuxtLink>
          <h1 class="text-2xl font-bold text-gray-800">Товар</h1>
        </div>
        <div v-if="product" class="bg-white rounded shadow p-6">
          <div class="flex gap-6">
            <div class="flex-1">
              <div class="h-64 bg-gray-200 rounded mb-6 flex items-center justify-center text-6xl">{{ product.emoji }}</div>
              <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
              <p class="text-gray-500 mb-4">{{ product.category }}</p>
              <p class="text-gray-700 mb-6">{{ product.description }}</p>
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-gray-50 p-4 rounded">
                  <p class="text-sm text-gray-500">Цена</p>
                  <p class="text-xl font-bold">{{ formatPrice(product.price) }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded">
                  <p class="text-sm text-gray-500">В наличии</p>
                  <p class="text-xl font-bold">{{ product.stock }} шт</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-12 text-gray-500">Товар не найден</div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface Product {
  id: number
  name: string
  category: string
  description: string
  price: number
  stock: number
  emoji: string
}

const route = useRoute()
const productId = Number(route.params.id)

const products = useState<Product[]>('products', () => [
  { id: 1, name: 'Ноутбук', category: 'Электроника', description: 'Мощный ноутбук для работы и игр', price: 45000, stock: 15, emoji: '💻' },
  { id: 2, name: 'Наушники', category: 'Электроника', description: 'Беспроводные наушники с шумоподавлением', price: 3500, stock: 50, emoji: '🎧' },
  { id: 3, name: 'Кофеварка', category: 'Бытовая техника', description: 'Автоматическая кофеварка с капучинатором', price: 12000, stock: 8, emoji: '☕' },
])

const product = computed(() => products.value.find(p => p.id === productId))

function formatPrice(price: number) {
  return price.toFixed(2) + ' ₽'
}
</script>
