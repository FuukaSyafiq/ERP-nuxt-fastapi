/**
 * Composable untuk komunikasi dengan Backend API
 */
export const useApi = () => {
  const config = useRuntimeConfig();
  const baseURL = `${config.public.apiBase}/api/${config.public.apiVersion}`;

  /**
   * Generic fetch wrapper
   */
  const fetchApi = async <T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    const response = await $fetch<T>(endpoint, {
      baseURL,
      ...options,
      method: options.method as
        | "GET"
        | "POST"
        | "PUT"
        | "PATCH"
        | "DELETE"
        | "HEAD"
        | "OPTIONS"
        | undefined,
    });
    return response;
  };

  /**
   * GET request
   */
  const get = <T>(
    endpoint: string,
    options?: { headers?: Record<string, string> }
  ) =>
    fetchApi<T>(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json",
        ...options?.headers, // header tambahan
      },
    });
  /**
   * POST request
   */
  const post = <T>(
    endpoint: string,
    body: unknown,
    options?: { headers?: Record<string, string> }
  ) =>
    fetchApi<T>(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        ...options?.headers, // merge headers tambahan, misal Authorization
      },
    });
  

  /**
   * PUT request
   */
  const put = <T>(endpoint: string, body: unknown) =>
    fetchApi<T>(endpoint, {
      method: "PUT",
      body: JSON.stringify(body),
      headers: { "Content-Type": "application/json" },
    });

  /**
   * DELETE request
   */
  const del = <T>(endpoint: string) =>
    fetchApi<T>(endpoint, { method: "DELETE" });

  return {
    get,
    post,
    put,
    del,
    fetchApi,
  };
};
