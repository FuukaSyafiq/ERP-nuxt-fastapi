# WarungAI Frontend

Platform AI untuk membantu usaha warung dan UMKM Indonesia menjadi lebih cerdas dan efisien.

## Tech Stack

- **Framework:** [Nuxt 3](https://nuxt.com/) (v3.14+)
- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Language:** TypeScript / Vue 3
- **Charts:** [Chart.js](https://www.chartjs.org/) + [vue-chartjs](https://vue-chartjs.org/)

## Struktur Folder

```
app/
├── assets/          # CSS & images yang diprocess
│   ├── css/         # Stylesheet (main.css)
│   └── images/      # Gambar assets
├── components/      # Komponen Vue (auto-import)
│   ├── charts/      # Chart components (LineChart)
│   ├── common/      # Common components (BurgerButton)
│   ├── layout/      # Layout components (Header, Footer, Sidebar, StatCard)
│   └── ui/          # UI components (FeatureCard, LoadingDots, Preview)
├── composables/     # Reusable logic
│   ├── useApi.ts        # API client
│   ├── useAuth.ts       # Authentication
│   ├── useAnalytics.ts  # Analytics & reporting
│   ├── useDashboard.ts  # Dashboard state
│   ├── useLaporan.ts    # Finance report
│   ├── useOcr.ts        # OCR processing
│   ├── useTheme.ts      # Dark/light mode
│   └── ...
├── layouts/         # Layout templates
├── middleware/      # Route middleware (auth.global.ts)
├── pages/           # Halaman (auto-routing)
├── plugins/         # Vue plugins (theme.client.ts)
└── public/          # Static files (favicon, robots.txt)
```

## Quick Start

### Prerequisites

- Node.js >= 20.x
- npm atau pnpm

### Installation

```bash
# Clone repository
git clone <repo-url>
cd WarungAI-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000) di browser.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run preview` | Preview production build |
| `npm run generate` | Generate static site |
| `npm run clean` | Clean build cache |
| `npm run rebuild` | Clean + rebuild |
| `npm run prod` | Full production build & start |

## Docker

### Quick Run (Production Image)

Buat file `compose.yml`:

```yaml
services:
  warungai-frontend:
    image: ghcr.io/kanjutgusion/warungai-frontend:latest
    container_name: warungai-frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NUXT_HOST=0.0.0.0
      - NUXT_PORT=3000
      - NUXT_PUBLIC_API_BASE=${API_BASE_URL}
      - NUXT_PUBLIC_API_VERSION=v1
    restart: unless-stopped
```

Jalankan:
```bash
docker compose up -d
```

### Build from Source

```bash
# Production
docker-compose up --build -d

# Development
docker-compose --profile dev up warungai-frontend-dev
```

## Environment Variables

Buat file `.env`:

```env
# API Configuration
NUXT_PUBLIC_API_BASE=http://localhost:3001
NUXT_PUBLIC_API_VERSION=v1

# App Configuration
NUXT_PUBLIC_APP_NAME=WarungAI
NUXT_PUBLIC_ENABLE_DARK_MODE=true

# Auth
NUXT_PUBLIC_AUTH_COOKIE_NAME=warungai_token
NUXT_PUBLIC_AUTH_COOKIE_EXPIRES=7
```

## Halaman

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/auth/login` | Halaman login |
| `/auth/register` | Halaman registrasi |
| `/dashboard` | Dashboard utama |
| `/dashboard/Laporan` | Laporan keuangan & grafik |
| `/dashboard/AiAssistant` | AI Assistant untuk rekomendasi harga |
| `/dashboard/settings` | Pengaturan akun |

## Features

-  **Authentication** - Login/Register dengan JWT
-  **Dashboard** - Ringkasan penjualan & statistik
-  **OCR Upload** - Scan nota otomatis
-  **Analytics** - Grafik omzet & laporan
-  **AI Assistant** - Rekomendasi harga produk
-  **Dark Mode** - Tema gelap/terang
-  **Responsive** - Mobile-friendly design
-  **Export PDF** - Export laporan ke PDF

## Contributing

1. Fork repository
2. Buat branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## License

MIT License - Lihat [LICENSE](LICENSE) untuk detail.

---

**WarungAI** - Dibuat dengan oleh Tim Sukses Kanjut Gusion
