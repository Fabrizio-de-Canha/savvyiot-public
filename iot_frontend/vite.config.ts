import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // Set base URL if the app is deployed to a subpath (optional)
  base: '/', // Adjust this if your app is hosted in a subdirectory, e.g., '/my-app/'
  build: {
    rollupOptions: {
      output: {
        // Ensures all chunks are output together, useful for SPAs
        manualChunks: undefined,
      },
    },
  },
})
