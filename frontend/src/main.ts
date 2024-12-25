import 'primeicons/primeicons.css'
import './assets/tailwind.css'
import './assets/main.css'

import '@/assets/github-markdown.css'
import hljsLightTheme from 'highlight.js/styles/github.css?inline'
import hljsDarkTheme from 'highlight.js/styles/github-dark.css?inline'

import { createApp, watchEffect } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ConfirmationService from 'primevue/confirmationservice'
import ToastService from 'primevue/toastservice'

import App from './App.vue'
import router from './router'
import i18n from './i18n'
import bus from './bus'
import { useThemeStore } from './stores/theme'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(createHead())
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.dark-mode',
    },
  },
  ripple: true,
})
app.use(ConfirmationService)
app.use(ToastService)
app.use(bus)

app.mount('#app')

const themeStore = useThemeStore()
const style = document.createElement('style')
document.head.appendChild(style)

watchEffect(() => {
  style.textContent = themeStore.darkMode ? hljsDarkTheme : hljsLightTheme
})
