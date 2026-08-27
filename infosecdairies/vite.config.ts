import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: true,
    proxy: {
      "/api/chat": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        secure: false,
        xfwd: true,
      },
      "/api/conversations": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        secure: false,
      },
      "/api/health": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        secure: false,
        xfwd: true,
      },
      "/api/token-usage": {
        target: "http://127.0.0.1:8001",
        changeOrigin: true,
        secure: false,
        xfwd: true,
      },
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
  plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
