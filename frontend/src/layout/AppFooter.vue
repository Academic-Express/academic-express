<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <footer>
    <div class="container mx-auto py-4 text-center text-muted-color">
      <p>&copy; 2024 {{ t('app.name') }}.</p>
    </div>
  </footer>
</template>
