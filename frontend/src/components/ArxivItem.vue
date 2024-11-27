<script setup lang="ts">
import { useI18n } from 'vue-i18n'

import type { ArxivEntry } from '@/services/api'

defineProps<{
  arxivEntry: ArxivEntry
}>()

const { t } = useI18n()
</script>

<template>
  <div class="mt-4">
    <!-- Title -->
    <div class="mb-3 line-clamp-1 text-xl font-bold">
      <RouterLink
        :to="{
          name: 'pub-arxiv',
          params: { arxivId: arxivEntry.arxiv_id, slug: arxivEntry.slug },
        }"
        class="transition-colors hover:text-blue-500 hover:underline"
      >
        {{ arxivEntry.title }}
      </RouterLink>
    </div>

    <!-- Authors -->
    <div class="mb-3 text-sm italic">
      <p>
        <template v-for="(author, i) in arxivEntry.authors" :key="i">
          <span v-if="i > 0" class="text-muted-color">, </span>
          <span>{{ author.name }}</span>
        </template>
      </p>
    </div>

    <!-- Abstract -->
    <div class="mb-4 flex items-center">
      <p class="line-clamp-3">{{ arxivEntry.summary }}</p>
    </div>

    <div class="flex flex-wrap gap-6 text-xs">
      <!-- Categories -->
      <div class="flex flex-wrap gap-4">
        <Button
          v-for="category in arxivEntry.categories"
          :key="category"
          severity="secondary"
          class="p-button-sm"
        >
          {{ category }}
        </Button>
      </div>

      <!-- Links -->
      <div class="flex gap-4">
        <Button
          icon="pi pi-external-link"
          :label="t('viewOriginal')"
          severity="success"
          as="a"
          :href="arxivEntry.link"
          target="_blank"
          class="p-button-sm"
        ></Button>
        <Button
          icon="pi pi-download"
          :label="t('downloadPdf')"
          severity="info"
          as="a"
          :href="arxivEntry.pdf"
          target="_blank"
          class="p-button-sm"
        ></Button>
      </div>
    </div>
  </div>
  <!-- Dividing Line -->
  <hr class="my-4" />
</template>

<i18n locale="zh-CN">
  {
    "viewOriginal": "查看原文",
    "downloadPdf": "下载 PDF",
  }
</i18n>
