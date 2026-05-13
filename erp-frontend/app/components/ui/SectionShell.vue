<template>
  <section :id="id" class="px-6 py-16 md:py-20">
    <div class="max-w-6xl mx-auto">
      <slot />
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{ id?: string }>()
</script>
