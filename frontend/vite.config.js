import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  assetsInclude: ['**/*.svg'],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        create: resolve(__dirname, 'create/index.html'),
        poll: resolve(__dirname, 'poll/index.html'),
        auth: resolve(__dirname, 'auth/index.html'),
        res: resolve(__dirname, 'res/index.html')
      }
    }
  }
})
