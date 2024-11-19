<script setup lang="ts">
import { ref, watchEffect } from 'vue'

import {
  getArxivEntry,
  type ArxivEntry,
  type ArxivAuthor,
} from '@/services/api'

const props = defineProps<{
  arxivId: string
}>()

const fetchedArxivEntry = ref<ArxivEntry | null>(null)
const fetchedArxivAuthors = ref<ArxivAuthor[]>([])

watchEffect(async () => {
  try {
    const response = await getArxivEntry(props.arxivId)
    fetchedArxivEntry.value = response.data
    fetchedArxivAuthors.value = response.data.authors
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <div class="container mx-auto max-w-[960px] p-4">
    <div class="rounded-lg bg-surface-50 p-6 shadow-md dark:bg-surface-950">
      <!-- Title -->
      <h1 class="mb-4 text-2xl font-bold">{{ fetchedArxivEntry?.title }}</h1>

      <!-- Authors -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Authors:</h2>
        <p>
          {{ fetchedArxivEntry?.authors.map(({ name }) => name).join(', ') }}
        </p>
      </div>

      <!-- Summary -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">Summary:</h2>
        <p>{{ fetchedArxivEntry?.summary }}</p>
      </div>

      <!-- Categories -->
      <div class="mb-4">
        <div class="flex flex-wrap gap-2">
          <Button
            v-for="category in fetchedArxivEntry?.categories"
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
      <div class="mb-4">
        <p>
          <strong>Published:</strong>
          {{
            fetchedArxivEntry?.published
              ? new Date(fetchedArxivEntry.published).toLocaleString()
              : ''
          }}
        </p>
        <p>
          <strong>Updated:</strong>
          {{
            fetchedArxivEntry?.updated
              ? new Date(fetchedArxivEntry.updated).toLocaleString()
              : ''
          }}
        </p>
      </div>

      <!-- Links -->
      <div class="flex gap-4">
        <Button
          icon="pi pi-external-link"
          label="View Original"
          severity="success"
          rounded
          as="a"
          :href="fetchedArxivEntry?.link"
          target="_blank"
        ></Button>
        <Button
          icon="pi pi-download"
          label="Download PDF"
          severity="info"
          rounded
          as="a"
          :href="fetchedArxivEntry?.pdf"
          target="_blank"
        ></Button>
      </div>
    </div>
  </div>
</template>
