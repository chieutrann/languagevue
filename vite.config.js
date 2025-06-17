import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5000,
    allowedHosts: [
      "bec1a4ba-802f-4031-b388-3b92e176cac7-00-19v8nzx5k7zt5.janeway.replit.dev",
    ],
  },
});
