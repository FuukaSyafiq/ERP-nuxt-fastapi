/**
 * Composable untuk manage state sidebar (open/close)
 * Note: Di desktop (lg breakpoint), sidebar selalu visible via CSS (lg:translate-x-0)
 * State ini hanya mengontrol visibility di mobile
 */
export const useSidebar = () => {
  const isOpen = useState('sidebar-open', () => false)

  const toggleSidebar = () => {
    isOpen.value = !isOpen.value
  }

  const closeSidebar = () => {
    isOpen.value = false
  }

  const openSidebar = () => {
    isOpen.value = true
  }

  return {
    isOpen,
    toggleSidebar,
    closeSidebar,
    openSidebar,
  }
}

