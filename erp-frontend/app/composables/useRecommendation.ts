export const useRecommendation = () => {
  /**
   * Recommendation optimal price
   */
  const api = useApi(); // Bisa dipakai di semua request
  /**
   * Global state untuk semua rekomendasi
   */
  const recommendationPriceState = useState<RecommendationResponse[]>(
    "recommendationPrice",
    () => []
  );

  const recommendationPriceByItemState =
    useState<RecommendationResponse | null>(
      "recommendationPriceByItem",
      () => null
    );
  
  const recommendationPrice = async (expectedMargin: number) => {
    try {
      const token = useCookie("auth_token", { path: "/" });
     
      const result = await api.get<RecommendationResponse[]>(
        `/pricing/recommendations?target_margin=${expectedMargin}`,
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );
      const data = result || [];
      recommendationPriceState.value = data;

      return { success: true, status: 200, data: result };
    } catch (err: any) {
      // $fetch throw error untuk non-2xx
      const status = err?.result?.status || null;
      const message = err?.data?.error || err?.message || "Terjadi kesalahan";

      return {
        success: false,
        status,
        error: message,
      };
    }
  };

  const recommendationPriceByItem = async (
    itemName: string,
    expectedMargin: number
  ) => {
    try {
      const token = useCookie("auth_token", { path: "/" });

      const response = await api.get<RecommendationResponse>(
        `/pricing/recommendations/${encodeURIComponent(
          itemName
        )}?target_margin=${expectedMargin}`,
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        }
      );
      const data: RecommendationResponse | null = response ?? null;

      // Simpan ke global state
      recommendationPriceByItemState.value = data;

      return { success: true, status: 200, data: response };
    } catch (err: any) {
      // $fetch throw error untuk non-2xx
      const status = err?.response?.status || null;
      const message = err?.data?.error || err?.message || "Terjadi kesalahan";

      return {
        success: false,
        status,
        error: message,
      };
    }
  };

  return {
    recommendationPrice,
    recommendationPriceByItem,
    recommendationPriceByItemState,
    recommendationPriceState
  };
};

export interface RecommendationResponse {
  item_name: string;
  current_price: number;
  recommended_price: number;
  expected_margin: number;
  reasoning: string;
}
