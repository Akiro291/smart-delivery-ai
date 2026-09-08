<template>
  <div class="space-y-6">
    <div class="flex items-center gap-4">
      <NuxtLink to="/dashboard/products" class="text-blue-600 hover:underline">&larr; Назад к товарам</NuxtLink>
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
            <input v-model.number="form.stock_quantity" type="number" min="0" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="0" />
          </div>
        </div>
        <div class="flex items-center gap-2">
          <input v-model="form.is_available" id="available" type="checkbox" class="rounded" />
          <label for="available" class="text-sm">Доступен для заказа</label>
        </div>
        <div class="flex gap-4 pt-4">
          <button type="submit" :disabled="isSaving" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
            {{ isSaving ? 'Сохранение...' : 'Сохранить' }}
          </button>
          <NuxtLink to="/dashboard/products" class="px-6 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">Отмена</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'manager', layout: 'manager' })

const authStore = useAuthStore()
const apiBase = useRuntimeConfig().public.apiBase
const isSaving = ref(false)

const form = reactive({
  name: '',
  category: '',
  description: '',
  price: 0,
  stock_quantity: 0,
  is_available: true,
})

async function saveProduct() {
  isSaving.value = true
  try {
    await $fetch(`${apiBase}/products/`, {
      method: 'POST',
      body: {
        name: form.name,
        category: form.category || null,
        description: form.description || null,
        price: form.price,
        stock_quantity: form.stock_quantity,
        is_available: form.is_available,
      },
      headers: { Authorization: `Bearer ${authStore.token}` },
    })
    navigateTo('/dashboard/products')
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка создания товара')
  } finally {
    isSaving.value = false
  }
}
</script>
