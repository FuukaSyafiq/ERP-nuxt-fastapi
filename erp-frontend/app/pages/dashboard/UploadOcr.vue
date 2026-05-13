<template>
  <!--  kolom -->
  <div class="grid grid-cols-1 lg:grid-cols-[2fr,1.2fr] gap-6 items-stretch">
    <!-- Upload Nota -->
    <div
      class="lg:col-span-1 bg-white dark:bg-slate-900/80 border border-gray-200 dark:border-slate-800/80 rounded-2xl overflow-hidden shadow-lg dark:shadow-[0_18px_40px_rgba(15,23,42,0.8)] flex flex-col min-w-0"
    >
      <!-- Header -->
      <div
        class="px-6 py-4 border-b border-gray-200 dark:border-slate-800 flex items-center justify-between"
      >
        <div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Upload Nota</h2>
          <p class="text-xs text-gray-500 dark:text-slate-400 mt-1">
            Upload foto nota untuk hitung omzet &amp; parsing OCR.
          </p>
        </div>
      </div>

      <!-- Body -->
      <div class="p-6 grid md:grid-cols-[1.2fr,1.5fr] gap-6 items-start flex-1">
        <!-- Form kiri -->
        <div class="space-y-4">
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onFileChange"
          />

          <!-- Status file -->
          <div
            class="text-xs text-gray-500 dark:text-slate-400 border border-dashed border-gray-300 dark:border-slate-700 rounded-xl px-4 py-3 bg-gray-50 dark:bg-slate-900/70"
          >
            <p class="font-semibold text-slate-900 dark:text-slate-100 mb-1">Status file</p>

            <p v-if="fileName" class="flex items-center gap-1">
              📄
              <span class="text-slate-800 dark:text-slate-50 font-medium truncate">{{
                fileName
              }}</span>
            </p>
            <p v-else class="italic">Belum ada file yang dipilih.</p>

            <p class="mt-2">
              Format yang didukung:
              <span class="text-slate-800 dark:text-slate-100 font-medium">JPG, PNG</span>
            </p>
          </div>

          <!-- Error -->
          <p
            v-if="uploadError"
            class="text-xs text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-950/40 border border-red-300 dark:border-red-500/40 rounded-lg px-3 py-2"
          >
            {{ uploadError }}
          </p>

          <!-- Tombol pilih -->
          <button
            type="button"
            @click="selectFile"
            class="w-full bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium px-4 py-3 rounded-lg transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isUploading"
          >
            <span v-if="!isUploading">Pilih Nota</span>
            <span v-else class="flex items-center gap-2">
              <span class="animate-pulse">• • •</span>
              Sedang mengupload...
            </span>
          </button>

          <!-- Tombol proses -->
          <button
            type="button"
            class="w-full border border-gray-300 dark:border-slate-700 text-slate-700 dark:text-slate-100 hover:bg-gray-100 dark:hover:bg-slate-800 text-xs font-medium px-4 py-2.5 rounded-lg transition disabled:opacity-40 disabled:cursor-not-allowed"
            :disabled="!selectedFile || isUploading"
            @click="handleProcess"
          >
            Upload &amp; Proses
          </button>
        </div>

        <!-- Preview Nota -->
          <div class="space-y-2">
            <p class="text-xs font-medium text-gray-600 dark:text-slate-300">Preview Nota</p>
            <div
              class="aspect-[4/3] w-full rounded-xl border border-gray-200 dark:border-slate-800 bg-gray-100 dark:bg-slate-950 flex items-center justify-center overflow-hidden relative"
            >
              <!-- Preview gambar -->
              <img
                v-if="previewUrl"
                :src="previewUrl"
                alt="Preview nota"
                class="w-full h-full object-contain"
              />

              <!-- Placeholder jika belum ada file -->
              <div
                v-else
                class="flex flex-col items-center justify-center text-gray-400 dark:text-slate-500 text-xs px-6 text-center"
              >
                <span class="text-3xl mb-2">🧾</span>
                Pilih file nota untuk melihat preview di sini.
              </div>

              <!-- Tombol exit -->
              <button
                v-if="previewUrl"
                @click="clearPreview"
                class="absolute top-2 right-2 bg-red-600 text-white text-xs px-2 py-1 rounded hover:bg-red-700"
              >
                ✕ Delete
              </button>
            </div>
          </div>

         
      </div>
    </div>

    <!--  Hasil OCR Parsing -->
    <div
      class="bg-white dark:bg-slate-900/80 border border-gray-200 dark:border-slate-800/80 rounded-2xl overflow-hidden shadow-lg dark:shadow-[0_18px_40px_rgba(15,23,42,0.7)] flex flex-col min-w-0"
    >
      <div
        class="px-6 py-4 border-b border-gray-200 dark:border-slate-800 flex items-center justify-between"
      >
        <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-50">Hasil OCR Parsing</h2>
      </div>

      <div class="p-4 space-y-3 flex-1 min-h-[260px]">
        <div
          v-if="!ocrRows.length"
          class="h-full flex items-center justify-center text-xs text-gray-500 dark:text-slate-400 italic text-center px-4"
        >
          Belum ada data OCR. Upload &amp; proses nota terlebih dahulu.
        </div>

        <div v-else class="overflow-x-auto max-h-[320px]">
          <table class="min-w-full text-xs text-slate-800 dark:text-slate-100">
            <thead class="bg-gray-100 dark:bg-slate-900/90 sticky top-0">
              <tr class="text-left border-b border-gray-200 dark:border-slate-800">
                <th class="py-2 pr-4 font-semibold">Produk</th>
                <th class="py-2 pr-4 font-semibold">Qty</th>
                <th class="py-2 pr-4 font-semibold">Harga</th>
                <th class="py-2 pr-4 text-right font-semibold">Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in ocrRows"
                :key="row.id"
                class="border-b border-gray-200 dark:border-slate-800/80 last:border-0"
              >
                <td class="py-2 pr-4">{{ row.name}}</td>
                <td class="py-2 pr-4">{{ row.qty }}</td>
                <td class="py-2 pr-4">{{ formatRupiah(row.price) }}</td>
                <td class="py-2 pr-4 text-right">
                  {{ formatRupiah(row.total) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useOcrUpload } from "~/composables/useOcrUpload";

const emit = defineEmits<{
  "ocr-parsed": [rows: OcrRow[]];
}>();

const props = defineProps<{
  ocrRows: OcrRow[];
  formatRupiah: (amount: number) => string;
}>();

const {
  fileInput,
  selectedFile,
  previewUrl,
  fileName,
  isUploading,
  uploadError,
  selectFile,
  onFileChange,
  processUpload,
} = useOcrUpload();
// Fungsi untuk menghapus preview
const clearPreview = () => {
  previewUrl.value = "";
  selectedFile.value = null;
  fileName.value = "";
  if (fileInput.value) fileInput.value.value = ""; // reset input
};

const handleProcess = async () => {
  processUpload((rows) => emit("ocr-parsed", rows));
};
</script>
