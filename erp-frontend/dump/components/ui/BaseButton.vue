<template>
  <button
    :class="[
      'inline-flex items-center justify-center font-semibold rounded-lg transition focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 focus:ring-offset-white dark:focus:ring-offset-slate-900',
      sizeClass,
      variantClass,
      block ? 'w-full' : ''
    ]"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  variant?: 'primary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  block?: boolean
}>()

const sizeClass = computed(() => ({
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-8 py-3 text-base'
}[props.size ?? 'md']))

const variantClass = computed(() => {
  switch (props.variant) {
    case 'outline':
      return 'border border-purple-600 dark:border-purple-400 text-purple-600 dark:text-purple-400 hover:bg-purple-600 dark:hover:bg-purple-400 hover:text-white'
    default:
      return 'bg-purple-600 hover:bg-purple-700 text-white'
  }
})
</script>
