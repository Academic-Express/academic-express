<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'

import { getArxivEntry, type ArxivEntry } from '@/services/api'

const props = defineProps<{
  arxivId: string
  slug?: string
}>()

const router = useRouter()
const { t } = useI18n()

const arxivEntry = ref<ArxivEntry | null>(null)
const pageTitle = computed(() => {
  if (arxivEntry.value) {
    return t('_title', { title: arxivEntry.value.title })
  }
  return t('_fallbackTitle')
})

const collected = ref(false)

useHead({ title: pageTitle })

watchEffect(async () => {
  try {
    const response = await getArxivEntry(props.arxivId)
    arxivEntry.value = response.data

    if (props.slug !== arxivEntry.value.slug) {
      router.replace({
        name: 'pub-arxiv',
        params: { arxivId: props.arxivId, slug: arxivEntry.value.slug },
      })
    }
  } catch (error) {
    console.error(error)
  }
})

async function onCollect() {
  if (!arxivEntry.value) return
  collected.value = !collected.value
}
</script>

<template>
  <div class="container mx-auto max-w-[960px] p-4">
    <div class="rounded-lg bg-surface-50 p-6 shadow-md dark:bg-surface-950">
      <!-- Title -->
      <h1 class="mb-4 flex items-center justify-between text-2xl font-bold">
        <span v-if="arxivEntry">{{ arxivEntry.title }}</span>
        <Skeleton v-else height="2rem" />

        <!-- 锁定/解锁按钮（ToggleButton）显示在最右边 -->
        <Button
          :icon="collected ? 'pi pi-star-fill' : 'pi pi-star'"
          class="h-10 w-12"
          severity="warn"
          @click="onCollect"
        />
      </h1>

      <!-- Authors -->
      <div class="mb-4">
        <h2 class="text-lg font-bold">{{ t('authors') }}</h2>
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
        <h2 class="text-lg font-bold">{{ t('summary') }}</h2>
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
          <strong>{{ t('published') }}</strong>
          {{ new Date(arxivEntry.published).toLocaleString() }}
        </p>
        <p>
          <strong>{{ t('updated') }}</strong>
          {{ new Date(arxivEntry.updated).toLocaleString() }}
        </p>
      </div>

      <!-- Links -->
      <div class="flex gap-4" v-if="arxivEntry">
        <Button
          icon="pi pi-external-link"
          :label="t('viewOriginal')"
          severity="success"
          rounded
          as="a"
          :href="arxivEntry.link"
          target="_blank"
        ></Button>
        <Button
          icon="pi pi-download"
          :label="t('downloadPdf')"
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

<i18n locale="zh-CN">
{
  "_title": "{title} - @:app.name",
  "_fallbackTitle": "ArXiv 论文 - @:app.name",
  "title": "标题",
  "authors": "作者",
  "summary": "摘要",
  "categories": "类别",
  "published": "发布时间：",
  "updated": "更新时间：",
  "viewOriginal": "查看原文",
  "downloadPdf": "下载 PDF",
}
</i18n>
