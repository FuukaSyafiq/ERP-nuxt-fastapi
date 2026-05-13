export default defineNuxtPlugin(() => {
  const { initTheme } = useTheme()
  
  // Initialize theme on client side
  initTheme()
})

