<script setup lang="ts">
import { ref, watchEffect } from 'vue'

import { getArxivEntry, type ArxivEntry } from '@/services/api'

const props = defineProps<{
  arxivId: string
}>()

const arxivEntry = ref<ArxivEntry | null>(null)

watchEffect(async () => {
  try {
    const response = await getArxivEntry(props.arxivId)
    arxivEntry.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <div class="container mx-auto max-w-[960px] p-4">
    <div class="rounded-lg bg-surface-50 p-6 shadow-md dark:bg-surface-950">
      <!-- Title -->
      <h1 class="mb-4 text-2xl font-bold">
        <span v-if="arxivEntry">{{ arxivEntry.title }}</span>
        <Skeleton v-else height="2rem" />
      </h1>

      <!-- Authors -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Authors:</h2>
        <p v-if="arxivEntry">
          <template v-for="(author, i) in arxivEntry.authors" :key="i">
            <span v-if="i > 0" class="text-muted-color">, </span>
            <span>{{ author.name }}</span>
          </template>
        </p>
        <Skeleton v-else height="1.5rem" />
      </div>

      <!-- Summary -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Summary:</h2>
        <p v-if="arxivEntry">{{ arxivEntry.summary }}</p>
        <p v-else>
          <Skeleton v-for="i in 5" :key="i" height="1rem" class="mt-2" />
        </p>
      </div>

      <!-- Categories -->
      <div class="mb-4" v-if="arxivEntry">
        <div class="flex flex-wrap gap-2">
          <Button
            v-for="category in arxivEntry.categories"
            :key="category"
            class="px-4 py-2"
            rounded
            severity="secondary"
          >
            {{ category }}
          </Button>
        </div>
      </div>

      <!-- Publication Dates -->
      <div class="mb-4" v-if="arxivEntry">
        <p>
          <strong>Published:</strong>
          {{ new Date(arxivEntry.published).toLocaleString() }}
        </p>
        <p>
          <strong>Updated:</strong>
          {{ new Date(arxivEntry.updated).toLocaleString() }}
        </p>
      </div>

      <!-- Links -->
      <div class="flex gap-4" v-if="arxivEntry">
        <Button
          icon="pi pi-external-link"
          label="View Original"
          severity="success"
          rounded
          as="a"
          :href="arxivEntry.link"
          target="_blank"
        ></Button>
        <Button
          icon="pi pi-download"
          label="Download PDF"
          severity="info"
          rounded
          as="a"
          :href="arxivEntry.pdf"
          target="_blank"
        ></Button>
      </div>
    </div>
  </div>
</template>
