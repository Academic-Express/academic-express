<script setup lang="ts">
import AppHeader from '@/layout/AppHeader.vue'
import AppFooter from '@/layout/AppFooter.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />

    <div class="container mx-auto flex flex-1 flex-col p-4">
      <RouterView />
    </div>

    <AppFooter />
  </div>
</template>
