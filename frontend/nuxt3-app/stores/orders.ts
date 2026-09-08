// Order store
import { defineStore } from 'pinia'

interface OrderItem {
  id: number
  order_id: number
  product_id: number
  product_name: string
  quantity: number
  price: number
  created_at: string | null
}

interface Order {
  id: number
  customer_id: number
  courier_id: number | null
  from_address: string
  to_address: string
  status: string
  total_amount: number
  description: string | null
  created_at: string | null
  updated_at: string | null
  items?: OrderItem[]
}

interface OrderState {
  orders: Order[]
  currentOrder: Order | null
  isLoading: boolean
  error: string | null
}

interface OrderStats {
  total: number
  by_status: Record<string, number>
  completed_revenue: number
  active: number
}

export const useOrdersStore = defineStore('orders', {
  state: (): OrderState => ({
    orders: [],
    currentOrder: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    getOrderById: (state) => (id: number) => {
      return state.orders.find((o) => o.id === id) || state.currentOrder
    },
    getOrdersByStatus: (state) => (status: string) => {
      return state.orders.filter((o) => o.status === status)
    },
  },

  actions: {
    async fetchOrders(skip = 0, limit = 50, statusFilter?: string) {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const query: Record<string, string | number> = { skip, limit }
        if (statusFilter) query.status_filter = statusFilter

        const orders = await $fetch(`${apiBase}/orders/`, {
          method: 'GET',
          query,
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.orders = orders as Order[]
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch orders'
      } finally {
        this.isLoading = false
      }
    },

    async fetchOrder(orderId: number) {
      this.isLoading = true
      this.error = null
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const order = await $fetch(`${apiBase}/orders/${orderId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.currentOrder = order as Order
        return order
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch order'
        return null
      } finally {
        this.isLoading = false
      }
    },

    async createOrder(orderData: {
      from_address: string
      to_address: string
      total_amount: number
      description?: string
      items?: Array<{
        product_id: number
        product_name: string
        quantity: number
        price: number
      }>
    }) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const order = await $fetch(`${apiBase}/orders/`, {
          method: 'POST',
          body: orderData,
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        this.orders.unshift(order as Order)
        return order
      } catch (err: any) {
        this.error = err.message || 'Failed to create order'
        throw err
      }
    },

    async updateOrder(orderId: number, orderData: Record<string, any>) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const order = await $fetch(`${apiBase}/orders/${orderId}`, {
          method: 'PUT',
          body: orderData,
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        const index = this.orders.findIndex((o) => o.id === orderId)
        if (index !== -1) {
          this.orders[index] = order as Order
        }
        return order
      } catch (err: any) {
        this.error = err.message || 'Failed to update order'
        throw err
      }
    },

    async getOrderHistory(orderId: number) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const history = await $fetch(`${apiBase}/orders/${orderId}/history`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        return history
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch order history'
        throw err
      }
    },

    async fetchStats(): Promise<OrderStats | null> {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const stats = await $fetch(`${apiBase}/orders/stats/summary`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        return stats as OrderStats
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch stats'
        return null
      }
    },

    async assignCourier(orderId: number, courierId: number) {
      try {
        const apiBase = useRuntimeConfig().public.apiBase
        const { token } = useAuthStore()
        const order = await $fetch(`${apiBase}/orders/${orderId}/assign`, {
          method: 'POST',
          body: { courier_id: courierId },
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        const index = this.orders.findIndex((o) => o.id === orderId)
        if (index !== -1) {
          this.orders[index] = order as Order
        }
        return order
      } catch (err: any) {
        this.error = err.message || 'Failed to assign courier'
        throw err
      }
    },

    clearCurrentOrder() {
      this.currentOrder = null
    },
  },
})
