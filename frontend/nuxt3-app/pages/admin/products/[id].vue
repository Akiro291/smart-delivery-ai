<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-4">
        <NuxtLink to="/admin/products" class="text-blue-600 hover:underline">← Назад к товарам</NuxtLink>
        <h1 class="text-2xl font-bold text-gray-800">Товар #{{ productId }}</h1>
      </div>
      <div class="flex gap-2">
        <button @click="startEdit" v-if="!isEditing" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          ✏️ Редактировать
        </button>
        <button @click="toggleEditMode" v-if="isEditing" class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700">
          ← Назад
        </button>
      </div>
    </div>

    <!-- Режим просмотра -->
    <div v-if="product && !isEditing" class="bg-white rounded shadow p-6">
      <div class="flex gap-6">
        <div class="w-64">
          <div v-if="product.image_url" class="h-64 bg-gray-100 rounded mb-4 overflow-hidden">
            <img :src="getFullImageUrl(product.image_url)" :alt="product.name" class="w-full h-full object-cover" />
          </div>
          <div v-else class="h-64 bg-gray-200 rounded mb-4 flex items-center justify-center text-6xl">📦</div>
          
          <!-- Загрузка фото -->
          <div class="space-y-2">
            <label class="flex items-center justify-center w-full h-10 border-2 border-dashed border-gray-300 rounded cursor-pointer hover:border-blue-500 transition-colors">
              <span class="text-sm text-gray-500">📷 Загрузить фото</span>
              <input type="file" accept="image/*" @change="handleImageUpload" class="hidden" />
            </label>
            <button v-if="product.image_url" @click="deleteImage" class="w-full px-3 py-1 text-sm text-red-600 border border-red-300 rounded hover:bg-red-50">
              Удалить фото
            </button>
          </div>
        </div>
        <div class="flex-1">
          <h2 class="text-2xl font-bold mb-2">{{ product.name }}</h2>
          <p class="text-gray-500 mb-4">{{ product.category || 'Без категории' }}</p>
          <p class="text-gray-700 mb-6">{{ product.description || 'Нет описания' }}</p>
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-gray-500">Цена</p>
              <p class="text-xl font-bold">{{ formatPrice(product.price) }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-gray-500">В наличии</p>
              <p class="text-xl font-bold">{{ product.stock_quantity }} шт</p>
            </div>
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-gray-500">Доступен</p>
              <p class="text-xl font-bold">{{ product.is_available ? 'Да' : 'Нет' }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded">
              <p class="text-sm text-gray-500">ID</p>
              <p class="text-xl font-bold">#{{ product.id }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Режим редактирования -->
    <div v-if="product && isEditing" class="bg-white rounded shadow p-6 max-w-2xl">
      <h2 class="text-xl font-bold mb-4">Редактировать товар</h2>
      <form @submit.prevent="saveProduct" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
          <input v-model="editForm.name" type="text" required class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
          <input v-model="editForm.category" type="text" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
          <textarea v-model="editForm.description" rows="3" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Цена (₽)</label>
            <input v-model.number="editForm.price" type="number" step="0.01" min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Количество</label>
            <input v-model.number="editForm.stock_quantity" type="number" min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
        </div>
        <div class="flex items-center gap-4">
          <label class="flex items-center gap-2">
            <input v-model="editForm.is_available" type="checkbox" class="w-4 h-4" />
            <span class="text-sm">Товар доступен</span>
          </label>
        </div>
        <div class="flex gap-4 pt-4">
          <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">💾 Сохранить</button>
          <button type="button" @click="toggleEditMode" class="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Отмена</button>
        </div>
      </form>
    </div>

    <div v-if="!product" class="text-center py-12 text-gray-500">Товар не найден</div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

interface Product {
  id: number
  name: string
  category: string | null
  description: string | null
  price: number
  stock_quantity: number
  image_url: string | null
  is_available: boolean
  created_at: string | null
}

const apiBase = useRuntimeConfig().public.apiBase
const route = useRoute()
const productId = Number(route.params.id)
const authStore = useAuthStore()

const product = ref<Product | null>(null)
const isEditing = ref(false)
const uploadLoading = ref(false)

const editForm = reactive({
  name: '',
  category: '',
  description: '',
  price: 0,
  stock_quantity: 0,
  is_available: true,
})

async function fetchProduct() {
  try {
    product.value = await $fetch(`${apiBase}/products/${productId}`, {
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    console.log('Product loaded:', product.value)
  } catch (e: any) {
    console.error('Error fetching product:', e)
    alert(e.response?.data?.detail || 'Ошибка загрузки товара')
  }
}

function startEdit() {
  if (product.value) {
    editForm.name = product.value.name
    editForm.category = product.value.category || ''
    editForm.description = product.value.description || ''
    editForm.price = product.value.price
    editForm.stock_quantity = product.value.stock_quantity
    editForm.is_available = product.value.is_available
    isEditing.value = true
  }
}

function toggleEditMode() {
  isEditing.value = !isEditing.value
}

async function saveProduct() {
  try {
    await $fetch(`${apiBase}/products/${productId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: editForm,
    })
    await fetchProduct()
    isEditing.value = false
    alert('Товар обновлён!')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка сохранения')
  }
}

async function handleImageUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  uploadLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)

    await $fetch(`${apiBase}/products/${productId}/image`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${authStore.token}` },
      body: formData,
    })
    await fetchProduct()
    alert('Фото загружено!')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка загрузки фото')
  } finally {
    uploadLoading.value = false
  }
}

async function deleteImage() {
  if (!confirm('Удалить фото товара?')) return
  
  try {
    await $fetch(`${apiBase}/products/${productId}/image`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    await fetchProduct()
    alert('Фото удалено!')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка удаления')
  }
}

function formatPrice(price: number) {
  return price.toFixed(2) + ' ₽'
}

function getFullImageUrl(imageUrl: string) {
  return `http://localhost:8000${imageUrl}`
}

onMounted(fetchProduct)
</script>
