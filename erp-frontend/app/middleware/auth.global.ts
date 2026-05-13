/**
 * Middleware untuk proteksi halaman yang membutuhkan login
 */
export default defineNuxtRouteMiddleware(async (to, from) => {
  const { user, isLoggedIn, checkAuth } = useAuth();
  const token = useCookie("auth_token");
  const publicPages = ["/", "/auth/login", "/auth/register"];

  const authPages = ["/auth/login", "/auth/register"];
  // Halaman publik
  if (authPages.includes(to.path) && isLoggedIn.value) {
    return navigateTo("/dashboard");
  }

  // Jika di halaman publik biasa (seperti /) → biarkan akses
  if (publicPages.includes(to.path)) {
    return;
  }

  if (!token.value) {
    return navigateTo("/auth/login");
  }
  
  if (!user) {
    return navigateTo("/auth/login");
  }
});
