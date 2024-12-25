<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js/lib/common'
import DOMPurify from 'dompurify'
import { useToast } from 'primevue/usetoast'

import CommentPanel from '@/components/comment/CommentPanel.vue'
import ClaimPanel from '@/components/pub/ClaimPanel.vue'
import {
  getGithubRepo,
  type GithubRepo,
  addCollection,
  removeCollection,
  getCollections,
  FeedOrigin,
} from '@/services/api'

import { isUrlAbsolute } from '@/utils'
import { useClaim } from '@/services/claim'

const props = defineProps<{
  owner: string
  repo: string
}>()

const { t } = useI18n()

const githubRepository = ref<GithubRepo | null>(null)
const pageTitle = computed(() => {
  if (githubRepository.value) {
    return t('_title', { full_name: githubRepository.value.full_name })
  }
  return t('_fallbackTitle')
})

const collected = ref(false) // 收藏状态
const toast = useToast()

const marked = new Marked(
  markedHighlight({
    emptyLangClass: 'hljs',
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext'
      return hljs.highlight(code, { language }).value
    },
  }),
)

const renderedReadme = computed(() => {
  if (!githubRepository.value?.readme) {
    return ''
  }

  const html = marked.parse(githubRepository.value.readme) as string
  const cleanHtml = DOMPurify.sanitize(html)

  // Add base URL to relative links and images
  const baseUrl = githubRepository.value.html_url
  const div = document.createElement('div')
  div.innerHTML = cleanHtml

  const convertUrl = (url: string, type: string) => {
    if (isUrlAbsolute(url) || url.startsWith('#')) {
      return url
    }
    if (url.startsWith('/')) {
      url = url.slice(1)
    }
    return `${baseUrl}/${type}/main/${url}`
  }

  for (const a of div.querySelectorAll('a[href]')) {
    const href = a.getAttribute('href')!
    a.setAttribute('href', convertUrl(href, 'blob'))
    a.setAttribute('target', '_blank')
    a.setAttribute('rel', 'noopener noreferrer')
  }

  for (const img of div.querySelectorAll('img[src]')) {
    const src = img.getAttribute('src')!
    img.setAttribute('src', convertUrl(src, 'raw'))
    img.setAttribute('loading', 'lazy')
  }

  return div.innerHTML
})

useHead({ title: pageTitle })
// 数据加载逻辑
watchEffect(async () => {
  try {
    const response = await getGithubRepo(props.owner, props.repo)
    githubRepository.value = response.data

    const collectionResponse = await getCollections()
    collected.value = collectionResponse.data.some(
      col =>
        col.item_id === githubRepository.value?.repo_id &&
        col.item_type === 'github',
    )
  } catch (error) {
    console.error(error)
  }
})

// 收藏操作
async function onCollect() {
  if (!githubRepository.value) return

  try {
    if (!collected.value) {
      await addCollection({
        item_type: FeedOrigin.Github,
        item_id: githubRepository.value.repo_id,
      })
      toast.add({
        severity: 'success',
        summary: t('toast.collectionSuccessSummary'),
        detail: t('toast.collectionSuccessDetail'),
        life: 3000,
      })
    } else {
      const collectionResponse = await getCollections()
      const collection = collectionResponse.data.find(
        col =>
          col.item_id === githubRepository.value?.repo_id &&
          col.item_type === 'github',
      )
      if (collection) {
        await removeCollection(collection.id)
        toast.add({
          severity: 'warn',
          summary: t('toast.removeCollectionSuccessSummary'),
          detail: t('toast.removeCollectionSuccessDetail'),
          life: 3000,
        })
      }
    }
    collected.value = !collected.value
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('error.collectionError'),
      life: 3000,
    })
    console.error(error)
  }
}

const { onClaimsUpdated } = useClaim()
</script>

