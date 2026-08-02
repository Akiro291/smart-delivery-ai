// Order store
interface OrderState {
  orders: Order[]
  currentOrder: Order | null
  loading: boolean
}

export const useOrderStore = defineStore('orders', {
  state: (): OrderState => ({
    orders: [],
    currentOrder: null,
    loading: false
  }),
  
  actions: {
    setOrders(orders: Order[]) {
      this.orders = orders
    },
    setCurrentOrder(order: Order | null) {
      this.currentOrder = order
    },
    setLoading(loading: boolean) {
      this.loading = loading
    }
  }
})