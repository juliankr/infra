import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  root: process.cwd(),
  server: {
    host: true,
    port: 5173
  }
})
