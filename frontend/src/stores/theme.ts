import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  const darkMode = ref(localStorage.getItem('darkMode') === 'true')

  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    localStorage.setItem('darkMode', darkMode.value.toString())
  }

  return {
    darkMode,
    toggleDarkMode,
  }
})
