<template>
  <div
    class="relative w-full max-w-xl aspect-[16/9] rounded-2xl overflow-hidden 
           border border-gray-200 dark:border-slate-700/70 bg-white dark:bg-slate-900 
           shadow-2xl shadow-gray-400/30 dark:shadow-black/40
           animate-fade-slide animate-floating transition-colors duration-300"
  >
    <!-- Carousel Container -->
    <div class="relative w-full h-full">
      <!-- Slides -->
      <transition-group name="carousel" tag="div" class="relative w-full h-full">
        <img 
          v-for="(image, index) in images"
          v-show="currentSlide === index"
          :key="image.src"
          :src="image.src"
          :alt="image.alt"
          class="absolute inset-0 w-full h-full object-cover"
        />
      </transition-group>

      <!-- Slide Indicators -->
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-10">
        <button
          v-for="(_, index) in images"
          :key="index"
          @click="goToSlide(index)"
          class="w-2 h-2 rounded-full transition-all duration-300 cursor-pointer"
          :class="currentSlide === index 
            ? 'bg-white w-6 shadow-lg' 
            : 'bg-white/50 hover:bg-white/80'"
          :aria-label="`Go to slide ${index + 1}`"
        />
      </div>

      <!-- Progress Bar -->
      <div class="absolute bottom-0 left-0 h-1 bg-white/20 w-full">
        <div 
          class="h-full bg-gradient-to-r transition-all duration-100"
          :class="isDark ? 'from-purple-500 to-pink-500' : 'from-amber-500 to-orange-500'"
          :style="{ width: `${progress}%` }"
        />
      </div>
    </div>

    <!-- Overlay gradient -->
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent"></div>
    <div class="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-gray-200/50 dark:ring-white/5"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import penjualImg from '~/assets/images/penjual.jpg'
import penjualNgitungImg from '~/assets/images/penjual-ngitung-utang-jokowi.jpg'

const { isDark } = useTheme()

const images = [
  { src: penjualImg, alt: 'Penjual warung UMKM Indonesia' },
  { src: penjualNgitungImg, alt: 'Menghitung keuangan warung' },
]

const currentSlide = ref(0)
const progress = ref(0)
const SLIDE_DURATION = 5000 // 5 seconds per slide
const PROGRESS_INTERVAL = 50 // Update progress every 50ms

let slideInterval: ReturnType<typeof setInterval> | null = null
let progressInterval: ReturnType<typeof setInterval> | null = null

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % images.length
  progress.value = 0
}

const goToSlide = (index: number) => {
  currentSlide.value = index
  progress.value = 0
  resetTimer()
}

const startTimer = () => {
  // Progress bar timer
  progressInterval = setInterval(() => {
    progress.value += (PROGRESS_INTERVAL / SLIDE_DURATION) * 100
  }, PROGRESS_INTERVAL)

  // Slide change timer
  slideInterval = setInterval(() => {
    nextSlide()
  }, SLIDE_DURATION)
}

const resetTimer = () => {
  if (slideInterval) clearInterval(slideInterval)
  if (progressInterval) clearInterval(progressInterval)
  startTimer()
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  if (slideInterval) clearInterval(slideInterval)
  if (progressInterval) clearInterval(progressInterval)
})
</script>

<style scoped>
/* Carousel Transitions */
.carousel-enter-active,
.carousel-leave-active {
  transition: all 0.8s ease-in-out;
}

.carousel-enter-from {
  opacity: 0;
  transform: scale(1.05);
}

.carousel-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Fade Slide Animation */
@keyframes fadeSlide {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-fade-slide {
  animation: fadeSlide 0.8s ease-out forwards;
}

/* Floating Animation */
@keyframes floating {
  0% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
  100% { transform: translateY(0); }
}

.animate-floating {
  animation: floating 6s ease-in-out infinite;
}
</style>
