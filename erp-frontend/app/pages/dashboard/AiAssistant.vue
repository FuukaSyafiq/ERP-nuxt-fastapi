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
      class="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-50 group flex items-center gap-1.5 sm:gap-2 px-3 py-2 sm:px-4 sm:py-2.5 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer bg-slate-800/90 dark:bg-white/90 backdrop-blur-sm hover:scale-105 active:scale-95"
      :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
      :title="isDark ? 'Mode Terang' : 'Mode Gelap'"
    >
      <span
        class="text-base sm:text-lg select-none transition-transform duration-300 group-hover:rotate-12"
      >
        {{ isDark ? "☀️" : "🌙" }}
      </span>
      <span
        class="text-xs sm:text-sm font-medium text-white dark:text-slate-800 hidden sm:inline"
      >
        {{ isDark ? "Terang" : "Gelap" }}
      </span>
    </button>

    <main class="flex-1 px-3 pt-14 pb-6 sm:px-6 sm:pt-6 lg:px-10 lg:pl-10 lg:pt-6 overflow-x-hidden">
      <div class="w-full max-w-7xl mx-auto space-y-6 sm:space-y-8">
        <!-- Header -->
        <header class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div class="flex items-center gap-3">
            <div
              class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl sm:rounded-2xl bg-purple-600/20 flex items-center justify-center text-xl sm:text-2xl"
            >
              🤖
            </div>
            <div>
              <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white">
                AI Asisten
              </h1>
              <p class="text-gray-600 dark:text-gray-400 mt-1 text-xs sm:text-sm">
                Dapatkan rekomendasi harga optimal berdasarkan data penjualan
                dan kompetitor.
              </p>
            </div>
          </div>
        </header>

        <!-- Main content -->
        <section
          class="bg-white dark:bg-slate-900/80 border border-gray-200 dark:border-white/5 rounded-2xl p-6 shadow-lg dark:shadow-xl space-y-5"
        >
          <div
            class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between"
          >
            <div>
              <h2
                class="text-base font-semibold text-slate-900 dark:text-white"
              >
              Atur Margin Untuk Product Anda & Dapatkan Harga Terbaik
              </h2>
              <p
                class="text-xs text-gray-500 dark:text-slate-400 mt-1 max-w-md"
              >
              Tentukan margin yang Anda inginkan. AI akan menghitung harga optimal beserta alasannya.
              </p>
            </div>
          </div>

          <!-- layout -->
          <div class="grid grid-cols-1 lg:grid-cols-[1.7fr,2fr] gap-6">
            <!-- Form input -->
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-1">
                  <label class="text-xs text-gray-600 dark:text-slate-300">
                    Target margin (%)
                  </label>
                  <input
                    v-model.number="marginForRecommendedProduct"
                    type="number"
                    min="0"
                    class="w-full rounded-xl bg-gray-50 dark:bg-slate-950/80 border border-gray-300 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="20"
                  />
                </div>
              </div>

              <div class="pt-2">
                <button
                  class="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-sm font-medium text-white transition disabled:opacity-50 disabled:cursor-not-allowed"
                  :disabled="!canSubmitRecommendedProduct || isLoadingRecommend"
                  @click="requestRecommendationProduct"
                >
                  <span v-if="!isLoadingRecommend">Dapatkan harga optimal</span>
                  <span v-else class="flex items-center gap-2">
                    <LoadingDots />
                  </span>
                </button>
              </div>

             

              <p v-if="errorRecommend" class="text-xs text-red-400">
                {{ errorRecommend }}
              </p>
            </div>

            <!-- Output rekomendasi -->
            <div class="space-y-3">
              <div
                class="min-h-[220px] rounded-xl bg-gray-50 dark:bg-slate-950/80 border border-gray-200 dark:border-slate-700 px-4 py-4 text-sm text-slate-900 dark:text-slate-100 flex flex-col justify-between"
              >
                <div class="space-y-4">
                  <template v-if="isLoadingRecommend">
                    <p class="text-xs text-gray-500 dark:text-slate-400 mb-1">
                      Menganalisis harga dan produk terbaik...
                    </p>
                    <LoadingDots />
                  </template>

                  <template
                    v-else-if="
                      recommendationPriceState &&
                      recommendationPriceState.length > 0
                    "
                  >
                    <div
                      v-for="(product, index) in recommendationPriceState"
                      :key="index"
                      class="mb-4"
                    >
                      <!-- Harga rekomendasi -->
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Produk
                        </p>
                        <p
                          class="text-sm font-semibold text-slate-900 dark:text-white"
                        >
                          {{ product.item_name }}
                        </p>
                      </div>

                      <!-- Harga saat ini -->
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Harga saat ini
                        </p>
                        <p
                          class="text-lg font-medium text-gray-700 dark:text-gray-200"
                        >
                          {{ formatCurrency(product.current_price ?? 0) }}
                        </p>
                      </div>

                      <!-- Harga rekomendasi -->
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Harga rekomendasi
                        </p>
                        <p
                          class="text-2xl font-semibold text-emerald-600 dark:text-emerald-400"
                        >
                          {{ formatCurrency(product.recommended_price ?? 0) }}
                        </p>
                        <p
                          class="text-[11px] text-gray-500 dark:text-slate-500 mt-1"
                        >
                          Target marginmu {{ product.expected_margin ?? 0 }}%
                        </p>
                      </div>

                      <!-- Alasan -->
                      <div>
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400 mb-1"
                        >
                          Alasan
                        </p>
                        <p
                          class="text-xs text-slate-700 dark:text-slate-100 leading-relaxed"
                        >
                          {{ product.reasoning }}
                        </p>
                      </div>
                    </div>
                  </template>

                  <template v-else>
                    <p class="text-gray-500 dark:text-slate-500 text-xs">
                      Belum ada analisis.
                    </p>
                    <ul
                      class="mt-3 text-xs text-gray-500 dark:text-slate-400 list-disc list-inside space-y-1"
                    >
                      <li>Harga rekomendasi yang tetap untung.</li>
                      <li>Margin rekomendasi.</li>
                      <li>Alasan.</li>
                    </ul>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section
          class="bg-white dark:bg-slate-900/80 border border-gray-200 dark:border-white/5 rounded-2xl p-6 shadow-lg dark:shadow-xl space-y-5"
        >
          <div
            class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between"
          >
            <div>
              <h2
                class="text-base font-semibold text-slate-900 dark:text-white"
              >
                Dapatkan Harga Optimal Dari Produk Anda
              </h2>
              <p
                class="text-xs text-gray-500 dark:text-slate-400 mt-1 max-w-md"
              >
                Pilih data produk anda dan margin yang diinginkan. AI akan
                membantu memberikan rekomendasi harga, dan alasan.
              </p>
            </div>
          </div>

          <!-- layout -->
          <div class="grid grid-cols-1 lg:grid-cols-[1.7fr,2fr] gap-6">
            <!-- Form input -->
            <div class="space-y-4">
              <div class="space-y-1">
                <label class="text-xs text-gray-600 dark:text-slate-300"
                  >Nama produk</label
                >
                <select
                  v-model="productName"
                  class="w-full rounded-xl bg-gray-50 dark:bg-slate-950/80 border border-gray-300 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  style="max-height: 160px; overflow-y: auto"
                >
                  <option disabled value="">Pilih produk…</option>

                  <option
                    v-for="(item, i) in productsName"
                    :key="i"
                    :value="item"
                  >
                    {{ item }}
                  </option>
                </select>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="space-y-1">
                  <label class="text-xs text-gray-600 dark:text-slate-300">
                    Target margin (%)
                  </label>
                  <input
                    v-model.number="marginPercent"
                    type="number"
                    min="0"
                    class="w-full rounded-xl bg-gray-50 dark:bg-slate-950/80 border border-gray-300 dark:border-slate-700 text-sm text-slate-900 dark:text-slate-100 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="20"
                  />
                </div>
              </div>
              <div class="flex items-center justify-between pt-2">
              
                <button
                  class="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-sm font-medium text-white transition disabled:opacity-50 disabled:cursor-not-allowed"
                  :disabled="!canSubmit || isLoading"
                  @click="requestRecommendationPriceByProduct"
                >
                  <span v-if="!isLoading">Dapatkan harga optimal</span>
                  <span v-else class="flex items-center gap-2">
                    <LoadingDots />
                  </span>
                </button>
              </div>

              <p v-if="error" class="text-xs text-red-400">
                {{ error }}
              </p>
            </div>

            <!-- Output rekomendasi -->
            <div class="space-y-3">
              <div
                class="min-h-[220px] rounded-xl bg-gray-50 dark:bg-slate-950/80 border border-gray-200 dark:border-slate-700 px-4 py-4 text-sm text-slate-900 dark:text-slate-100 flex flex-col justify-between"
              >
                <div class="space-y-4">
                  <template v-if="isLoading">
                    <p class="text-xs text-gray-500 dark:text-slate-400 mb-1">
                      Menganalisis harga terbaik…
                    </p>
                    <LoadingDots />
                  </template>

                  <template v-if="recommendationPriceByItemState">
                    <div>
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Produk
                        </p>
                        <p
                          class="text-sm font-semibold text-slate-900 dark:text-white"
                        >
                          {{ recommendationPriceByItemState.item_name ?? "-" }}
                        </p>
                      </div>

                      <!-- Harga saat ini -->
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Harga saat ini
                        </p>
                        <p
                          class="text-lg font-medium text-gray-700 dark:text-gray-200"
                        >
                          {{
                            formatCurrency(
                              Number(
                                recommendationPriceByItemState.current_price ??
                                  0
                              )
                            )
                          }}
                        </p>
                      </div>

                      <!-- Harga rekomendasi -->
                      <div class="mb-2">
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400"
                        >
                          Harga rekomendasi
                        </p>
                        <p
                          class="text-2xl font-semibold text-emerald-600 dark:text-emerald-400"
                        >
                          {{
                            formatCurrency(
                              Number(
                                recommendationPriceByItemState.recommended_price ??
                                  0
                              )
                            )
                          }}
                        </p>
                        <p
                          class="text-[11px] text-gray-500 dark:text-slate-500 mt-1"
                        >
                          Target marginmu
                          {{
                            recommendationPriceByItemState.expected_margin ?? 0
                          }}%
                        </p>
                      </div>

                      <!-- Alasan -->
                      <div>
                        <p
                          class="text-[11px] uppercase tracking-wide text-gray-500 dark:text-slate-400 mb-1"
                        >
                          Alasan
                        </p>
                        <p
                          class="text-xs text-slate-700 dark:text-slate-100 leading-relaxed"
                        >
                          {{ recommendationPriceByItemState.reasoning ?? "-" }}
                        </p>
                      </div>
                    </div>
                  </template>

                  <template v-else-if="recommendationPriceByItemState == null && !isLoading">
                    <p class="text-gray-500 dark:text-slate-500 text-xs">
                      Belum ada analisis.
                    </p>
                    <ul
                      class="mt-3 text-xs text-gray-500 dark:text-slate-400 list-disc list-inside space-y-1"
                    >
                      <li>Harga rekomendasi yang tetap untung.</li>
                      <li>Margin rekomendasi.</li>
                      <li>Alasan promo.</li>
                    </ul>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>
