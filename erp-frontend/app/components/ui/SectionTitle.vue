<template>
  <div class="text-center mb-10 md:mb-14"
       style="animation: fadeInUp 0.6s ease-out">
    <h2 class="text-3xl md:text-4xl font-bold mb-4 flex flex-wrap items-center justify-center gap-2">
      <slot name="title" />
    </h2>
    <p v-if="$slots.subtitle" 
       class="text-lg max-w-2xl mx-auto leading-relaxed transition-colors duration-300"
       :class="isDark ? 'text-gray-400' : 'text-slate-600'">
      <slot name="subtitle" />
    </p>
  </div>
</template>

<script setup lang="ts">
const { isDark } = useTheme()
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
