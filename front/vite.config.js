import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// o navegador chama /api/... e o vite repassa pro fofissimo backend (sem /api).
const backend = process.env.BACKEND_URL || 'http://localhost:17000';

const proxy = {
  '/api': {
    target: backend,
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),
  },
};

export default defineConfig({
  plugins: [svelte()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    watch: { usePolling: true },
    proxy,
  },
  preview: { host: true, port: 5173, proxy },
});
