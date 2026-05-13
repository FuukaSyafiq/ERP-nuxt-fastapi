<!-- components/charts/LineChart.vue -->
<template>
  <div class="relative w-full" :style="{ height: height + 'px' }">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler,
  type ChartConfiguration,
} from 'chart.js'

// Register Chart.js components
Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend,
  Filler
)

interface Props {
  labels: string[]
  data: number[]
  height?: number
  label?: string
  borderColor?: string
  backgroundColor?: string
  isDark?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  height: 300,
  label: 'Data',
  borderColor: 'rgb(147, 51, 234)', // purple-600
  backgroundColor: 'rgba(147, 51, 234, 0.1)',
  isDark: false,
})

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

const createChart = () => {
  if (!chartCanvas.value) return

  // Destroy previous instance
  if (chartInstance) {
    chartInstance.destroy()
  }

  const textColor = props.isDark ? '#e2e8f0' : '#334155' // slate-200 : slate-700
  const gridColor = props.isDark ? 'rgba(148, 163, 184, 0.1)' : 'rgba(148, 163, 184, 0.2)'

  const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.label,
          data: props.data,
          borderColor: props.borderColor,
          backgroundColor: props.backgroundColor,
          borderWidth: 3,
          tension: 0.4, // Smooth curve
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: props.borderColor,
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: props.isDark ? '#1e293b' : '#ffffff',
          titleColor: textColor,
          bodyColor: textColor,
          borderColor: gridColor,
          borderWidth: 1,
          padding: 12,
          displayColors: false,
          callbacks: {
            label: (context) => {
              const value = context.parsed.y ?? 0
              return new Intl.NumberFormat('id-ID', {
                style: 'currency',
                currency: 'IDR',
                maximumFractionDigits: 0,
              }).format(value)
            },
          },
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            color: textColor,
            font: {
              size: 11,
            },
          },
        },
        y: {
          beginAtZero: true,
          border: {
            display: false,
          },
          grid: {
            color: gridColor,
          },
          ticks: {
            color: textColor,
            font: {
              size: 11,
            },
            callback: (value) => {
              // Format to K (thousands) or M (millions)
              const num = Number(value)
              if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M'
              } else if (num >= 1000) {
                return (num / 1000).toFixed(0) + 'K'
              }
              return num.toString()
            },
          },
        },
      },
    },
  }

  chartInstance = new Chart(chartCanvas.value, config)
}

onMounted(() => {
  createChart()
})

// Watch for data changes
watch(
  () => [props.labels, props.data, props.isDark],
  () => {
    createChart()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>

