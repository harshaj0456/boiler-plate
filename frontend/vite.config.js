import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";
import path from "node:path";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.svg"],
      manifest: {
        name: "Hackathon App",
        short_name: "Hackathon App",
        description: "Reusable React + Vite + Tailwind hackathon starter",
        theme_color: "#0f172a",
        background_color: "#f8fafc",
        display: "standalone",
        icons: [
          { src: "/pwa-192x192.png", sizes: "192x192", type: "image/png" },
          { src: "/pwa-512x512.png", sizes: "512x512", type: "image/png" }
        ]
      }
    })
  ],
  resolve: { alias: { "@": path.resolve(process.cwd(), "./src") } },
  server: { port: 5173, host: true }
});
