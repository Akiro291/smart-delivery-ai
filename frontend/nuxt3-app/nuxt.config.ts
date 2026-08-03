export default defineNuxtConfig({
  app: {
    head: {
      title: 'Smart Delivery AI',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
    }
  },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api/v1',
    },
  },
  compatibilityDate: '2026-07-30',
  routeRules: {
    '/auth/**': { ssr: false },
    '/dashboard/**': { ssr: false },
    '/admin/**': { ssr: false },
  },
  nitro: {
    routeRules: {
      '/uploads/**': { cors: true },
    }
  },
})
