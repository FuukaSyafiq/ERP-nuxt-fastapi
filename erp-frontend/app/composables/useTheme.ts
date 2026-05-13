export const useTheme = () => {
  const isDark = useState<boolean>('theme-is-dark', () => false)

  const applyTheme = () => {
    if (import.meta.client) {
      if (isDark.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  }

  const initTheme = () => {
    if (import.meta.client) {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        isDark.value = savedTheme === 'dark'
      } else {
        // Default to light mode
        isDark.value = false
        localStorage.setItem('theme', 'light')
      }
      applyTheme()
    }
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    if (import.meta.client) {
      localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
      applyTheme()
    }
  }

  // Watch for changes
  watch(isDark, () => {
    applyTheme()
  })

  return {
    isDark,
    toggleTheme,
    initTheme
  }
}
