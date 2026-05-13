<template>
  <footer id="Footer" class="relative border-t transition-colors duration-300"
          :class="isDark 
            ? 'bg-slate-900 border-white/10' 
            : 'bg-gradient-to-br from-amber-50 to-orange-50 border-amber-100'">
    <div class="max-w-6xl mx-auto px-6 py-14">
      <div class="grid md:grid-cols-4 gap-10">
        <!-- Brand -->
        <div class="md:col-span-2">
          <div class="flex items-center space-x-2.5 mb-5">
            <img src="~/assets/images/logo_warung_Ai.png" 
                 alt="WarungAI Logo" 
                 class="h-12 w-auto" />
            <h3 class="text-2xl font-bold"
                :class="isDark ? 'text-white' : 'text-slate-900'">
              Warung<span class="text-transparent bg-clip-text bg-gradient-to-r"
                          :class="isDark ? 'from-purple-400 to-pink-400' : 'from-amber-500 to-orange-500'">AI</span>
            </h3>
          </div>
          <p class="max-w-md leading-relaxed mb-6"
             :class="isDark ? 'text-gray-400' : 'text-slate-600'">
            Platform AI untuk membantu usaha warung dan UMKM Indonesia menjadi lebih cerdas, 
            efisien, dan menguntungkan.
          </p>
          <!-- Social links placeholder -->
          <div class="flex gap-3">
            <a v-for="social in socials" :key="social.name"
               :href="social.url"
               class="w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-300 hover:scale-110"
               :class="isDark 
                 ? 'bg-white/10 text-gray-400 hover:bg-white/20 hover:text-white' 
                 : 'bg-white text-slate-600 hover:bg-amber-500 hover:text-white shadow-sm'"
               :aria-label="social.name">
              <span class="text-lg">{{ social.icon }}</span>
            </a>
          </div>
        </div>

        <!-- Links -->
        <div>
          <h4 class="font-bold mb-5"
              :class="isDark ? 'text-white' : 'text-slate-900'">Navigasi</h4>
          <ul class="space-y-3">
            <li v-for="link in navLinks" :key="link.to">
              <NuxtLink :to="link.to" 
                        class="flex items-center gap-2 transition-colors duration-300"
                        :class="isDark 
                          ? 'text-gray-400 hover:text-white' 
                          : 'text-slate-600 hover:text-amber-600'">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h4 class="font-bold mb-5"
              :class="isDark ? 'text-white' : 'text-slate-900'">Hubungi Kami</h4>
          <ul class="space-y-3">
            <li v-for="contact in contacts" :key="contact.value"
                class="flex items-center gap-3"
                :class="isDark ? 'text-gray-400' : 'text-slate-600'">
              <span class="w-8 h-8 rounded-lg flex items-center justify-center text-sm"
                    :class="isDark ? 'bg-white/10' : 'bg-amber-100'">
                {{ contact.icon }}
              </span>
              {{ contact.value }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Copyright -->
      <div class="mt-12 pt-8 border-t flex flex-col md:flex-row justify-between items-center gap-4"
           :class="isDark ? 'border-white/10' : 'border-amber-200'">
        <p :class="isDark ? 'text-gray-500' : 'text-slate-500'">
          © {{ currentYear }} WarungAI. Dibuat dengan ❤️ di Indonesia
        </p>
        <p class="text-sm"
           :class="isDark ? 'text-gray-600' : 'text-slate-400'">
          Powered by Nuxt.js & AI
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { isDark } = useTheme()
const currentYear = new Date().getFullYear()

const navLinks = [
  { to: '/', label: 'Beranda' },
  { to: '/#features', label: 'Fitur' },
  { to: '/#about', label: 'Tentang' },
]

const contacts = [
  { icon: '📧', value: 'kanjutgusion@tim.com' },
  { icon: '📱', value: '+62 000 000 000' },
  { icon: '📍', value: 'Indonesia' },
]

const socials = [
  { name: 'Instagram', icon: '📷', url: '#' },
  { name: 'Twitter', icon: '🐦', url: '#' },
  { name: 'WhatsApp', icon: '💬', url: '#' },
]
</script>
