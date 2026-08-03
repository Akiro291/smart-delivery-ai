<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">Товары</h1>
          <NuxtLink to="/dashboard/products/create" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            + Добавить
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <NuxtLink v-for="item in products" :key="item.id" :to="`/dashboard/products/${item.id}`" class="bg-white p-4 rounded shadow hover:shadow-lg transition-shadow cursor-pointer block">
            <div class="h-32 bg-gray-200 rounded mb-4 flex items-center justify-center text-4xl">{{ item.emoji }}</div>
            <h3 class="font-semibold">{{ item.name }}</h3>
            <p class="text-sm text-gray-500">{{ item.category }}</p>
            <div class="flex justify-between items-center mt-3">
              <span class="font-bold">{{ formatPrice(item.price) }}</span>
              <span class="text-sm text-gray-500">В наличии: {{ item.stock }}</span>
            </div>
          </NuxtLink>
        </div>
        <div v-if="products.length === 0" class="text-center py-12 text-gray-500">Товаров пока нет</div>
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

const products = useState<Product[]>('products', () => [
  { id: 1, name: 'Ноутбук', category: 'Электроника', description: 'Мощный ноутбук для работы и игр', price: 45000, stock: 15, emoji: '💻' },
  { id: 2, name: 'Наушники', category: 'Электроника', description: 'Беспроводные наушники с шумоподавлением', price: 3500, stock: 50, emoji: '🎧' },
  { id: 3, name: 'Кофеварка', category: 'Бытовая техника', description: 'Автоматическая кофеварка с капучинатором', price: 12000, stock: 8, emoji: '☕' },
])

function formatPrice(price: number) {
  return price.toFixed(2) + ' ₽'
}
</script>
