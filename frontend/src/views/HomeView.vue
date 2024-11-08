<script setup lang="ts">
import { useHead } from '@unhead/vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

useHead({ title: t('_title') })
</script>

<template>
  <main>
    <h1>Hello, world!</h1>
  </main>
</template>

<i18n locale="zh-CN">
{
  "_title": "@:app.name",
}
</i18n>
