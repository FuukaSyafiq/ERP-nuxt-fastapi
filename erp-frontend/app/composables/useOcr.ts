export type OcrRow = {
  id: number;
  name: string;
  qty: number;
  price: number;
  total: number;
};

export function useOcr() {
  const config = useRuntimeConfig();
  const baseURL = `${config.public.apiBase}/api/${config.public.apiVersion}`;
  const ocrRows = ref<OcrRow[]>([]);
  const ocrLoading = ref(false);
  const uploadError = ref<string | null>(null);

  const omzetToday = computed(() =>
    ocrRows.value.reduce((sum, row) => sum + row.total, 0)
  );

  const uniqueProductCount = computed(() => {
    const products = new Set(ocrRows.value.map((row) => row.name));
    return products.size;
  });

  const formatRupiah = (amount: number) =>
    new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(amount || 0);

  const updateOcrData = (parsedData: OcrRow[]) => {
    ocrRows.value = parsedData;
    uploadError.value = null;
  };

  const clearError = () => {
    uploadError.value = null;
  };

  const api = useApi();

  /**
   * Upload file ke backend dan update OCR rows
   */
  const upload = async (file: File) => {
    if (!file) {
      uploadError.value = "File tidak ditemukan.";
      return {
        success: false,
        status: 400,
        error: "File tidak ditemukan.",
      };
    }

    ocrLoading.value = true;
    uploadError.value = null;

    try {
      const formData = new FormData();
      formData.append("image", file);
      const token = useCookie("auth_token", { path: "/" });
      const endpoint = `${baseURL}/ocr`;
      const response = await $fetch<OcrResponse>(endpoint, {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      const data = response;
      const parsedRows: OcrRow[] = data.items.map(
        (item: any, index: number) => ({
          id: index + 1,
          name: item.name, // pastikan sesuai OcrRow
          qty: item.qty,
          price: item.price,
          total: item.qty * item.price,
        })
      );

      updateOcrData(parsedRows);
      return {
        success: true,
        status: 200,
        data: parsedRows
      }
    } catch (err: any) {
      uploadError.value =
        err?.response?.data?.message || "Gagal mengupload nota.";
      const status = err?.response?.status || null;
      const message = err?.data?.error || err?.message || "Terjadi kesalahan";

      return {
        success: false,
        status,
        error: message,
      };
    } finally {
      ocrLoading.value = false;
    }
  };

  interface OcrItem {
    name: string;
    qty: number;
    price: number;
  }

  interface OcrResponse {
    items: OcrRow[];
    total: number;
    profit: number;
    summary: Record<string, any>; // karena summary kosong dan bisa fleksibel
  }

  return {
    ocrRows,
    ocrLoading,
    uploadError,
    upload,
    // omzetToday,
    uniqueProductCount,
    formatRupiah,
    updateOcrData,
    clearError,
  };
}
