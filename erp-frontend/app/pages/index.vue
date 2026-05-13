<template>
  <div class="min-h-screen relative overflow-hidden transition-colors duration-500"
       :class="isDark 
         ? 'bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950' 
         : 'bg-gradient-to-br from-amber-50 via-orange-50/30 to-white'">
    
    <!-- Decorative Background Pattern -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Geometric Pattern inspired by Batik -->
      <div class="absolute top-0 left-0 w-full h-full batik-pattern"
           :class="isDark ? 'opacity-[0.02]' : 'opacity-[0.04]'">
      </div>
      
      <!-- Floating Decorative Circles -->
      <div class="absolute -top-24 -right-24 w-96 h-96 rounded-full blur-3xl"
           :class="isDark ? 'bg-purple-500/10' : 'bg-amber-300/30'"></div>
      <div class="absolute top-1/2 -left-32 w-72 h-72 rounded-full blur-3xl"
           :class="isDark ? 'bg-pink-500/10' : 'bg-orange-200/40'"></div>
      <div class="absolute -bottom-32 right-1/4 w-80 h-80 rounded-full blur-3xl"
           :class="isDark ? 'bg-indigo-500/10' : 'bg-yellow-200/30'"></div>
    </div>

    <!-- Theme Toggle Button - Bottom Right FAB -->
    <button
      @click="toggleTheme"
      class="fixed bottom-6 right-6 z-50 group flex items-center gap-2.5 px-5 py-3 rounded-2xl 
             shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer
             border backdrop-blur-md
             hover:scale-105 active:scale-95"
      :class="isDark 
        ? 'bg-white/90 border-white/20 hover:bg-white' 
        : 'bg-slate-900/90 border-slate-800 hover:bg-slate-900'"
      :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      :title="isDark ? 'Mode Terang' : 'Mode Gelap'"
    >
      <span class="text-xl select-none transition-transform duration-500 group-hover:rotate-[360deg]">
        {{ isDark ? '☀️' : '🌙' }}
      </span>
      <span class="text-sm font-semibold hidden sm:inline"
            :class="isDark ? 'text-slate-800' : 'text-white'">
        {{ isDark ? 'Terang' : 'Gelap' }}
      </span>
    </button>

    <!-- HEADER / NAV -->
    <LandingHeader />
    
    <!-- HERO SECTION -->
    <SectionShell class="relative z-10">
      <div class="grid md:grid-cols-2 gap-12 lg:gap-16 items-center">
        <div class="text-center md:text-left space-y-6 lg:space-y-8 pt-6 md:pt-10"
             style="animation: fadeInUp 0.8s ease-out">
          
          <!-- Badge -->
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full border
                      transition-colors duration-300"
               :class="isDark 
                 ? 'bg-white/5 border-white/10 text-gray-300' 
                 : 'bg-amber-100/80 border-amber-200 text-amber-800'">
            <span class="flex h-2 w-2 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
                    :class="isDark ? 'bg-purple-400' : 'bg-amber-500'"></span>
              <span class="relative inline-flex rounded-full h-2 w-2"
                    :class="isDark ? 'bg-purple-500' : 'bg-amber-600'"></span>
            </span>
            <span class="text-xs font-semibold uppercase tracking-wider">
              Platform AI untuk Warung & UMKM
            </span>
          </div>

          <!-- Main Heading -->
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight tracking-tight">
            <span :class="isDark ? 'text-white' : 'text-slate-900'">
              Kelola Warung
            </span>
            <br />
            <span class="relative inline-block">
              <span class="text-transparent bg-clip-text bg-gradient-to-r"
                    :class="isDark 
                      ? 'from-purple-400 via-pink-400 to-amber-400' 
                      : 'from-amber-600 via-orange-500 to-pink-500'">
                Lebih Cerdas
              </span>
              <!-- Underline decoration -->
              <svg class="absolute -bottom-2 left-0 w-full h-3" viewBox="0 0 200 12" preserveAspectRatio="none">
                <path d="M0,8 Q50,0 100,8 T200,8" fill="none" 
                      :stroke="isDark ? '#a855f7' : '#f59e0b'" 
                      stroke-width="3" stroke-linecap="round"/>
              </svg>
            </span>
          </h1>

          <!-- Description -->
          <p class="text-lg md:text-xl max-w-xl mx-auto md:mx-0 leading-relaxed"
             :class="isDark ? 'text-gray-300' : 'text-slate-600'">
            Dari <strong>nota fisik</strong> ke <strong>laporan digital</strong> dalam hitungan detik. 
            Pantau omzet, analisis penjualan, dan dapat rekomendasi AI — 
            <span class="font-semibold" :class="isDark ? 'text-amber-400' : 'text-amber-600'">100% GRATIS</span>
          </p>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start pt-2">
            <NuxtLink to="/auth/login">
              <button class="group relative px-8 py-4 rounded-xl font-bold text-lg overflow-hidden
                           transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl
                           active:scale-[0.98]"
                      :class="isDark 
                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg shadow-purple-500/25' 
                        : 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-amber-500/30'">
                <span class="relative z-10 flex items-center gap-2">
                  Mulai Gratis
                  <svg class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </button>
            </NuxtLink>

            <NuxtLink to="#features">
              <button class="px-8 py-4 rounded-xl font-semibold text-lg border-2 
                           transition-all duration-300 hover:shadow-lg"
                      :class="isDark 
                        ? 'border-white/20 text-white hover:bg-white/10 hover:border-white/30' 
                        : 'border-slate-300 text-slate-700 hover:bg-slate-50 hover:border-slate-400'">
                Lihat Fitur
              </button>
            </NuxtLink>
          </div>

          <!-- Trust Indicators -->
          <div class="flex flex-wrap items-center gap-6 justify-center md:justify-start pt-4">
            <div class="flex items-center gap-2">
              <div class="flex -space-x-2">
                <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                     :class="isDark ? 'bg-purple-600 border-slate-900 text-white' : 'bg-amber-500 border-white text-white'">W</div>
                <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                     :class="isDark ? 'bg-pink-600 border-slate-900 text-white' : 'bg-orange-500 border-white text-white'">K</div>
                <div class="w-8 h-8 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                     :class="isDark ? 'bg-indigo-600 border-slate-900 text-white' : 'bg-red-500 border-white text-white'">T</div>
              </div>
              <span class="text-sm" :class="isDark ? 'text-gray-400' : 'text-slate-500'">
                <strong :class="isDark ? 'text-white' : 'text-slate-900'">500+</strong> UMKM aktif
              </span>
            </div>
            <div class="flex items-center gap-1.5">
              <div class="flex text-amber-400">
                <svg v-for="i in 5" :key="i" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <span class="text-sm" :class="isDark ? 'text-gray-400' : 'text-slate-500'">
                <strong :class="isDark ? 'text-white' : 'text-slate-900'">4.9</strong> rating
              </span>
            </div>
          </div>
        </div>

        <!-- PREVIEW DASHBOARD -->
        <div class="hidden md:flex justify-end relative"
             style="animation: fadeInRight 0.8s ease-out 0.2s both">
          <HeroPreview />
          <!-- Decorative badge -->
          <div class="absolute -bottom-4 -left-4 px-4 py-2 rounded-xl shadow-lg backdrop-blur-sm
                      border animate-bounce-slow"
               :class="isDark 
                 ? 'bg-slate-800/90 border-slate-700 text-white' 
                 : 'bg-white/90 border-amber-200 text-slate-900'">
            <div class="flex items-center gap-2">
              <span class="text-2xl">🚀</span>
              <div>
                <p class="text-xs font-medium" :class="isDark ? 'text-gray-400' : 'text-slate-500'">Omzet Hari Ini</p>
                <p class="text-sm font-bold" :class="isDark ? 'text-green-400' : 'text-green-600'">+Rp 2.450.000</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </SectionShell>

    <!-- FEATURES SECTION -->
    <SectionShell id="features" class="relative z-10">
      <SectionTitle>
        <template #title>
          <span :class="isDark ? 'text-white' : 'text-slate-900'">Fitur</span>
          <span class="text-transparent bg-clip-text bg-gradient-to-r"
                :class="isDark ? 'from-purple-400 to-pink-400' : 'from-amber-500 to-orange-500'">
            Unggulan
          </span>
        </template>
        <template #subtitle>
          Semua yang Anda butuhkan untuk mengelola usaha kecil, dari nota sampai laporan keuangan.
        </template>
      </SectionTitle>

      <div class="grid md:grid-cols-3 gap-6 lg:gap-8">
        <FeatureCard 
          v-for="(feature, index) in features" 
          :key="feature.title"
          :icon="feature.icon"
          :title="feature.title"
          :description="feature.description"
          :color="feature.color"
          :delay="index * 100"
        />
      </div>
    </SectionShell>

    <!-- STATS SECTION -->
    <SectionShell class="relative z-10">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <div v-for="(stat, index) in stats" :key="stat.label"
             class="text-center p-6 rounded-2xl border transition-all duration-300 hover:scale-105"
             :class="isDark 
               ? 'bg-white/5 border-white/10 hover:bg-white/10' 
               : 'bg-white/80 border-amber-100 hover:shadow-lg hover:shadow-amber-100'"
             :style="{ animationDelay: `${index * 100}ms` }">
          <div class="text-3xl md:text-4xl font-extrabold mb-1"
               :class="isDark ? 'text-white' : stat.colorClass">
            {{ stat.value }}
          </div>
          <div class="text-sm font-medium"
               :class="isDark ? 'text-gray-400' : 'text-slate-600'">
            {{ stat.label }}
          </div>
        </div>
      </div>
    </SectionShell>

    <!-- ABOUT SECTION -->
    <SectionShell id="about" class="relative z-10">
      <div class="max-w-3xl mx-auto text-center">
        <div class="flex items-center justify-center w-full rounded-2xl mb-6 p-8
                    transition-colors duration-300"
             :class="isDark ? 'bg-purple-500/20' : 'bg-amber-100'">
          <img src="~/assets/images/logo_warung_Ai.png" alt="WarungAI Logo" class="w-32 h-32 object-contain" />
        </div>
        <h2 class="text-3xl md:text-4xl font-bold mb-6"
            :class="isDark ? 'text-white' : 'text-slate-900'">
          Tentang <span class="text-transparent bg-clip-text bg-gradient-to-r"
                        :class="isDark ? 'from-purple-400 to-pink-400' : 'from-amber-500 to-orange-500'">
            WarungAI
          </span>
        </h2>
        <p class="text-lg leading-relaxed mb-8"
           :class="isDark ? 'text-gray-300' : 'text-slate-600'">
          WarungAI adalah solusi digital yang dirancang khusus untuk <strong>UMKM Indonesia</strong>. 
          Kami memahami tantangan yang dihadapi warung, kios, dan toko kelontong dalam mengelola 
          keuangan sehari-hari. Dengan teknologi AI yang mudah digunakan, kami membantu Anda 
          mengubah <strong>nota kertas</strong> menjadi <strong>insight bisnis</strong> yang berharga.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <div v-for="tag in aboutTags" :key="tag"
               class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-300"
               :class="isDark 
                 ? 'bg-white/10 text-gray-300' 
                 : 'bg-amber-100 text-amber-800'">
            {{ tag }}
          </div>
        </div>
      </div>
    </SectionShell>

    <!-- FOOTER -->
    <LandingFooter />
  </div>
