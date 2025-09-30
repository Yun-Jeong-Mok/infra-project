// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
    server: {
      proxy: {
        '/api': {
          target: 'https://localhost:8888',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
      https: {
        cert: 'localhost+1.pem',
        key: 'localhost+1-key.pem',
      },
      host: true,
      allowedHosts: true,
    },
  },
});

