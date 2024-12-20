// vite.config.ts
import { fileURLToPath, URL } from "node:url";
import { resolve, dirname } from "node:path";
import { defineConfig } from "file:///home/shenzhiy21/academic-express/frontend/node_modules/vite/dist/node/index.js";
import vue from "file:///home/shenzhiy21/academic-express/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import vueJsx from "file:///home/shenzhiy21/academic-express/frontend/node_modules/@vitejs/plugin-vue-jsx/dist/index.mjs";
import Components from "file:///home/shenzhiy21/academic-express/frontend/node_modules/unplugin-vue-components/dist/vite.js";
import { PrimeVueResolver } from "file:///home/shenzhiy21/academic-express/frontend/node_modules/@primevue/auto-import-resolver/index.mjs";
import VueI18nPlugin from "file:///home/shenzhiy21/academic-express/frontend/node_modules/@intlify/unplugin-vue-i18n/lib/vite.mjs";
var __vite_injected_original_import_meta_url = "file:///home/shenzhiy21/academic-express/frontend/vite.config.ts";
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    Components({
      resolvers: [PrimeVueResolver()]
    }),
    VueI18nPlugin({
      include: resolve(
        dirname(fileURLToPath(__vite_injected_original_import_meta_url)),
        "src/locales/**"
      )
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvaG9tZS9zaGVuemhpeTIxL2FjYWRlbWljLWV4cHJlc3MvZnJvbnRlbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9ob21lL3NoZW56aGl5MjEvYWNhZGVtaWMtZXhwcmVzcy9mcm9udGVuZC92aXRlLmNvbmZpZy50c1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vaG9tZS9zaGVuemhpeTIxL2FjYWRlbWljLWV4cHJlc3MvZnJvbnRlbmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBmaWxlVVJMVG9QYXRoLCBVUkwgfSBmcm9tICdub2RlOnVybCdcbmltcG9ydCB7IHJlc29sdmUsIGRpcm5hbWUgfSBmcm9tICdub2RlOnBhdGgnXG5cbmltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gJ3ZpdGUnXG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSdcbmltcG9ydCB2dWVKc3ggZnJvbSAnQHZpdGVqcy9wbHVnaW4tdnVlLWpzeCdcbmltcG9ydCBDb21wb25lbnRzIGZyb20gJ3VucGx1Z2luLXZ1ZS1jb21wb25lbnRzL3ZpdGUnXG5pbXBvcnQgeyBQcmltZVZ1ZVJlc29sdmVyIH0gZnJvbSAnQHByaW1ldnVlL2F1dG8taW1wb3J0LXJlc29sdmVyJ1xuaW1wb3J0IFZ1ZUkxOG5QbHVnaW4gZnJvbSAnQGludGxpZnkvdW5wbHVnaW4tdnVlLWkxOG4vdml0ZSdcblxuLy8gaHR0cHM6Ly92aXRlLmRldi9jb25maWcvXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xuICBwbHVnaW5zOiBbXG4gICAgdnVlKCksXG4gICAgdnVlSnN4KCksXG4gICAgQ29tcG9uZW50cyh7XG4gICAgICByZXNvbHZlcnM6IFtQcmltZVZ1ZVJlc29sdmVyKCldLFxuICAgIH0pLFxuICAgIFZ1ZUkxOG5QbHVnaW4oe1xuICAgICAgaW5jbHVkZTogcmVzb2x2ZShcbiAgICAgICAgZGlybmFtZShmaWxlVVJMVG9QYXRoKGltcG9ydC5tZXRhLnVybCkpLFxuICAgICAgICAnc3JjL2xvY2FsZXMvKionLFxuICAgICAgKSxcbiAgICB9KSxcbiAgXSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQCc6IGZpbGVVUkxUb1BhdGgobmV3IFVSTCgnLi9zcmMnLCBpbXBvcnQubWV0YS51cmwpKSxcbiAgICB9LFxuICB9LFxufSlcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBZ1QsU0FBUyxlQUFlLFdBQVc7QUFDblYsU0FBUyxTQUFTLGVBQWU7QUFFakMsU0FBUyxvQkFBb0I7QUFDN0IsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sWUFBWTtBQUNuQixPQUFPLGdCQUFnQjtBQUN2QixTQUFTLHdCQUF3QjtBQUNqQyxPQUFPLG1CQUFtQjtBQVJrSyxJQUFNLDJDQUEyQztBQVc3TyxJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTO0FBQUEsSUFDUCxJQUFJO0FBQUEsSUFDSixPQUFPO0FBQUEsSUFDUCxXQUFXO0FBQUEsTUFDVCxXQUFXLENBQUMsaUJBQWlCLENBQUM7QUFBQSxJQUNoQyxDQUFDO0FBQUEsSUFDRCxjQUFjO0FBQUEsTUFDWixTQUFTO0FBQUEsUUFDUCxRQUFRLGNBQWMsd0NBQWUsQ0FBQztBQUFBLFFBQ3RDO0FBQUEsTUFDRjtBQUFBLElBQ0YsQ0FBQztBQUFBLEVBQ0g7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLE9BQU87QUFBQSxNQUNMLEtBQUssY0FBYyxJQUFJLElBQUksU0FBUyx3Q0FBZSxDQUFDO0FBQUEsSUFDdEQ7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