<script setup lang="ts">
import { ref, computed } from "vue";
import DashboardSidebar from "~/components/layout/Sidebar.vue";
import LoadingDots from "~/components/ui/LoadingDots.vue";
import { useRecommendation } from "~/composables/useRecommendation";
import { useTheme } from "~/composables/useTheme.ts";
const {
  recommendationPriceByItem,
  recommendationPrice,
  recommendationPriceState,
  recommendationPriceByItemState,
} = useRecommendation();
const { getTopItems } = useAnalytics();
// -----------------------------
// Theme
// -----------------------------
const { isDark, toggleTheme } = useTheme();

// -----------------------------
// Form State
// -----------------------------
const productName = ref("");
const marginPercent = ref<number | null>(null);
const marginForRecommendedProduct = ref<number | null>(null);

// -----------------------------
// Result & UI State
// -----------------------------
const isLoading = ref(false);
const error = ref("");

const isLoadingRecommend = ref(false);
const errorRecommend = ref("");

// -----------------------------
// Computed
// -----------------------------
const canSubmit = computed(() => {
  return (
    productName.value.trim() !== "" &&
    marginPercent.value !== null &&
    marginPercent.value >= 0
  );
});

const canSubmitRecommendedProduct = computed(() => {
  return (
    marginForRecommendedProduct.value !== null &&
    marginForRecommendedProduct.value >= 0
  );
});

