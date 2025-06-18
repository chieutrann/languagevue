import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "127.0.0.1", // Changed from 0.0.0.0 to 127.0.0.1 to avoid permission issues
    port: 3000, // Changed from 5000 to 3000 to avoid conflict with Flask server
    allowedHosts: [
      "bec1a4ba-802f-4031-b388-3b92e176cac7-00-19v8nzx5k7zt5.janeway.replit.dev",
    ],
  },
});
