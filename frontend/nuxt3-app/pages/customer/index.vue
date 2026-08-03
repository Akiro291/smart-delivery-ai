<template>
  <CustomerLayout>
    <div class="space-y-6">
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-800">Каталог услуг</h1>
        <div v-if="authStore.isCustomer" class="flex gap-2">
          <button @click="showRoleModal = true" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm">
            Запросить роль курьера
          </button>
        </div>
      </div>

      <!-- Role Request Status -->
      <div v-if="roleRequest" class="bg-white rounded shadow p-4">
        <div class="flex items-center gap-3">
          <span :class="requestStatusClass(roleRequest.status)" class="px-3 py-1 rounded-full text-xs font-medium">
            {{ requestStatusLabel(roleRequest.status) }}
          </span>
          <span class="text-sm text-gray-600">
            Запрошена роль: {{ roleRequest.requested_role }}
          </span>
        </div>
        <p v-if="roleRequest.reason" class="text-sm text-gray-500 mt-1">{{ roleRequest.reason }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x1F4E6;</div>
          <h3 class="text-lg font-semibold mb-2">Стандартная доставка</h3>
          <p class="text-gray-500 text-sm">Доставка в течение 1-3 дней</p>
          <p class="text-xl font-bold mt-4 text-purple-600">от 299 ₽</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x26A1;</div>
          <h3 class="text-lg font-semibold mb-2">Экспресс доставка</h3>
          <p class="text-gray-500 text-sm">Доставка в течение 2-4 часов</p>
          <p class="text-xl font-bold mt-4 text-purple-600">от 599 ₽</p>
        </div>
        <div class="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow cursor-pointer">
          <div class="text-4xl mb-4">&#x1F3E2;</div>
          <h3 class="text-lg font-semibold mb-2">Корпоративная доставка</h3>
          <p class="text-gray-500 text-sm">Для бизнеса с особыми условиями</p>
          <p class="text-xl font-bold mt-4 text-purple-600">по запросу</p>
        </div>
      </div>
    </div>

    <!-- Role Request Modal -->
    <div v-if="showRoleModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h2 class="text-xl font-bold mb-4">Запросить роль курьера</h2>
        <p class="text-sm text-gray-600 mb-4">
          Вы можете запросить роль курьера. После одобрения администратором вы сможете принимать заказы.
        </p>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Причина (необязательно)</label>
          <textarea v-model="reason" rows="3" class="w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-500" placeholder="Почему вы хотите стать курьером?"></textarea>
        </div>
        <div class="flex gap-2">
          <button @click="submitRequest" :disabled="submitting" class="flex-1 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">
            {{ submitting ? 'Отправка...' : 'Отправить заявку' }}
          </button>
          <button @click="showRoleModal = false" class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
            Отмена
          </button>
        </div>
      </div>
    </div>
  </CustomerLayout>
</template>

<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'customer'], layout: 'customer' })

const authStore = useAuthStore()
const showRoleModal = ref(false)
const reason = ref('')
const submitting = ref(false)
const roleRequest = ref<any>(null)

function requestStatusClass(status: string) {
  const classes = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    APPROVED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

function requestStatusLabel(status: string) {
  const labels = {
    PENDING: 'На рассмотрении',
    APPROVED: 'Одобрено',
    REJECTED: 'Отклонено',
  }
  return labels[status] || status
}

async function submitRequest() {
  submitting.value = true
  try {
    await authStore.requestRoleChange('COURIER', reason.value || undefined)
    await fetchRoleRequest()
    showRoleModal.value = false
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Ошибка при отправке заявки')
  } finally {
    submitting.value = false
  }
}

async function fetchRoleRequest() {
  try {
    roleRequest.value = await authStore.getMyRoleRequest()
  } catch (e) {
    console.error('Error fetching role request:', e)
  }
}

onMounted(fetchRoleRequest)
</script>
