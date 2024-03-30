export default defineNuxtConfig({
  devtools: { 
    enabled: true 
  },
  modules: ['@nuxtjs/tailwindcss'],
  tailwindcss: {
    exposeConfig: true,
  }
})
