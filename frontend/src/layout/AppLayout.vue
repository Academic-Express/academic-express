<script setup lang="ts">
import AppHeader from '@/layout/AppHeader.vue'
import AppFooter from '@/layout/AppFooter.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />

    <div class="container mx-auto flex-1 p-4">
      <RouterView />
    </div>

    <AppFooter />
  </div>
</template>
