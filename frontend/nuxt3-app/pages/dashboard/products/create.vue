<template>
  <DashboardLayout>
    <template #default>
      <div class="space-y-6">
        <div class="flex items-center gap-4">
          <NuxtLink to="/dashboard/products" class="text-blue-600 hover:underline">← Назад к товарам</NuxtLink>
          <h1 class="text-2xl font-bold text-gray-800">Создать товар</h1>
        </div>
        <div class="bg-white rounded shadow p-6 max-w-2xl">
          <form @submit.prevent="saveProduct" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
              <input v-model="form.name" type="text" required class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Введите название товара" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
              <input v-model="form.category" type="text" required class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Например: Электроника" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
              <textarea v-model="form.description" rows="3" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Описание товара"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Цена (₽)</label>
                <input v-model.number="form.price" type="number" step="0.01" required min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="0.00" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Количество</label>
                <input v-model.number="form.stock" type="number" required min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="0" />
              </div>
            </div>
            <div class="flex gap-4 pt-4">
              <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Сохранить</button>
              <NuxtLink to="/dashboard/products" class="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Отмена</NuxtLink>
            </div>
          </form>
        </div>
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

const emojiOptions = ['📦', '💻', '🎧', '☕', '📱', '⌚', '🖥️', '🎮', '📷', '🔌', '🖨️', '⌨️']
const emojis = emojiOptions[Math.floor(Math.random() * emojiOptions.length)]

const form = reactive({
  name: '',
  category: '',
  description: '',
  price: 0,
  stock: 0,
})

const products = useState<Product[]>('products', () => [
  { id: 1, name: 'Ноутбук', category: 'Электроника', description: 'Мощный ноутбук для работы и игр', price: 45000, stock: 15, emoji: '💻' },
  { id: 2, name: 'Наушники', category: 'Электроника', description: 'Беспроводные наушники с шумоподавлением', price: 3500, stock: 50, emoji: '🎧' },
  { id: 3, name: 'Кофеварка', category: 'Бытовая техника', description: 'Автоматическая кофеварка с капучинатором', price: 12000, stock: 8, emoji: '☕' },
])

function saveProduct() {
  const newProduct: Product = {
    id: products.value.length + 1,
    ...form,
    emoji: emojis,
  }
  products.value.push(newProduct)
  navigateTo('/dashboard/products')
}
</script>
