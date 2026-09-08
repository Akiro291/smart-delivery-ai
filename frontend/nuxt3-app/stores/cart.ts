// Cart store
import { defineStore } from 'pinia'

interface CartItem {
  id: number
  product_id: number
  product_name?: string
  product_price?: number
  subtotal?: number
  quantity: number
}

interface CartState {
  items: CartItem[]
  isLoading: boolean
  error: string | null
}

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    items: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    totalQuantity: (state) => state.items.reduce((sum, i) => sum + i.quantity, 0),
    totalAmount: (state) =>
      state.items.reduce((sum, i) => sum + (i.subtotal ?? (i.product_price || 0) * i.quantity), 0),
  },

  actions: {
    _headers() {
      const { token } = useAuthStore()
      return { Authorization: `Bearer ${token}` }
    },

    async fetchCart() {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const items = await $fetch(`${apiBase}/cart/`, {
          headers: this._headers(),
        })
        this.items = items as CartItem[]
      } catch (err: any) {
        this.error = err?.message || 'Failed to fetch cart'
      } finally {
        this.isLoading = false
      }
    },

    async addToCart(productId: number, quantity = 1) {
      const apiBase = useRuntimeConfig().public.apiBase
      await $fetch(`${apiBase}/cart/add`, {
        method: 'POST',
        body: { product_id: productId, quantity },
        headers: { ...this._headers(), 'Content-Type': 'application/json' },
      })
      await this.fetchCart()
    },

    async updateQuantity(itemId: number, quantity: number) {
      const apiBase = useRuntimeConfig().public.apiBase
      await $fetch(`${apiBase}/cart/${itemId}`, {
        method: 'PUT',
        body: { quantity },
        headers: { ...this._headers(), 'Content-Type': 'application/json' },
      })
      await this.fetchCart()
    },

    async removeItem(itemId: number) {
      const apiBase = useRuntimeConfig().public.apiBase
      await $fetch(`${apiBase}/cart/${itemId}`, {
        method: 'DELETE',
        headers: this._headers(),
      })
      await this.fetchCart()
    },

    async clearCart() {
      const apiBase = useRuntimeConfig().public.apiBase
      await $fetch(`${apiBase}/cart/clear`, {
        method: 'DELETE',
        headers: this._headers(),
      })
      this.items = []
    },

    async checkout(fromAddress: string, toAddress: string, description?: string) {
      const apiBase = useRuntimeConfig().public.apiBase
      const order = await $fetch(`${apiBase}/cart/checkout`, {
        method: 'POST',
        body: { from_address: fromAddress, to_address: toAddress, description: description || null },
        headers: { ...this._headers(), 'Content-Type': 'application/json' },
      })
      this.items = []
      return order
    },
  },
})
