<template>
  <div 
    class="group relative p-8 rounded-2xl border transition-all duration-500 
           hover:scale-[1.02] hover:-translate-y-1"
    :class="cardClasses"
    :style="{ animationDelay: `${delay}ms` }"
  >
    <!-- Icon Container -->
    <div class="w-14 h-14 rounded-xl flex items-center justify-center mb-6 
                transition-all duration-300 group-hover:scale-110"
         :class="iconClasses">
      <!-- Chart Icon -->
      <svg v-if="icon === 'chart'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
      </svg>
      
      <!-- Robot Icon -->
      <svg v-else-if="icon === 'robot'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
      </svg>
      
      <!-- Money Icon -->
      <svg v-else-if="icon === 'money'" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
      </svg>
      
      <!-- Default slot for custom icons -->
      <slot v-else name="icon" />
    </div>
    
    <!-- Title -->
    <h3 class="text-xl font-bold mb-3 transition-colors duration-300"
        :class="titleClasses">
      {{ title }}
      <slot v-if="!title" name="title" />
    </h3>
    
    <!-- Description -->
    <p class="leading-relaxed transition-colors duration-300"
       :class="descriptionClasses">
      {{ description }}
      <slot v-if="!description" name="description" />
    </p>

    <!-- Decorative corner gradient -->
    <div class="absolute top-0 right-0 w-24 h-24 opacity-0 group-hover:opacity-100 
                transition-opacity duration-500 pointer-events-none overflow-hidden rounded-tr-2xl">
      <div class="absolute -top-12 -right-12 w-24 h-24 rounded-full blur-2xl"
           :class="glowClasses"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  icon?: 'chart' | 'robot' | 'money' | string
  title?: string
  description?: string
  color?: 'blue' | 'purple' | 'green' | 'amber' | 'orange'
  delay?: number
}>()

const { isDark } = useTheme()

const cardClasses = computed(() => {
  if (isDark.value) {
    return 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20 backdrop-blur-sm'
  }
  return 'bg-white/80 border-slate-200/80 hover:bg-white hover:shadow-xl hover:shadow-amber-100/50 backdrop-blur-sm'
})

const iconClasses = computed(() => {
  const colorMap = {
    blue: isDark.value ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-600',
    purple: isDark.value ? 'bg-purple-500/20 text-purple-400' : 'bg-purple-100 text-purple-600',
    green: isDark.value ? 'bg-green-500/20 text-green-400' : 'bg-green-100 text-green-600',
    amber: isDark.value ? 'bg-amber-500/20 text-amber-400' : 'bg-amber-100 text-amber-600',
    orange: isDark.value ? 'bg-orange-500/20 text-orange-400' : 'bg-orange-100 text-orange-600'
  }
  return colorMap[props.color || 'amber'] || colorMap.amber
})

const titleClasses = computed(() => {
  return isDark.value ? 'text-white' : 'text-slate-900'
})

const descriptionClasses = computed(() => {
  return isDark.value ? 'text-gray-400' : 'text-slate-600'
})

const glowClasses = computed(() => {
  const colorMap = {
    blue: 'bg-blue-400',
    purple: 'bg-purple-400',
    green: 'bg-green-400',
    amber: 'bg-amber-400',
    orange: 'bg-orange-400'
  }
  return colorMap[props.color || 'amber'] || colorMap.amber
})
</script>
