<template>
  <div class="inline-flex items-center gap-1 text-xs text-slate-400">
    <span>Memproses</span>
    <span class="flex gap-1">
      <span class="dot" />
      <span class="dot animation-delay-200" />
      <span class="dot animation-delay-400" />
    </span>
  </div>
</template>

<script setup>
</script>

<style scoped>
@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }

  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.dot {
  width: 4px;
  height: 4px;
  border-radius: 9999px;
  background-color: #9ca3af;
  animation: bounce 1.2s infinite ease-in-out;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}
</style>
