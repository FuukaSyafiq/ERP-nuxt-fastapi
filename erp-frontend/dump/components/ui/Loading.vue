<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div :class="spinnerClasses" class="animate-spin rounded-full border-t-transparent"></div>
    <span v-if="text" class="ml-3 text-gray-400">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg'
  text?: string
  fullscreen?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  fullscreen: false,
})

const spinnerClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-4',
    lg: 'w-12 h-12 border-4',
  }
  return [sizes[props.size], 'border-purple-500']
})

const containerClass = computed(() => 
  props.fullscreen ? 'fixed inset-0 bg-slate-900/80 backdrop-blur-sm z-50' : ''
)
</script>

