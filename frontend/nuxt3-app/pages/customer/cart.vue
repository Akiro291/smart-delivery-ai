<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Корзина</h1>
      <p class="text-gray-500 text-sm mt-1">Проверьте состав заказа и оформите доставку</p>
    </div>

    <template v-if="cartStore.items.length">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Товары -->
        <div class="lg:col-span-2 space-y-3">
          <div v-for="item in cartStore.items" :key="item.id" class="card p-4 flex items-center gap-4">
            <div class="h-14 w-14 rounded-lg bg-gradient-to-br from-brand-50 to-violet-50 flex items-center justify-center text-2xl flex-shrink-0">
              📦
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-800 text-sm truncate">{{ item.product_name }}</h3>
              <p class="text-xs text-gray-500">{{ formatMoney(item.product_price || 0) }} ₽ за шт.</p>
              <div class="flex items-center gap-2 mt-2">
                <button
                  @click="changeQty(item, item.quantity - 1)"
                  class="h-7 w-7 rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50 flex items-center justify-center transition-colors"
                >
                  −
                </button>
                <span class="w-8 text-center text-sm font-semibold">{{ item.quantity }}</span>
                <button
                  @click="changeQty(item, item.quantity + 1)"
                  class="h-7 w-7 rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50 flex items-center justify-center transition-colors"
                >
                  +
                </button>
              </div>
            </div>
            <div class="text-right flex-shrink-0">
              <p class="font-bold text-gray-900">{{ formatMoney(item.subtotal || 0) }} ₽</p>
              <button @click="cartStore.removeItem(item.id)" class="text-xs text-red-500 hover:text-red-700 mt-1">Удалить</button>
            </div>
          </div>
        </div>

        <!-- Оформление -->
        <div class="lg:col-span-1">
          <div class="card p-6 sticky top-24">
            <h3 class="font-semibold text-gray-800 mb-5">Оформление</h3>
            <div class="space-y-4">
              <div>
                <label class="label">Адрес забора</label>
                <input v-model="fromAddress" type="text" class="input" placeholder="ул. Ленина, 1" />
              </div>
              <div>
                <label class="label">Адрес доставки</label>
                <input v-model="toAddress" type="text" class="input" placeholder="ул. Мира, 5" />
              </div>
              <div>
                <label class="label">Комментарий</label>
                <input v-model="description" type="text" class="input" placeholder="Необязательно" />
              </div>
            </div>
            <div class="mt-6 pt-5 border-t border-gray-100 space-y-2">
              <div class="flex justify-between text-sm text-gray-500">
                <span>Товаров:</span>
                <span>{{ cartStore.totalQuantity }} шт.</span>
              </div>
              <div class="flex justify-between text-lg font-bold text-gray-900">
                <span>Итого</span>
                <span>{{ formatMoney(cartStore.totalAmount) }} ₽</span>
              </div>
            </div>
            <UiButton class="mt-5" block :loading="isCheckingOut" :disabled="!fromAddress || !toAddress" @click="checkout">
              Оформить заказ
            </UiButton>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="card">
      <UiEmptyState icon="🛒" title="Корзина пуста" description="Добавьте товары из каталога, чтобы оформить доставку">
        <NuxtLink to="/customer" class="btn-primary">Перейти в каталог</NuxtLink>
      </UiEmptyState>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

const cartStore = useCartStore()
const fromAddress = ref('')
const toAddress = ref('')
const description = ref('')
const isCheckingOut = ref(false)

onMounted(() => cartStore.fetchCart())

async function changeQty(item: { id: number; quantity: number }, value: number) {
  if (value < 1) {
    await cartStore.removeItem(item.id)
    return
  }
  await cartStore.updateQuantity(item.id, value)
}

async function checkout() {
  isCheckingOut.value = true
  try {
    await cartStore.checkout(fromAddress.value, toAddress.value, description.value)
    navigateTo('/customer/orders')
  } catch (e: any) {
    alert(e?.data?.detail || e?.message || 'Ошибка оформления заказа')
  } finally {
    isCheckingOut.value = false
  }
}
</script>