// -----------------------------
// Methods
// -----------------------------
const requestRecommendationPriceByProduct = async () => {
  if (!canSubmit.value) return;

  isLoading.value = true;
  error.value = "";
  recommendationPriceByItemState.value = null;
  try {
    // const result = await recommendationPrice(marginPercent.value!);
    const result = await recommendationPriceByItem(
      productName.value,
      marginPercent.value!
    );
    if (!result.success) {
      error.value = result.error; // <-- assign error dari API
      return;
    }
  } catch (err: any) {
    console.log(err);
    error.value = err.error || "Terjadi kesalahan";
  } finally {
    isLoading.value = false;
  }
};

const requestRecommendationProduct = async () => {
  if (!canSubmitRecommendedProduct.value) return;

  isLoadingRecommend.value = true;
  errorRecommend.value = "";
  recommendationPriceState.value = [];
  try {
    // const result = await recommendationPrice(marginPercent.value!);
    const result = await recommendationPrice(
      marginForRecommendedProduct.value!
    );
    if (!result.success) {
      errorRecommend.value = result.error; // <-- assign error dari API
      return;
    }
  } catch (err: any) {
    errorRecommend.value = err.error || "Terjadi kesalahan";
  } finally {
    isLoadingRecommend.value = false;
  }
};
// -----------------------------
// Helper
// -----------------------------
const formatCurrency = (value: number) => {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
  }).format(value);
};
const productsName = ref<string[]>([]);

onMounted(async () => {
  const result = await getTopItems();

  // Pastikan result itu array
  if (Array.isArray(result)) {
    productsName.value = result.map((item) => item.name);
  }
});
</script>
