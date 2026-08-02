// User store
interface UserState {
  users: User[]
  currentUser: User | null
  loading: boolean
}

export const useUserStore = defineStore('users', {
  state: (): UserState => ({
    users: [],
    currentUser: null,
    loading: false
  }),
  
  actions: {
    setUsers(users: User[]) {
      this.users = users
    },
    setCurrentUser(user: User | null) {
      this.currentUser = user
    },
    setLoading(loading: boolean) {
      this.loading = loading
    }
  }
})