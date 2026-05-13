/**
 * Composable untuk Dashboard Overview
 */
import type { OcrRow } from "~/composables/useOcr";

// Types
export interface Stat {
  icon: string;
  value: string;
  label: string;
}

// Re-export OcrRow for convenience
export type { OcrRow } from "~/composables/useOcr";

export function useDashboardOverview() {
  // State
  const ocrRows = ref<OcrRow[]>([]);

  // Computed
  const omzetToday = computed(() =>
    ocrRows.value.reduce((sum, row) => sum + row.total, 0)
  );

  const todayLabel = computed(() =>
    new Intl.DateTimeFormat("id-ID", {
      weekday: "long",
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(new Date())
  );

  // Methods
  const formatRupiah = (amount: number) =>
    new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(amount || 0);

  const updateOcrData = (parsedData: OcrRow[]) => {
    ocrRows.value = parsedData;
  };

  return {
    ocrRows,
    omzetToday,
    todayLabel,
    formatRupiah,
    updateOcrData,
  };
}