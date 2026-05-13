// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: process.env.NUXT_PUBLIC_ENABLE_DEVTOOLS === "true" },
  ssr: true,
  nitro: {
    preset: "node-server",
  },
  // Source directory
  srcDir: "app",

  // Modules
  modules: ["@nuxtjs/tailwindcss"],

  // Tailwind CSS config
  tailwindcss: {
    config: {
      darkMode: 'class'
    }
  },

  // Global CSS
  css: ["~/assets/css/main.css"],

  // Runtime config (accessible via useRuntimeConfig())
  runtimeConfig: {
    // Private keys (server-side only)
    apiSecret: "",

    // Public keys (exposed to client)
    public: {
      // API
      apiBase:
        process.env.NUXT_PUBLIC_API_BASE ||
        process.env.API_BASE_URL ||
        "http://localhost:3001",

      apiVersion:
        process.env.NUXT_PUBLIC_API_VERSION || process.env.API_VERSION || "v1",
      apiTimeout: parseInt(process.env.API_TIMEOUT || "30000"),
      // App
      appName: process.env.NUXT_PUBLIC_APP_NAME || "WarungAI",
      appDescription:
        process.env.NUXT_PUBLIC_APP_DESCRIPTION ||
        "Platform AI untuk UMKM Indonesia",

      // Auth
      authCookieName:
        process.env.NUXT_PUBLIC_AUTH_COOKIE_NAME || "warungai_token",
      authCookieExpires: parseInt(
        process.env.NUXT_PUBLIC_AUTH_COOKIE_EXPIRES || "7"
      ),

      // Features
      enableAnalytics: process.env.NUXT_PUBLIC_ENABLE_ANALYTICS === "true",
      enableDarkMode: process.env.NUXT_PUBLIC_ENABLE_DARK_MODE !== "false",

      // Third Party
      gaId: process.env.NUXT_PUBLIC_GA_ID || "",
      sentryDsn: process.env.NUXT_PUBLIC_SENTRY_DSN || "",

      // Upload
      maxUploadSize: parseInt(
        process.env.NUXT_PUBLIC_MAX_UPLOAD_SIZE || "5242880"
      ),
      allowedFileTypes:
        process.env.NUXT_PUBLIC_ALLOWED_FILE_TYPES ||
        "image/jpeg,image/png,image/webp",

      // Pagination
      defaultPageSize: parseInt(
        process.env.NUXT_PUBLIC_DEFAULT_PAGE_SIZE || "10"
      ),
      maxPageSize: parseInt(process.env.NUXT_PUBLIC_MAX_PAGE_SIZE || "100"),

      // Cache
      cacheTtl: parseInt(process.env.NUXT_PUBLIC_CACHE_TTL || "300"),

      // Social
      socialInstagram: process.env.NUXT_PUBLIC_SOCIAL_INSTAGRAM || "",
      socialTwitter: process.env.NUXT_PUBLIC_SOCIAL_TWITTER || "",
      socialFacebook: process.env.NUXT_PUBLIC_SOCIAL_FACEBOOK || "",
      socialWhatsapp: process.env.NUXT_PUBLIC_SOCIAL_WHATSAPP || "",
    },
  },

  // App config
  app: {
    head: {
      title: process.env.NUXT_PUBLIC_APP_NAME || "WarungAI",
      meta: [
        {
          name: "description",
          content:
            process.env.NUXT_PUBLIC_APP_DESCRIPTION ||
            "Platform AI untuk UMKM Indonesia",
        },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "theme-color", content: "#f59e0b" },
      ],
      link: [
        { rel: "icon", type: "image/png", href: "/favicon.png" },
      ],
    },
  },
});
