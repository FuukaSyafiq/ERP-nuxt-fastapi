<!-- pages/dashboard/Laporan.vue -->
<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950 flex transition-colors duration-300"
  >
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

    <!-- KONTEN  -->
    <main class="flex-1 px-3 pt-14 pb-6 sm:px-6 sm:pt-6 lg:px-10 lg:pl-10 lg:pt-6 overflow-x-hidden">
      <div class="w-full max-w-7xl mx-auto space-y-6 sm:space-y-8">
       <!-- Header -->
        <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div class="flex items-center gap-3">
            <div>
              <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white">Laporan Keuangan</h1>
              <p class="text-gray-600 dark:text-gray-400 mt-1 text-xs sm:text-sm">
               Catat pemasukan dan pengeluaran secara otomatis dari hasil OCR nota
              </p>
            </div>
          </div>
        </header>

        <!-- ERROR HANDLER -->
        <div
          v-if="error"
          class="rounded-lg border border-red-500/40 bg-red-500/10 text-red-700 dark:text-red-200 text-sm px-4 py-3 flex items-start gap-2"
        >
          <span class="mt-0.5">⚠️</span>
          <div>
            <p class="font-semibold">Gagal memuat data</p>
            <p class="text-xs opacity-80">{{ error }}</p>
            <button
              type="button"
              class="mt-2 text-xs underline underline-offset-2"
              @click="loadReport"
            >
              Coba lagi
            </button>
          </div>
        </div>

        <!-- RINGKASAN -->
        <section class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-4 sm:p-6 space-y-4 shadow-sm dark:shadow-none">
          <h2 class="text-base sm:text-lg font-semibold text-slate-900 dark:text-white">Ringkasan Minggu Ini</h2>

          <!-- LOADING  -->
          <div v-if="isLoading" class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <div
              v-for="n in 4"
              :key="n"
              class="p-3 sm:p-4 bg-gray-100 dark:bg-slate-900/40 rounded-lg border border-gray-200 dark:border-slate-700 animate-pulse"
            >
              <div class="h-3 w-12 sm:w-16 bg-gray-300 dark:bg-slate-700 rounded mb-2"></div>
              <div class="h-4 sm:h-5 w-16 sm:w-24 bg-gray-200 dark:bg-slate-600 rounded"></div>
            </div>
          </div>

          <!-- DATA -->
          <div v-else class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            <div class="p-3 sm:p-4 bg-gray-50 dark:bg-slate-900/40 rounded-lg border border-gray-200 dark:border-slate-700">
              <p class="text-[10px] sm:text-xs text-gray-500 dark:text-slate-400">Total Omzet</p>
              <p class="text-sm sm:text-lg font-bold text-purple-600 dark:text-purple-400 truncate">
                {{ formatRupiah(summary.omzetToday) }}
              </p>
            </div>

            <div class="p-3 sm:p-4 bg-gray-50 dark:bg-slate-900/40 rounded-lg border border-gray-200 dark:border-slate-700">
              <p class="text-[10px] sm:text-xs text-gray-500 dark:text-slate-400">Total Transaksi</p>
              <p class="text-sm sm:text-lg font-bold text-purple-600 dark:text-purple-400">
                {{ summary.totalTransactions }}
              </p>
            </div>

            <div class="p-3 sm:p-4 bg-gray-50 dark:bg-slate-900/40 rounded-lg border border-gray-200 dark:border-slate-700">
              <p class="text-[10px] sm:text-xs text-gray-500 dark:text-slate-400">Total Produk</p>
              <p class="text-sm sm:text-lg font-bold text-purple-600 dark:text-purple-400">
                {{ summary.uniqueProducts }}
              </p>
            </div>

            <div class="p-3 sm:p-4 bg-gray-50 dark:bg-slate-900/40 rounded-lg border border-gray-200 dark:border-slate-700">
              <p class="text-[10px] sm:text-xs text-gray-500 dark:text-slate-400">Total Pengeluaran</p>
              <p class="text-sm sm:text-lg font-bold text-purple-600 dark:text-purple-400 truncate">
                {{ formatRupiah(summary.totalExpenses) }}
              </p>
            </div>
          </div>

          <p class="text-gray-600 dark:text-slate-400 text-xs sm:text-sm leading-relaxed">
            Laporan ini menampilkan total keseluruhan, data ini akan otomatis diperbarui setiap anda mengupload nota transaksi.
          </p>
        </section>

        <!-- GRAFIK OMZET -->
        <section class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-4 sm:p-6 space-y-4 shadow-sm dark:shadow-none">
          <div class="flex items-center justify-between gap-2">
            <h2 class="text-base sm:text-lg font-semibold text-slate-900 dark:text-white">Grafik Omzet</h2>
            <p class="text-[10px] sm:text-xs text-gray-500 dark:text-slate-400">7 hari terakhir</p>
          </div>

          <!-- LOADING STATE -->
          <div v-if="isLoadingChart" class="bg-gray-50 dark:bg-slate-900/60 border border-gray-200 dark:border-slate-700/80 rounded-lg p-4 sm:p-8">
            <div class="animate-pulse space-y-3">
              <div class="h-3 sm:h-4 bg-gray-200 dark:bg-slate-700 rounded w-3/4"></div>
              <div class="h-3 sm:h-4 bg-gray-200 dark:bg-slate-700 rounded w-1/2"></div>
              <div class="h-3 sm:h-4 bg-gray-200 dark:bg-slate-700 rounded w-5/6"></div>
            </div>
          </div>

          <!-- CHART -->
          <div v-else class="bg-gray-50 dark:bg-slate-900/60 border border-gray-200 dark:border-slate-700/80 rounded-lg p-2 sm:p-4">
            <LineChart
              :labels="chartLabels"
              :data="chartData"
              :height="200"
              label="Omzet Harian"
              :is-dark="isDark"
              border-color="rgb(147, 51, 234)"
              background-color="rgba(147, 51, 234, 0.1)"
            />
          </div>
        </section>
      </div>
    </main>
  </div>
</template>
<script setup lang="ts">
// Components (auto-imported by Nuxt, explicit for clarity)
import DashboardSidebar from "~/components/layout/Sidebar.vue";
import LineChart from "~/components/charts/LineChart.vue";

// Composables
const { isDark, toggleTheme } = useTheme();
const { isLoading, error, summary, formatRupiah, loadReport } = useFinanceReport();
const analytics = useAnalytics();

// Chart state
const isLoadingChart = ref(false);
const dailySales = ref<
  Array<{ date: string; total_sales: number; transaction_count: number }>
>([]);

// Chart data computed
const chartLabels = computed(() => {
  if (!dailySales.value.length) {
    return ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"];
  }

  return dailySales.value.map((day) => {
    const date = new Date(day.date);
    const days = ["Min", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"];
    return days[date.getDay()];
  });
});

const chartData = computed(() => {
  if (!dailySales.value.length) {
    // Dummy data jika belum ada data dari API
    return [800000, 650000, 900000, 1200000, 1500000, 1100000, 1300000];
  }

  return dailySales.value.map((day) => day.total_sales);
});

// Load chart data
const loadChartData = async () => {
  try {
    isLoadingChart.value = true;
    const data = await analytics.getDailySales(7);
    dailySales.value = data;
  } catch (err) {
    console.error("Failed to load chart data:", err);
    // Keep using dummy data on error
  } finally {
    isLoadingChart.value = false;
  }
};

onMounted(() => {
  loadReport();
  loadChartData();
});
</script>