<template>
  <div class="flex justify-center">
    <div class="container mx-auto w-2/3 max-w-[960px] p-4">
      <div class="rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-900">
        <!-- Repository Title -->
        <div class="mb-4 flex items-center">
          <img
            v-if="githubRepository"
            :src="githubRepository.owner.avatar_url"
            alt="Owner Avatar"
            class="mr-3 h-10 w-10 rounded-full"
          />
          <Skeleton v-else width="40px" height="40px" class="rounded-full" />
          <h1 class="ml-3 text-2xl font-bold">
            <a
              v-if="githubRepository"
              :href="githubRepository.html_url"
              target="_blank"
              class="text-blue-500 hover:underline"
            >
              {{ githubRepository.full_name }}
            </a>
            <Skeleton v-else height="2rem" />
          </h1>
          <div class="ml-auto flex items-center gap-4">
            <Button
              v-if="githubRepository?.homepage"
              :label="t('homepage')"
              icon="pi pi-external-link"
              severity="success"
              rounded
              as="a"
              :href="githubRepository.homepage"
              target="_blank"
            ></Button>
            <!-- 锁定/解锁按钮（ToggleButton）显示在最右边 -->
            <Button
              :icon="collected ? 'pi pi-star-fill' : 'pi pi-star'"
              class="h-10 w-12"
              severity="warn"
              @click="onCollect"
            />
          </div>
        </div>

        <!-- Repository Description -->
        <div class="mb-4">
          <p class="mt-2" v-if="githubRepository">
            {{ githubRepository.description }}
          </p>
          <Skeleton v-else height="1rem" class="mt-2" />
        </div>

        <!-- Repository Stats -->
        <div class="mb-4 flex space-x-4" v-if="githubRepository">
          <!-- Repository Stars -->
          <Button
            icon="pi pi-star"
            severity="info"
            variant="text"
            :label="`${githubRepository.stargazers_count} stars`"
          ></Button>

          <!-- Repository Watchers -->
          <Button
            icon="pi pi-eye"
            severity="warn"
            variant="text"
            :label="`${githubRepository.subscribers_count} watching`"
          ></Button>

          <!-- Repository Forks -->
          <Button
            icon="pi pi-share-alt -rotate-90"
            severity="success"
            variant="text"
            :label="`${githubRepository.forks_count} forks`"
          ></Button>
        </div>

        <!-- Repository Topics -->
        <div class="mb-4" v-if="githubRepository?.topics.length">
          <div class="mt-2 flex flex-wrap gap-2">
            <Button
              v-for="topic in githubRepository.topics"
              :key="topic"
              class="px-4 py-2"
              severity="secondary"
            >
              {{ topic }}
            </Button>
          </div>
        </div>

        <!-- README Section -->
        <div class="mt-8" v-if="githubRepository?.readme">
          <div
            v-html="renderedReadme"
            class="prose markdown-body max-w-full"
          ></div>
        </div>
      </div>
    </div>
    <div class="flex w-1/3 flex-col gap-6 p-4">
      <!-- 作者列表：展示认领该文章的作者 -->
      <ClaimPanel
        v-if="githubRepository"
        :origin="FeedOrigin.Github"
        :resource="githubRepository.repo_id"
        @claims-updated="onClaimsUpdated"
      />

      <CommentPanel
        v-if="githubRepository"
        :origin="FeedOrigin.Github"
        :resource="'id' + githubRepository.repo_id"
      />
    </div>
  </div>
</template>

<style>
.markdown-body {
  box-sizing: border-box;
  min-width: 200px;
  max-width: 980px;
  margin: 0 auto;
  padding: 45px;
}

@media (max-width: 767px) {
  .markdown-body {
    padding: 15px;
  }
}
</style>

<i18n locale="zh-CN">
{
  "_title": "{full_name} - @:app.name",
  "_fallbackTitle": "GitHub - @:app.name",
  "homepage": "主页",
  "toast": {
    "collectionSuccessSummary": "收藏成功",
    "collectionSuccessDetail": "您已成功收藏该项目",
    "removeCollectionSuccessSummary": "取消收藏成功",
    "removeCollectionSuccessDetail": "您已取消收藏该项目",
  },
  "error": {
    "collectionError": "收藏操作失败",
  },
}
</i18n>
