<script setup lang="ts">
const props = defineProps<{
  userId?: string
}>()
</script>

<template>
  <main class="user-profile">
    <h1>用户主页 {{ props.userId }}</h1>
  </main>
</template>
