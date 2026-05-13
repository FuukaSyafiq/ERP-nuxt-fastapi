<template>
  <header class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg border-b transition-all duration-300"
          :class="isDark 
            ? 'bg-slate-900/80 border-white/10' 
            : 'bg-white/80 border-amber-100 shadow-sm'">
    <nav class="max-w-6xl mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center space-x-2.5 group">
          <img src="~/assets/images/logo_warung_Ai.png" 
               alt="WarungAI Logo" 
               class="h-10 w-auto transition-transform duration-300 group-hover:scale-110" />
          <span class="text-2xl font-bold transition-colors duration-300"
                :class="isDark ? 'text-white' : 'text-slate-900'">
            Warung<span class="text-transparent bg-clip-text bg-gradient-to-r"
                        :class="isDark ? 'from-purple-400 to-pink-400' : 'from-amber-500 to-orange-500'">AI</span>
          </span>
        </NuxtLink>

        <!-- Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <NuxtLink 
            v-for="link in navLinks" 
            :key="link.to"
            :to="link.to"
            class="font-medium transition-colors duration-300 hover:scale-105 transform"
            :class="isDark 
              ? 'text-gray-300 hover:text-white' 
              : 'text-slate-600 hover:text-amber-600'"
          >
            {{ link.label }}
          </NuxtLink>

          <!-- Login Button -->
          <NuxtLink to="/auth/login">
            <button class="px-5 py-2.5 rounded-xl font-semibold transition-all duration-300
                         hover:scale-105 active:scale-95"
                    :class="isDark 
                      ? 'bg-white text-slate-900 hover:bg-gray-100' 
                      : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-md shadow-amber-500/25 hover:shadow-lg hover:shadow-amber-500/30'">
              Masuk
            </button>
          </NuxtLink>
        </div>

        <!-- Mobile menu button -->
        <button 
          @click="isMenuOpen = !isMenuOpen"
          class="md:hidden p-2 rounded-lg transition-colors duration-300"
          :class="isDark ? 'text-white hover:bg-white/10' : 'text-slate-900 hover:bg-amber-50'"
        >
          <svg v-if="!isMenuOpen" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile menu -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-if="isMenuOpen" class="md:hidden mt-4 pb-4 space-y-4">
          <NuxtLink 
            v-for="link in navLinks" 
            :key="link.to"
            :to="link.to"
            class="block py-2 font-medium transition-colors duration-300"
            :class="isDark 
              ? 'text-gray-300 hover:text-white' 
              : 'text-slate-600 hover:text-amber-600'"
            @click="isMenuOpen = false"
          >
            {{ link.label }}
          </NuxtLink>

          <!-- Mobile Login Button -->
          <NuxtLink 
            to="/auth/login" 
            class="block"
            @click="isMenuOpen = false"
          >
            <button class="w-full px-5 py-3 rounded-xl font-semibold transition-all duration-300"
                    :class="isDark 
                      ? 'bg-white text-slate-900' 
                      : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white'">
              Masuk
            </button>
          </NuxtLink>
        </div>
      </Transition>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isMenuOpen = ref(false)
const { isDark } = useTheme()

const navLinks = [
  { to: '/#features', label: 'Fitur' },
  { to: '/#about', label: 'Tentang' },
]
</script>
