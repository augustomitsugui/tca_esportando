import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'

// Endereço da API FastAPI. Dentro do Docker use http://host.docker.internal:17000
const backend = process.env.BACKEND_URL ?? 'http://localhost:17000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte(), tailwindcss()],
  server: {
    // O backend não configura CORS. Em desenvolvimento o Vite repassa as
    // chamadas de "/api/..." para a API e tira o prefixo "/api".
    proxy: {
      '/api': {
        target: backend,
        changeOrigin: true,
        rewrite: (caminho) => caminho.replace(/^\/api/, ''),
      },
    },
  },
})
