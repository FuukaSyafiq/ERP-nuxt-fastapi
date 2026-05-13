<template>
  <div class="flex flex-wrap gap-2">
    <button v-for="item in items" :key="item" type="button"
      class="px-3 py-1 rounded-full bg-slate-800/80 text-xs text-slate-200 hover:bg-slate-700 hover:text-white transition border border-slate-700"
      @click="$emit('select', item)">
      {{ item }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['select'])
</script>
