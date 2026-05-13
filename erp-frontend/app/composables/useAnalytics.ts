/**
 * Composable untuk Analytics API
 * Endpoint: /analytics dari backend
 */

// Types berdasarkan backend DTO
export interface SalesSummary {
  total_sales: number;
  total_profit: number;
  avg_profit_margin: number;
  transaction_count: number;
  avg_transaction_value: number;
}

export interface TopItem {
  name: string;
  total_qty: number;
  total_revenue: number;
  frequency: number;
}

export interface RecentSale {
  id: string;
  createdAt: Date;
  itemCount: number;
  totalAmount: number;
  profit: number;
  items: {
    name: string;
    qty: number;
    subtotal: number;
  }[];
}

export interface DailySales {
  date: string;
  total_sales: number;
  transaction_count: number;
}

export function useAnalytics() {
  const config = useRuntimeConfig();
  const api = useApi();
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const salesSummary = useState<SalesSummary | null>(
    "sales-summary",
    () => null
  );
  /**
   * Get Sales Summary
   * GET /analytics/sales-summary
   */
  async function getSalesSummary(
    startDate?: string,
    endDate?: string
  ): Promise<SalesSummary | null> {
    try {
      isLoading.value = true;
      error.value = null;

      const token = useCookie("auth_token");
      const params = new URLSearchParams();
      if (startDate) params.append("startDate", startDate);
      if (endDate) params.append("endDate", endDate);

      const query = params.toString() ? `?${params.toString()}` : "";

      // GET ke API menggunakan api.get
      const result = await api.get<SalesSummary>(
        `/analytics/sales-summary${query}`,
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );

      // Simpan state
      salesSummary.value = result;
      return result;
    } catch (err: any) {
      error.value = err?.message || "Gagal memuat ringkasan penjualan";
      console.error("[Analytics] getSalesSummary error:", err);
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Export Sales To PDF
   * GET /analytics/export/pdf
   */
  async function exportPdf(startDate?: string, endDate?: string) {
    try {
      isLoading.value = true;
      error.value = null;
      const baseURL = `${config.public.apiBase}/api/${config.public.apiVersion}`;
      const token = useCookie("auth_token");

      // Build query params
      const params = new URLSearchParams();
      if (startDate) params.append("startDate", startDate);
      if (endDate) params.append("endDate", endDate);
      params.append("exportAll", "true");

      const query = params.toString() ? `?${params.toString()}` : "";

      // Fetch PDF file
      const res = await fetch(`${baseURL}/analytics/export/pdf${query}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      if (!res.ok) {
        throw new Error(`Gagal export PDF: ${res.status}`);
      }

      // Ambil Blob (PDF)
      const pdfBlob = await res.blob();

      // Download otomatis
      const url = URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");

      const fileName = `sales-report-${
        new Date().toISOString().split("T")[0]
      }.pdf`;

      link.href = url;
      link.download = fileName;
      link.click();

      URL.revokeObjectURL(url);

      return true;
    } catch (err: any) {
      error.value = err.message || "Gagal export PDF";
      console.error("[Analytics] exportPdf error:", err);
      return null;
    } finally {
      isLoading.value = false;
    }
  }
  
  

  /**
   * Get Top Selling Items
   * GET /analytics/top-items
   */
  async function getTopItems(
    limit: number = 10,
    startDate?: string,
    endDate?: string
  ): Promise<TopItem[]> {
    try {
      isLoading.value = true;
      error.value = null;
      const token = useCookie("auth_token", { path: "/" });

      const params = new URLSearchParams();
      params.append("limit", limit.toString());
      if (startDate) params.append("startDate", startDate);
      if (endDate) params.append("endDate", endDate);

      const query = params.toString() ? `?${params.toString()}` : "";

      // API GET
      const result = await api.get<TopItem[]>(`/analytics/top-items${query}`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });

      return result;
    } catch (err: any) {
      error.value = err?.message || "Gagal memuat top items";
      console.error("[Analytics] getTopItems error:", err);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Get Recent Sales
   * GET /analytics/recent-sales
   */
  async function getRecentSales(limit: number = 10): Promise<RecentSale[]> {
    try {
      isLoading.value = true;
      error.value = null;

      const token = useCookie("auth_token", { path: "/" });

      // Build query params
      const params = new URLSearchParams();
      params.append("limit", limit.toString());

      const query = `?${params.toString()}`;

      // GET dengan api.get
      const result = await api.get<RecentSale[]>(
        `/analytics/recent-sales${query}`,
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );

      return result;
    } catch (err: any) {
      error.value = err?.message || "Gagal memuat recent sales";
      console.error("[Analytics] getRecentSales error:", err);
      return [];
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Get Daily Sales for Chart (7 days)
   * Menggunakan recent-sales dan aggregate per hari
   */
  async function getDailySales(days: number = 7): Promise<DailySales[]> {
    try {
      const sales = await getRecentSales(100); // Get lebih banyak untuk aggregate

      // Group by date
      const dailyMap = new Map<string, { total: number; count: number }>();

      sales.forEach((sale) => {
        const date = new Date(sale.createdAt).toISOString().split("T")[0];
        const existing = dailyMap.get(date) || { total: 0, count: 0 };
        dailyMap.set(date, {
          total: existing.total + sale.totalAmount,
          count: existing.count + 1,
        });
      });

      // Convert to array and sort
      const dailySales: DailySales[] = Array.from(dailyMap.entries())
        .map(([date, data]) => ({
          date,
          total_sales: data.total,
          transaction_count: data.count,
        }))
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
        .slice(-days); // Take last N days

      // Fill missing days
      const result: DailySales[] = [];
      const today = new Date();

      for (let i = days - 1; i >= 0; i--) {
        const targetDate = new Date(today);
        targetDate.setDate(today.getDate() - i);
        const dateStr = targetDate.toISOString().split("T")[0];

        const found = dailySales.find((d) => d.date === dateStr);
        result.push(
          found || {
            date: dateStr,
            total_sales: 0,
            transaction_count: 0,
          }
        );
      }

      return result;
    } catch (err: any) {
      error.value = err?.message || "Gagal memuat daily sales";
      console.error("[Analytics] getDailySales error:", err);
      return [];
    }
  }

  return {
    isLoading,
    error,
    getSalesSummary,
    getTopItems,
    salesSummary,
    exportPdf,
    getRecentSales,
    getDailySales,
  };
}
