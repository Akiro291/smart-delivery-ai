<template>
  <div class="space-y-6">
    <div class="flex items-center gap-4">
      <NuxtLink to="/admin/products" class="text-blue-600 hover:underline">← Назад к товарам</NuxtLink>
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
          <input v-model="form.category" type="text" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Например: Электроника" />
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
            <input v-model.number="form.stock_quantity" type="number" required min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="0" />
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input v-model="form.is_available" type="checkbox" class="w-4 h-4" />
          <label class="text-sm">Товар доступен</label>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Фото товара</label>
          <div class="flex items-center gap-4">
            <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded cursor-pointer hover:border-blue-500 transition-colors">
              <div v-if="previewUrl" class="w-full h-full p-2">
                <img :src="previewUrl" alt="Preview" class="w-full h-full object-cover rounded" />
              </div>
              <div v-else class="text-center">
                <span class="text-2xl">📷</span>
                <p class="text-sm text-gray-500 mt-2">Выберите фото</p>
              </div>
              <input type="file" accept="image/*" @change="handleFileChange" class="hidden" />
            </label>
          </div>
        </div>
        <div class="flex gap-4 pt-4">
          <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700" :disabled="loading">
            {{ loading ? 'Создание...' : 'Сохранить' }}
          </button>
          <NuxtLink to="/admin/products" class="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Отмена</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'admin'], layout: 'admin' })

const apiBase = useRuntimeConfig().public.apiBase
const authStore = useAuthStore()
const loading = ref(false)
const previewUrl = ref('')
const selectedFile = ref<File | null>(null)

const form = reactive({
  name: '',
  category: '',
  description: '',
  price: 0,
  stock_quantity: 0,
  is_available: true,
})

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

async function saveProduct() {
  loading.value = true
  let productId: number | null = null
  
  try {
    const product = await $fetch(`${apiBase}/products/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${authStore.token}`,
        'Content-Type': 'application/json',
      },
      body: form,
    }) as any
    productId = product.id
    console.log('Product created with ID:', productId)
    
    if (selectedFile.value) {
      console.log('Uploading image for product:', productId)
      const formData = new FormData()
      formData.append('file', selectedFile.value)
      
      await $fetch(`${apiBase}/products/${productId}/image`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${authStore.token}` },
        body: formData,
      })
      console.log('Image uploaded successfully')
    }
    
    navigateTo('/admin/products')
  } catch (e: any) {
    console.error('Error creating product:', e)
    console.error('Error response:', e.response)
    const errorMessage = e.response?.data?.detail || e.message || 'Ошибка при создании товара'
    alert(`Ошибка: ${errorMessage}`)
    loading.value = false
  }
}
</script>
