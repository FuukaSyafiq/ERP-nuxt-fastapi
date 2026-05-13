<template>
  <div class="lg:w-64 w-0">
    <!-- Overlay untuk mobile (backdrop) -->
    <Transition name="fade">
      <div
        v-if="isOpen"
        @click="closeSidebar"
        class="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm"
      />
    </Transition>

    <!-- Sidebar -->
    <aside
      class="fixed lg:static inset-y-0 left-0 z-50 w-64 h-screen bg-gradient-to-b from-white to-gray-50/50 dark:from-slate-950 dark:to-slate-900/50 border-r border-gray-200 dark:border-slate-800 flex flex-col transition-all duration-300 shadow-xl lg:shadow-none"
      :class="{
        'translate-x-0': isOpen,
        '-translate-x-full lg:translate-x-0': !isOpen,
      }"
    >
      <!-- Brand Header -->
      <div class="px-6 py-6 border-b border-gray-200/80 dark:border-slate-800/80">
        <div class="flex items-center justify-between">
          <!-- Logo & Brand -->
          <div class="flex items-center gap-3">
            <div class="relative">
              <img 
                src="~/assets/images/logo_warung_Ai.png" 
                alt="WarungAI Logo" 
                class="w-10 h-10 object-contain drop-shadow-lg"
              />
              <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white dark:border-slate-950 animate-pulse"></div>
            </div>
            <div class="flex flex-col">
              <h1 class="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 dark:from-purple-400 dark:to-blue-400 bg-clip-text text-transparent">
                WarungAI
              </h1>
              <p class="text-[10px] text-gray-500 dark:text-slate-400 font-medium">Smart Business</p>
            </div>
          </div>
          
          <!-- Close button untuk mobile -->
          <button
            @click="closeSidebar"
            class="lg:hidden p-2 rounded-xl hover:bg-gray-100 dark:hover:bg-slate-800 transition-all duration-200 hover:rotate-90"
            aria-label="Close sidebar"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600 dark:text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- User Info Card -->
      <div class="px-4 py-4">
        <Transition name="slide-fade" mode="out-in">
          <!-- Logged In User -->
          <div v-if="user" key="logged-in" class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border border-purple-100 dark:border-purple-800/30">
            <div class="w-9 h-9 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-semibold text-sm shadow-md">
              {{ userInitial }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 dark:text-white truncate">
                {{ user.username }}
              </p>
              <p class="text-xs text-gray-500 dark:text-slate-400 truncate">
                {{ userDisplayEmail }}
              </p>
            </div>
          </div>
          
          <!-- Guest Mode -->
          <div v-else key="guest" class="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-gradient-to-r from-gray-50 to-slate-50 dark:from-slate-900/20 dark:to-slate-800/20 border border-gray-200 dark:border-slate-800/30">
            <div class="w-9 h-9 rounded-full bg-gradient-to-br from-gray-400 to-slate-400 flex items-center justify-center text-white font-semibold text-sm shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-700 dark:text-slate-300">
                Guest Mode
              </p>
              <p class="text-xs text-gray-500 dark:text-slate-400">
                Login untuk akses penuh
              </p>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Divider -->
      <div class="px-6 pb-2">
        <div class="h-px bg-gradient-to-r from-transparent via-gray-300 dark:via-slate-700 to-transparent"></div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-2 space-y-1.5 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-slate-700 scrollbar-track-transparent">
        <!-- Navigation Label -->
        <p class="px-3 pt-2 pb-1 text-xs font-semibold text-gray-400 dark:text-slate-500 uppercase tracking-wider">
          Menu
        </p>
        
        <template v-for="item in navItems" :key="item.label">
          <!-- Logout item -->
          <button
            v-if="item.action === 'logout'"
            @click="handleNav(item)"
            class="group flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-gray-600 dark:text-slate-300 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 transition-all duration-200 hover:translate-x-1"
          >
            <component 
              :is="getIcon(item.icon)" 
              class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" 
            />
            <span>{{ item.label }}</span>
          </button>

          <!-- Normal links -->
          <NuxtLink
            v-else
            :to="item.to"
            @click="handleLinkClick"
            class="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 hover:translate-x-1"
            :class="linkClass(item.to || '/')"
          >
            <component 
              :is="getIcon(item.icon)" 
              class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" 
            />
            <span>{{ item.label }}</span>
          </NuxtLink>
        </template>
      </nav>

      <!-- Divider -->
      <div class="px-6 py-2">
        <div class="h-px bg-gradient-to-r from-transparent via-gray-300 dark:via-slate-700 to-transparent"></div>
      </div>

      <!-- Footer -->
      <div class="px-4 py-4">
        <NuxtLink
          to="/"
          @click="handleLinkClick"
          class="group flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-all duration-200 hover:scale-105"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          <span>Kembali ke Beranda</span>
        </NuxtLink>
        
        <!-- Version Info -->
        <div class="mt-3 text-center">
          <p class="text-xs text-gray-400 dark:text-slate-500">
            v1.0.0 • © 2024 WarungAI
          </p>
        </div>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { useSidebar } from '@/composables/useSidebar'

const route = useRoute()
const router = useRouter()
const { logout, user, checkAuth } = useAuth()
const { isOpen, closeSidebar } = useSidebar()
// Auto-load user data saat component mounted (jika ada token)
onMounted(async () => {
  if (!user.value) {
    await checkAuth()
  }
})

// Computed properties untuk user display
const userInitial = computed(() => {
  return user.value?.username?.[0]?.toUpperCase() || 'G'
})

const userDisplayEmail = computed(() => {
  return user.value?.email?.split('@')[0] || 'guest'
})


interface NavItem {
  to?: string
  icon: string
  label: string
  action?: string
}

const navItems: NavItem[] = [
  { 
    to: '/dashboard', 
    icon: 'chart-bar', 
    label: 'Overview' 
  },
  { 
    to: '/dashboard/AiAssistant', 
    icon: 'sparkles', 
    label: 'AI Asisten' 
  },
  { 
    to: '/dashboard/Laporan', 
    icon: 'currency-dollar', 
    label: 'Laporan Keuangan' 
  },
  { 
    to: '/dashboard/settings', 
    icon: 'cog', 
    label: 'Settings' 
  },
  { 
    icon: 'logout', 
    label: 'Logout', 
    action: 'logout' 
  },
]

const linkClass = (to: string) => {
  const isActive = route.path === to
  return isActive
    ? 'bg-gradient-to-r from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 text-purple-700 dark:text-purple-300 font-semibold shadow-sm border-l-4 border-purple-500'
    : 'text-gray-600 dark:text-slate-300 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
}

const handleNav = (item: NavItem) => {
  if (item.action === 'logout') {
    console.log("Tes")
    logout()
    checkAuth()
    // Close sidebar di mobile saja
    if (window.innerWidth < 1024) {
      closeSidebar()
    }
  } else if (item.to) {
    router.push(item.to)
    // Close sidebar di mobile saja
    if (window.innerWidth < 1024) {
      closeSidebar()
    }
  }
}

const handleLinkClick = () => {
  // Close sidebar hanya di mobile (< 1024px)
  if (window.innerWidth < 1024) {
    closeSidebar()
  }
}

// Icon mapping - returns SVG component
const getIcon = (iconName: string) => {
  const icons: Record<string, any> = {
    'chart-bar': h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      fill: 'none',
      viewBox: '0 0 24 24',
      stroke: 'currentColor',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
      })
    ]),
    'sparkles': h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      fill: 'none',
      viewBox: '0 0 24 24',
      stroke: 'currentColor',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'
      })
    ]),
    'currency-dollar': h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      fill: 'none',
      viewBox: '0 0 24 24',
      stroke: 'currentColor',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
      })
    ]),
    'cog': h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      fill: 'none',
      viewBox: '0 0 24 24',
      stroke: 'currentColor',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z'
      }),
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z'
      })
    ]),
    'logout': h('svg', {
      xmlns: 'http://www.w3.org/2000/svg',
      fill: 'none',
      viewBox: '0 0 24 24',
      stroke: 'currentColor',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1'
      })
    ]),
  }
  
  return icons[iconName] || icons['chart-bar']
}
</script>

<style scoped>
/* Fade transition untuk overlay */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide fade transition untuk user card */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Custom Scrollbar */
.scrollbar-thin {
  scrollbar-width: thin;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background: #475569;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}

/* Smooth animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

nav > * {
  animation: slideIn 0.3s ease-out backwards;
}

nav > *:nth-child(1) { animation-delay: 0.05s; }
nav > *:nth-child(2) { animation-delay: 0.1s; }
nav > *:nth-child(3) { animation-delay: 0.15s; }
nav > *:nth-child(4) { animation-delay: 0.2s; }
nav > *:nth-child(5) { animation-delay: 0.25s; }
nav > *:nth-child(6) { animation-delay: 0.3s; }
</style>
