<template>
    <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 flex transition-colors duration-300">
        <!-- SIDEBAR -->
        <DashboardSidebar />

    <!-- Burger Menu Button (Mobile) -->
    <CommonBurgerButton />

        <!-- Theme Toggle Button -->
        <button
          @click="toggleTheme"
          class="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50 group flex items-center gap-1.5 sm:gap-2 px-3 py-2 sm:px-4 sm:py-2.5 rounded-full 
                 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer
                 bg-slate-800/90 dark:bg-white/90 backdrop-blur-sm
                 hover:scale-105 active:scale-95"
          :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
          :title="isDark ? 'Mode Terang' : 'Mode Gelap'"
        >
          <span class="text-base sm:text-lg select-none transition-transform duration-300 group-hover:rotate-12">
            {{ isDark ? '☀️' : '🌙' }}
          </span>
          <span class="text-xs sm:text-sm font-medium text-white dark:text-slate-800 hidden sm:inline">
            {{ isDark ? 'Terang' : 'Gelap' }}
          </span>
        </button>

        <!-- Area konten -->
        <main class="flex-1 px-3 pt-14 pb-6 sm:px-6 sm:pt-6 lg:px-10 lg:pl-10 lg:pt-6 overflow-x-hidden">
            <div class="w-full max-w-7xl mx-auto space-y-6 sm:space-y-8">
                <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div class="flex items-center gap-3">
                        <div>
                            <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white">Pengaturan</h1>
                        </div>
                    </div>
                </header>

                <!-- profil + password -->
                <div class="grid gap-1 lg:grid-cols-[1fr,1fr] items-start">
                    <PasswordForm />
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import DashboardSidebar from '~/components/layout/Sidebar.vue'
import PasswordForm from '~/components/layout/PasswordForm.vue'

const { isDark, toggleTheme } = useTheme()
</script>
