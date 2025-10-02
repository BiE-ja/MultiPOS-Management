import {defineConfig} from "vite";
import path from "node:path";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import {tanstackRouter} from "@tanstack/router-plugin/vite";

// https://vite.dev/config/
export default defineConfig({
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    plugins: [
        tanstackRouter({
            target: "react",
            autoCodeSplitting: true,
        }),
        react(),
        tsconfigPaths(),
    ],
    build: {
        target: "es2023", // ✅ ici
    },
});
