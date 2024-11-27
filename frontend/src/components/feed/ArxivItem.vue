<script setup lang="ts">
import type { ArxivEntry } from '@/services/api'

import arxivLogo from '@/assets/arxiv-logo.svg'

defineProps<{
  arxivEntry: ArxivEntry
}>()
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

    <div class="flex flex-wrap text-xs">
      <!-- Links -->
      <div class="mr-4">
        <Button
          :label="arxivEntry.arxiv_id.split('v')[0]"
          severity="primary"
          as="a"
          :href="arxivEntry.link"
          target="_blank"
          class="p-button-sm"
        ></Button>
      </div>

      <!-- Categories -->
      <div class="flex flex-wrap gap-x-4 gap-y-2">
        <Button
          v-for="category in arxivEntry.categories"
          :key="category"
          severity="secondary"
          class="p-button-sm"
        >
          {{ category }}
        </Button>
      </div>

      <div class="ml-auto mr-2 flex items-center">
        <a :href="arxivEntry.link" target="_blank">
          <img :src="arxivLogo" alt="Arxiv Logo" class="h-5" />
        </a>
      </div>
    </div>
  </div>
  <!-- Dividing Line -->
  <hr class="my-4" />
</template>
