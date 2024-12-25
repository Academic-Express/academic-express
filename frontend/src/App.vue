<script setup lang="ts">
import { onMounted, watchEffect } from 'vue'
import { useAuthStore } from './stores/auth'
import { useUserStore } from './stores/user'
import { useThemeStore } from './stores/theme'

const authStore = useAuthStore()
const userStore = useUserStore()
const themeStore = useThemeStore()

onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      await userStore.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }
})

watchEffect(() => {
  document.documentElement.classList.toggle('dark-mode', themeStore.darkMode)
})
</script>

<template>
  <RouterView />
  <Toast position="top-center" />
  <ConfirmDialog />
</template>

<style scoped></style>
