<template>
  <div class="min-h-screen relative overflow-hidden">
    <!-- Background Image with Fade -->
    <div class="absolute inset-0 z-0">
      <Transition name="bg-fade" mode="out-in">
        <img 
          :key="currentBg"
          :src="bgImages[currentBg]"
          :alt="'Background'"
          class="absolute inset-0 w-full h-full object-cover object-center"
        />
      </Transition>
      <!-- Dark Overlay -->
      <div class="absolute inset-0 bg-gradient-to-br from-black/70 via-black/50 to-black/70"></div>
      <!-- Gradient accent -->
      <div class="absolute inset-0 bg-gradient-to-t from-amber-900/30 via-transparent to-purple-900/20"></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 min-h-screen flex items-center justify-center p-4 sm:p-6 md:p-8">
      <div class="w-full max-w-sm sm:max-w-md">
        <!-- Glass Card -->
        <div class="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl sm:rounded-3xl p-6 sm:p-8 md:p-10 shadow-2xl shadow-black/40">
          <!-- Logo & Header -->
          <div class="text-center mb-6 sm:mb-8">
            <div class="flex justify-center mb-3 sm:mb-4">
              <img 
                src="~/assets/images/logo_warung_Ai.png" 
                alt="WarungAI Logo" 
                class="h-16 w-16 sm:h-20 sm:w-20 object-contain drop-shadow-2xl"
              />
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-white mb-1 sm:mb-2">
              Selamat Datang
            </h1>
            <p class="text-white/70 text-sm sm:text-base">Masuk ke akun WarungAI Anda</p>
            
            <!-- API Error -->
            <Transition name="slide-fade">
              <div v-if="errors.api" class="mt-4 p-3 rounded-xl bg-red-500/20 border border-red-500/30 backdrop-blur-sm">
                <p class="text-sm text-red-300">{{ errors.api }}</p>
              </div>
            </Transition>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-5">
            <!-- Email Field -->
            <div class="space-y-1.5 sm:space-y-2">
              <label class="block text-sm font-medium text-white/80">Email</label>
              <div class="relative group">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-white/50 group-focus-within:text-amber-400 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </span>
                <input 
                  v-model="form.email" 
                  type="email" 
                  placeholder="nama@email.com"
                  class="w-full pl-11 sm:pl-12 pr-4 py-3 sm:py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 text-sm sm:text-base
                         focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50 focus:bg-white/10
                         transition-all duration-300"
                />
              </div>
              <p v-if="errors.email" class="text-xs sm:text-sm text-red-400 pl-1">{{ errors.email }}</p>
            </div>

            <!-- Password Field -->
            <div class="space-y-1.5 sm:space-y-2">
              <label class="block text-sm font-medium text-white/80">Password</label>
              <div class="relative group">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-white/50 group-focus-within:text-amber-400 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </span>
                <input 
                  v-model="form.password" 
                  :type="showPassword ? 'text' : 'password'" 
                  placeholder="••••••••"
                  class="w-full pl-11 sm:pl-12 pr-11 sm:pr-12 py-3 sm:py-3.5 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/40 text-sm sm:text-base
                         focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50 focus:bg-white/10
                         transition-all duration-300"
                />
                <button 
                  type="button" 
                  @click="showPassword = !showPassword"
                  class="absolute right-3 sm:right-4 top-1/2 -translate-y-1/2 text-white/50 hover:text-white transition-colors"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
              <p v-if="errors.password" class="text-xs sm:text-sm text-red-400 pl-1">{{ errors.password }}</p>
            </div>

            <!-- Submit Button -->
            <button 
              type="submit"
              class="w-full mt-4 sm:mt-6 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 
                     text-white px-6 py-3 sm:py-4 rounded-xl font-semibold text-base sm:text-lg
                     shadow-lg shadow-amber-500/30 hover:shadow-amber-500/50
                     transform hover:scale-[1.02] active:scale-[0.98]
                     transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Memuat...
              </span>
              <span v-else>Masuk</span>
            </button>
          </form>

          <!-- Divider -->
          <div class="my-5 sm:my-6 flex items-center">
            <div class="flex-1 border-t border-white/10"></div>
            <span class="px-3 sm:px-4 text-xs sm:text-sm text-white/40">atau</span>
            <div class="flex-1 border-t border-white/10"></div>
          </div>

          <!-- Register Link -->
          <div class="text-center">
            <p class="text-white/60 text-sm sm:text-base">
              Belum punya akun?
              <NuxtLink 
                to="/auth/register" 
                class="text-amber-400 hover:text-amber-300 font-medium ml-1 hover:underline transition-colors"
              >
                Daftar sekarang
              </NuxtLink>
            </p>
          </div>
        </div>

        <!-- Back to Home -->
        <div class="mt-4 sm:mt-6 text-center">
          <NuxtLink 
            to="/" 
            class="inline-flex items-center gap-2 text-white/50 hover:text-white transition-colors text-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Kembali ke Beranda
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import penjualImg from '~/assets/images/penjual.jpg'
import penjualNgitungImg from '~/assets/images/penjual-ngitung-utang-jokowi.jpg'

const bgImages = [penjualImg, penjualNgitungImg]
const currentBg = ref(0)

// Auto-rotate background
let bgInterval = null
onMounted(() => {
  bgInterval = setInterval(() => {
    currentBg.value = (currentBg.value + 1) % bgImages.length
  }, 8000)
})

onUnmounted(() => {
  if (bgInterval) clearInterval(bgInterval)
})

const form = reactive({
  email: "",
  password: "",
});

const errors = reactive({
  email: "",
  password: "",
  api: "",
});

const isLoading = ref(false);
const showPassword = ref(false);

const handleLogin = async () => {
  errors.email = "";
  errors.password = "";
  errors.api = "";
  const { login } = useAuth();
  if (!form.email) {
    errors.email = "Email harus diisi";
    return;
  }

  if (!form.password) {
    errors.password = "Password harus diisi";
    return;
  }

  isLoading.value = true;
  const res = await login(form.email, form.password);

  isLoading.value = false;
  if (res.success) {
    navigateTo("/dashboard");
  } else {
    switch (res.status) {
      case 400:
        errors.api = res.error || "Form tidak valid, silakan periksa kembali";
        break;
      case 401:
        errors.api = "Email atau password salah";
        break;
      case 403:
        errors.api = `User dengan email ini sudah terdaftar`;
        break;
      case 404:
        errors.api = "Resource tidak ditemukan";
        break;
      case 500:
        errors.api = "Terjadi kesalahan server, silakan coba lagi nanti";
        break;
      default:
        errors.api = "Terjadi kesalahan, silakan coba lagi";
    }
  }
};
</script>

<style scoped>
/* Background fade transition */
.bg-fade-enter-active,
.bg-fade-leave-active {
  transition: opacity 1.5s ease-in-out;
}

.bg-fade-enter-from,
.bg-fade-leave-to {
  opacity: 0;
}

/* Slide fade for error messages */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