</template>

<script setup lang="ts">
import LandingHeader from '~/components/layout/Header.vue'
import LandingFooter from '~/components/layout/Footer.vue'
import HeroPreview from '~/components/ui/Preview.vue'
import SectionShell from '~/components/ui/SectionShell.vue'
import SectionTitle from '~/components/ui/SectionTitle.vue'
import FeatureCard from '~/components/ui/FeatureCard.vue'

const { isDark, toggleTheme } = useTheme()

const features = [
  {
    icon: 'chart' as const,
    title: 'Analisis Penjualan',
    description: 'Pantau penjualan harian, produk terlaris, dan tren omzet setiap hari secara real-time.',
    color: 'blue' as const
  },
  {
    icon: 'robot' as const,
    title: 'AI Assistant',
    description: 'Dapatkan rekomendasi harga optimal dan saran untuk meningkatkan keuntungan bisnis Anda.',
    color: 'purple' as const
  },
  {
    icon: 'money' as const,
    title: 'Laporan Keuangan',
    description: 'Catat pemasukan dan pengeluaran secara otomatis dari nota yang diunggah.',
    color: 'green' as const
  }
]

const stats = [
  { value: '500+', label: 'UMKM Aktif', colorClass: 'text-amber-600' },
  { value: '50K+', label: 'Nota Diproses', colorClass: 'text-orange-600' },
  { value: '99%', label: 'Akurasi AI', colorClass: 'text-green-600' },
  { value: '24/7', label: 'Dukungan', colorClass: 'text-purple-600' }
]

const aboutTags = [
  '🇮🇩 Buatan Indonesia',
  '🔒 Data Aman',
  '📱 Mobile Friendly',
  '🆓 Gratis Selamanya'
]

useHead({
  title: 'WarungAI - Platform AI untuk Warung & UMKM Indonesia',
  meta: [
    {
      name: 'description',
      content: 'Platform AI gratis untuk membantu warung, kios, dan toko kelontong mengelola nota, pantau omzet, dan analisis penjualan dengan mudah.',
    },
  ],
})
</script>

<style scoped>
.batik-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23d97706' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-bounce-slow {
  animation: bounce-slow 3s infinite;
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
