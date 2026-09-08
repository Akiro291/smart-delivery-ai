<template>
  <div class="space-y-6 max-w-2xl">
    <div>
      <NuxtLink to="/dashboard/products" class="text-sm font-medium text-brand-600 hover:text-brand-700 inline-flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        К товарам
      </NuxtLink>
      <h1 class="text-2xl font-bold tracking-tight mt-2">Создать товар</h1>
    </div>

    <div class="card p-6 sm:p-8">
      <form @submit.prevent="saveProduct" class="space-y-5">
        <div>
          <label class="label" for="name">Название</label>
          <input id="name" v-model="form.name" type="text" required class="input" placeholder="Например: Торт «Прага»" />
        </div>
        <div>
          <label class="label" for="category">Категория</label>
          <input id="category" v-model="form.category" type="text" class="input" placeholder="Кондитерские изделия" />
        </div>
        <div>
          <label class="label" for="description">Описание</label>
          <textarea id="description" v-model="form.description" rows="3" class="input resize-none" placeholder="Кратко о товаре" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label" for="price">Цена, ₽</label>
            <input id="price" v-model.number="form.price" type="number" step="0.01" required min="0" class="input" placeholder="0.00" />
          </div>
          <div>
            <label class="label" for="stock">На складе</label>
            <input id="stock" v-model.number="form.stock_quantity" type="number" min="0" class="input" placeholder="0" />
          </div>
        </div>
        <label class="flex items-center gap-3 cursor-pointer select-none">
          <input v-model="form.is_available" type="checkbox" class="h-4 w-4 rounded border-gray-300 text-brand-600 focus:ring-brand-500" />
          <span class="text-sm text-gray-700">Доступен для заказа</span>
        </label>

        <div class="flex gap-3 pt-4 border-t border-gray-100">
          <UiButton type="submit" :loading="isSaving">Сохранить</UiButton>
          <NuxtLink to="/dashboard/products" class="btn-secondary">Отмена</NuxtLink>
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
