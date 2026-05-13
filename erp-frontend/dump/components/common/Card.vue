<template>
  <div :class="cardClasses">
    <div v-if="$slots.header" class="px-6 py-4 border-b border-white/10">
      <slot name="header" />
    </div>

    <div class="p-6">
      <slot />
    </div>

    <div v-if="$slots.footer" class="px-6 py-4 border-t border-white/10">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'glass'
  hover?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  hover: false,
})

const base =
  'rounded-xl border border-white/10 text-white overflow-hidden'

const variants: Record<NonNullable<Props['variant']>, string> = {
  default: 'bg-slate-900/80',
  glass: 'bg-white/10 backdrop-blur-sm',
}

const hoverEffect = computed(() =>
  props.hover ? 'hover:bg-white/20 transition-colors cursor-pointer' : ''
)

const cardClasses = computed(
  () => `${base} ${variants[props.variant!]} ${hoverEffect.value}`.trim()
)
</script>
