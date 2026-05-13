<template>
  <section
    class="bg-white dark:bg-slate-900/70 border border-gray-200 dark:border-slate-800 rounded-xl p-6 space-y-6 shadow-sm dark:shadow-none"
  >
    <div>
      <h2 class="text-lg font-semibold text-slate-900 dark:text-white">
        Keamanan Akun
      </h2>
      <p class="text-xs text-gray-500 dark:text-slate-400 mt-1">
        Ubah email dan kata sandi akun Anda.
      </p>
    </div>

    <form @submit.prevent="changePassword" class="space-y-4">
      <!-- Email -->
      <div class="space-y-1.5">
        <label class="text-sm font-medium text-slate-700 dark:text-slate-200"
          >Email</label
        >
        <input
          v-model="form.email"
          type="email"
          class="w-full rounded-lg bg-gray-50 dark:bg-slate-800 border border-gray-300 dark:border-slate-700 px-3 py-2 text-sm text-slate-900 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
          placeholder="email@contoh.com"
        />
      </div>

      <!-- Password sekarang -->
      <div class="space-y-1.5">
        <label class="text-sm font-medium text-slate-700 dark:text-slate-200">
          Kata Sandi Sekarang
        </label>

        <div class="relative">
          <input
            :type="showCurrentPassword ? 'text' : 'password'"
            v-model="form.currentPassword"
            class="w-full rounded-lg bg-gray-50 dark:bg-slate-800 border border-gray-300 dark:border-slate-700 px-3 py-2 pr-10 text-sm text-slate-900 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="••••••••"
          />

          <!-- Icon toggle -->
          <button
            type="button"
            @click="showCurrentPassword = !showCurrentPassword"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-slate-400"
          >
            <svg
              v-if="showCurrentPassword"
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>

            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.293-4.362M9.88 9.88a3 3 0 104.242 4.242M4.22 4.22l15.56 15.56"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Password baru -->
      <div class="space-y-1.5">
        <label class="text-sm font-medium text-slate-700 dark:text-slate-200">
          Kata Sandi Baru
        </label>

        <div class="relative">
          <input
            :type="showNewPassword ? 'text' : 'password'"
            v-model="form.newPassword"
            class="w-full rounded-lg bg-gray-50 dark:bg-slate-800 border border-gray-300 dark:border-slate-700 px-3 py-2 pr-10 text-sm text-slate-900 dark:text-slate-100 placeholder-gray-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Minimal 8 karakter"
          />

          <!-- Icon toggle -->
          <button
            type="button"
            @click="showNewPassword = !showNewPassword"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-slate-400"
          >
            <svg
              v-if="showNewPassword"
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>

            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.293-4.362M9.88 9.88a3 3 0 104.242 4.242M4.22 4.22l15.56 15.56"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Submit -->
      <div class="flex flex-col gap-3">
        <button
          type="submit"
          class="inline-flex items-center justify-center rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white hover:bg-blue-400 transition disabled:opacity-60"
          :disabled="isSaving"
        >
          <span v-if="!isSaving">Simpan Perubahan</span>
          <span v-else>Memproses...</span>
        </button>

        <p v-if="message" class="text-xs" :class="messageClass">
          {{ message }}
        </p>
      </div>

      <p
        class="border-t border-gray-200 dark:border-slate-800 pt-4 text-[11px] text-gray-500 dark:text-slate-500 leading-relaxed"
      >
        Jangan bagikan kata sandi Anda kepada siapapun.
      </p>
    </form>
  </section>
</template>

<script setup lang="ts">
import { usePasswordSettings } from "~/composables/usePassword";
import { ref } from "vue";
const showCurrentPassword = ref(false);
const showNewPassword = ref(false);

const { form, isSaving, message, messageClass, changePassword } =
  usePasswordSettings();
</script>
