<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { Marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import DOMPurify from 'dompurify'
import { useToast } from 'primevue/usetoast'

import CommentPanel from '@/components/comment/CommentPanel.vue'
import {
  getGithubRepo,
  type GithubRepo,
  addCollection,
  removeCollection,
  getCollections,
  FeedOrigin,
  claimResource,
  unclaimResource,
  getResourceClaims,
  type User,
} from '@/services/api'

import { isUrlAbsolute } from '@/utils'
import { useUserStore } from '@/stores/user'

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
const claimed = ref(false) // 认领状态
const toast = useToast()
const userStore = useUserStore()
const claimedAuthors = ref<User[]>([])

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

    const claimResponse = await getResourceClaims(
      FeedOrigin.Github,
      githubRepository.value.repo_id,
    )
    const currentUserId = userStore.user?.id // 动态获取用户 ID
    claimed.value = claimResponse.data.some(
      clm => clm.user.id === currentUserId,
    )

    claimedAuthors.value = claimResponse.data.map(claim => claim.user)
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

// 认领操作
async function onClaim() {
  if (!githubRepository.value) return

  try {
    const currentUserId = userStore.user?.id // 动态获取用户 ID
    if (!currentUserId) {
      toast.add({
        severity: 'error',
        summary: t('error.claimError'),
        detail: t('error.noUserId'),
        life: 3000,
      })
      return
    }

    if (!claimed.value) {
      // 用户未认领，执行认领操作
      await claimResource(FeedOrigin.Github, githubRepository.value.repo_id)
      claimedAuthors.value = [...claimedAuthors.value, userStore.user as User]
      toast.add({
        severity: 'success',
        summary: t('toast.claimSuccessSummary'),
        detail: t('toast.claimSuccessDetail'),
        life: 3000,
      })
    } else {
      // 用户已认领，执行取消认领操作
      const claimResponse = await getResourceClaims(
        FeedOrigin.Github,
        githubRepository.value.repo_id,
      )
      const claim = claimResponse.data.find(
        clm => clm.user.id === currentUserId,
      )

      if (claim) {
        await unclaimResource(FeedOrigin.Github, claim.resource_id)
        claimedAuthors.value = claimedAuthors.value.filter(
          author => author.id !== currentUserId,
        )
        toast.add({
          severity: 'warn',
          summary: t('toast.unclaimSuccessSummary'),
          detail: t('toast.unclaimSuccessDetail'),
          life: 3000,
        })
      } else {
        // 理论上不会进入此分支，因 claimed.value 应与后台数据同步
        toast.add({
          severity: 'error',
          summary: t('error.claimError'),
          detail: t('error.unclaimNotFound'),
          life: 3000,
        })
      }
    }

    // 更新认领状态
    claimed.value = !claimed.value
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: t('error.claimError'),
      life: 3000,
    })
    console.error(error)
  }
}
</script>

<template>
  <div class="flex justify-center">
    <div class="container mx-auto w-2/3 max-w-[960px] p-4">
      <div class="rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950">
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
          <div
            class="ml-auto flex items-center gap-4"
            v-if="githubRepository?.homepage"
          >
            <Button
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
    <div class="w-1/3 p-4">
      <!-- 作者列表：展示认领该文章的作者 -->
      <div
        class="mb-4 flex max-h-[800px] flex-col gap-4 rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950"
      >
        <!-- 面板标题 -->
        <h3 class="mb-4 text-lg font-bold">{{ t('claimedAuthorsTitle') }}</h3>

        <!-- 认领按钮 -->
        <div class="mb-4">
          <Button
            :icon="claimed ? 'pi pi-times' : 'pi pi-check'"
            :label="claimed ? t('toggle.claimed') : t('toggle.unclaimed')"
            class="h-10 w-32 bg-green-500 text-white"
            :aria-label="t('toggle.claimButton')"
            @click="onClaim"
          />
        </div>

        <!-- 认领的作者列表 -->
        <ul class="space-y-2">
          <template v-if="claimedAuthors.length">
            <li
              v-for="author in claimedAuthors"
              :key="author.id"
              class="flex items-center space-x-4"
            >
              <img
                :src="author.avatar"
                alt="Author Avatar"
                class="h-10 w-10 rounded-full shadow"
              />
              <div>
                <p class="font-medium">
                  <RouterLink
                    :to="{
                      name: 'user-profile',
                      params: { userId: author.id },
                    }"
                    class="transition-colors hover:text-blue-500 hover:underline"
                  >
                    {{ author.nickname }}
                  </RouterLink>
                </p>
              </div>
            </li>
          </template>
          <!-- 当没有认领作者时，显示提示文本 -->
          <template v-else>
            <li class="text-muted-color">
              {{ t('claimedAuthorsPlaceholder') }}
            </li>
          </template>
        </ul>
      </div>
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
    "claimSuccessSummary": "认领成功",
    "claimSuccessDetail": "您已成功认领该项目",
    "unclaimSuccessSummary": "取消认领成功",
    "unclaimSuccessDetail": "您已取消认领该项目"
  },
  "error": {
    "collectionError": "收藏操作失败",
    "claimError": "认领操作失败"
  },
  "toggle": {
    "claimed": "认领",
    "unclaimed": "取消认领"
  },
  "claimedAuthorsTitle": "认领作者",
  "claimedAuthorsPlaceholder": "暂无认领作者,快来认领吧"
}
</i18n>
