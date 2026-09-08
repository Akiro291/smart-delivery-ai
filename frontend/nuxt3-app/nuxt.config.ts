export default defineNuxtConfig({
  app: {
    head: {
      title: 'Smart Delivery AI',
      htmlAttrs: { lang: 'ru' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'SaaS-платформа управления доставкой с AI-ассистентом, real-time трекингом и ролевым доступом' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap',
        },
      ],
    },
    pageTransition: { name: 'page', mode: 'out-in' },
  },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
      wsUrl: process.env.NUXT_PUBLIC_WS_URL || '',
    },
  },
  compatibilityDate: '2026-07-30',
  routeRules: {
    '/auth/**': { ssr: false },
    '/dashboard/**': { ssr: false },
    '/admin/**': { ssr: false },
    '/customer/**': { ssr: false },
    '/courier/**': { ssr: false },
    '/orders/**': { ssr: false },
    '/profile/**': { ssr: false },
  },
  nitro: {
    routeRules: {
      '/uploads/**': { cors: true },
    }
  },
})
