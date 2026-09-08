<template>
    <div class="space-y-6">
      <h1 class="text-2xl font-bold text-gray-800">Корзина</h1>

      <div v-if="cartStore.items.length" class="space-y-4">
        <div v-for="item in cartStore.items" :key="item.id" class="bg-white p-4 rounded shadow flex items-center justify-between">
          <div>
            <h3 class="font-semibold">{{ item.product_name }}</h3>
            <p class="text-sm text-gray-500">{{ formatMoney(item.product_price || 0) }} ₽ × {{ item.quantity }}</p>
          </div>
          <div class="flex items-center gap-3">
            <input
              type="number"
              min="1"
              :value="item.quantity"
              @change="onQuantity(item, $event)"
              class="w-16 border rounded px-2 py-1 text-sm"
            />
            <span class="w-24 text-right font-medium">{{ formatMoney(item.subtotal || 0) }} ₽</span>
            <button @click="cartStore.removeItem(item.id)" class="text-red-600 hover:text-red-800">Удалить</button>
          </div>
        </div>

        <div class="bg-white p-6 rounded shadow max-w-lg space-y-4">
          <h3 class="text-lg font-semibold">Оформление заказа</h3>
          <div>
            <label class="block text-sm font-medium">Адрес забора</label>
            <input v-model="fromAddress" type="text" class="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label class="block text-sm font-medium">Адрес доставки</label>
            <input v-model="toAddress" type="text" class="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div>
            <label class="block text-sm font-medium">Комментарий</label>
            <input v-model="description" type="text" class="mt-1 w-full border rounded px-3 py-2" />
          </div>
          <div class="flex justify-between text-lg font-bold">
            <span>Итого:</span>
            <span>{{ formatMoney(cartStore.totalAmount) }} ₽</span>
          </div>
          <button
            @click="checkout"
            :disabled="!fromAddress || !toAddress || isCheckingOut"
            class="w-full px-4 py-3 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50"
          >
            {{ isCheckingOut ? 'Оформление...' : 'Оформить заказ' }}
          </button>
        </div>
      </div>

      <div v-else class="bg-white p-12 rounded shadow text-center text-gray-500">
        Корзина пуста.
        <NuxtLink to="/customer" class="text-purple-600 hover:underline">Перейти в каталог</NuxtLink>
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

async function onQuantity(item: { id: number; quantity: number }, event: Event) {
  const value = Math.max(1, Number((event.target as HTMLInputElement).value) || 1)
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

function formatMoney(value: number) {
  return Number(value).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}
</script>
