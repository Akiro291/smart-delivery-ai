<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">Товары</h1>
          <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Добавить</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="item in products" :key="item.id" class="bg-white p-4 rounded shadow">
            <div class="h-32 bg-gray-200 rounded mb-4 flex items-center justify-center text-4xl">{{ item.emoji }}</div>
            <h3 class="font-semibold">{{ item.name }}</h3>
            <p class="text-sm text-gray-500">{{ item.category }}</p>
            <div class="flex justify-between items-center mt-3">
              <span class="font-bold">{{ item.price }} ₽</span>
              <span class="text-sm text-gray-500">В наличии: {{ item.stock }}</span>
            </div>
          </div>
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
  price: number
  stock: number
  emoji: string
}

const products = ref<Product[]>([
  { id: 1, name: 'Ноутбук', category: 'Электроника', price: 45000, stock: 15, emoji: '💻' },
  { id: 2, name: 'Наушники', category: 'Электроника', price: 3500, stock: 50, emoji: '🎧' },
  { id: 3, name: 'Кофеварка', category: 'Бытовая техника', price: 12000, stock: 8, emoji: '☕' },
])
</script>
