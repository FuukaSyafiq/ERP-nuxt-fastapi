/**
 * Composable untuk Laporan Keuangan
 * Fetch data dari Analytics API
 */

interface OmzetPoint {
  label: string
  value: number
}

interface FinanceSummary {
  omzetToday: number
  totalTransactions: number
  uniqueProducts: number
  totalExpenses: number
}

export function useFinanceReport() {
  const api = useApi()
  const isLoading = ref(true)
  const error = ref<string | null>(null)

  const summary = ref<FinanceSummary>({
    omzetToday: 0,
    totalTransactions: 0,
    uniqueProducts: 0,
    totalExpenses: 0,
  })

  const omzetSeries = ref<OmzetPoint[]>([
    { label: 'Sen', value: 0 },
    { label: 'Sel', value: 0 },
    { label: 'Rab', value: 0 },
    { label: 'Kam', value: 0 },
    { label: 'Jum', value: 0 },
    { label: 'Sab', value: 0 },
    { label: 'Min', value: 0 },
  ])

  const formatRupiah = (value: number) =>
    new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      maximumFractionDigits: 0,
    }).format(value)

  const loadReport = async () => {
    try {
      isLoading.value = true
      error.value = null

      const token = useCookie('auth_token', { path: '/' })

      // Fetch sales summary dari Analytics API
      const salesSummary = await api.get<{
        total_sales: number
        total_profit: number
        avg_profit_margin: number
        transaction_count: number
        avg_transaction_value: number
      }>(`/analytics/sales-summary`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      })

      // Fetch top items untuk count unique products
      const topItems = await api.get<Array<{
        name: string
        total_qty: number
        total_revenue: number
        frequency: number
      }>>('/analytics/top-items?limit=1000', {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      })

      // Calculate expenses: total_sales - total_profit = expenses
      const totalExpenses = (salesSummary.total_sales || 0) - (salesSummary.total_profit || 0)

      // Map data dari API ke format summary
      summary.value = {
        omzetToday: salesSummary.total_sales || 0,
        totalTransactions: salesSummary.transaction_count || 0,
        uniqueProducts: topItems.length || 0, // Count unique products
        totalExpenses: totalExpenses > 0 ? totalExpenses : 0, // Total pengeluaran
      }

    } catch (err: any) {
      error.value = err?.message ?? 'Gagal memuat laporan.'
      console.error('[FinanceReport] Error:', err)
      
      // Fallback to zero values on error
      summary.value = {
        omzetToday: 0,
        totalTransactions: 0,
        uniqueProducts: 0,
        totalExpenses: 0,
      }
    } finally {
      isLoading.value = false
    }
  }

  // Untuk line chart 
  const omzetPath = computed(() => {
    const points = omzetSeries.value
    if (!points.length) return ''

    const maxVal = Math.max(...points.map((p) => p.value)) || 1
    const width = 200
    const height = 60
    const padding = 6
    const stepX = points.length > 1 ? width / (points.length - 1) : 0

    return points
      .map((p, idx) => {
        const x = idx * stepX
        const y =
          height -
          padding -
          (p.value / maxVal) * (height - padding * 2)

        return `${idx === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`
      })
      .join(' ')
  })

  return {
    isLoading,
    error,
    summary,
    omzetSeries,
    omzetPath,
    formatRupiah,
    loadReport,
  }
}
