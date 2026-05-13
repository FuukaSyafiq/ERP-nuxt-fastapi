<template>
  <section class="bg-slate-900/70 border border-slate-800 rounded-xl p-6 space-y-4">
    <h2 class="text-lg font-semibold text-white">Ringkasan Akun</h2>

    <div class="space-y-3 text-sm text-slate-300">
      <p><span class="text-slate-400">Email:</span> {{ email }}</p>
      <p><span class="text-slate-400">Status Keamanan:</span> 
        <span class="text-green-400 font-medium">Aman</span>
      </p>
      <p><span class="text-slate-400">Terakhir Login:</span> 2 hari lalu</p>
    </div>

    <div class="pt-4 border-t border-slate-800 space-y-2">
      <button
        class="w-full bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
      >
        Kelola Profil
      </button>
      <button
        class="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium px-4 py-2 rounded-lg transition"
      >
        Lihat Aktivitas Login
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
const email = "email@contoh.com" 
</script>
