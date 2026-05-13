/**
 * Composable untuk Authentication
 */
export const useAuth = () => {
  const user = useState<User | null>("user", () => null);
  const isLoggedIn = computed(() => !!user.value);

  /**
   * Register user
   */
  const api = useApi(); // Bisa dipakai di semua request
  const register = async (
    username: string,
    password: string,
    email: string,
    phone: string,
  ) => {
    try {
      const response = await api.post<AuthResponse>(
        "/auth/register",
        {
          username,
          phone,
          email,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
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

  /**
   * Login user
   */
  const login = async (email: string, password: string) => {
    try {
      const response = await api.post<AuthResponse>(
        "/auth/login",
        {
          email,
          password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        },
      );

      user.value = response.data.user;

      // Store token di cookie
      const token = useCookie("auth_token", {
        path: "/",
        maxAge: 60 * 60 * 24,
      });
      token.value = response.data.token;
      user.value = response.data.user;

      return {
        success: response.success,
        status: 200, // HTTP OK
        data: response.data,
      };
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

  /**
   * Logout user
   */
  const logout = () => {
    user.value = null;
    const token = useCookie("auth_token", { path: "/" });
    token.value = null;
    navigateTo("/auth/login");
  };

  /**
   * Check if user is authenticated
   */
  const checkAuth = async () => {
    const token = useCookie("auth_token", { path: "/" });
    if (!token.value) {
      return {
        success: false,
        error: "User already logged out",
      };
    }
    try {
      const response = await api.get<User>("/auth/me", {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      });
      user.value = response;
      return {
        success: true,
        status: 200, // HTTP OK
        data: response,
      };
    } catch (err: any) {
      logout();
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
    user,
    isLoggedIn,
    login,
    register,
    logout,
    checkAuth,
  };
};

// Types
interface User {
  id: number;
  username: string;
  phone: string;
  email: string;
  status: string;
  user_role: {
    id: string;
    name: string;
  };
}

interface AuthResponse {
  user: User;
  token: string;
}
