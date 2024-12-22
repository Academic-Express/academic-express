<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { useToast } from 'primevue/usetoast'

import CommentPanel from '@/components/comment/CommentPanel.vue'
import {
  getArxivEntry,
  type ArxivEntry,
  addCollection,
  removeCollection,
  getCollections,
  FeedOrigin,
  claimResource,
  unclaimResource,
  getResourceClaims,
  type User,
} from '@/services/api'
import { useUserStore } from '@/stores/user'

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

const collected = ref(false) // 收藏状态
const claimed = ref(false) // 认领状态
const toast = useToast()
const userStore = useUserStore()
const claimedAuthors = ref<User[]>([])

useHead({ title: pageTitle })

// 数据加载逻辑
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

    const currentUserId = userStore.user?.id
    if (currentUserId) {
      const collectionResponse = await getCollections()
      collected.value = collectionResponse.data.some(
        col =>
          col.item_id === arxivEntry.value?.arxiv_id &&
          col.item_type === 'arxiv',
      )
    }

    const claimResponse = await getResourceClaims(
      FeedOrigin.Arxiv,
      arxivEntry.value.arxiv_id,
    )

    claimed.value = claimResponse.data.some(
      claim => claim.user.id === currentUserId,
    )
    claimedAuthors.value = claimResponse.data.map(claim => claim.user)
  } catch (error) {
    console.error(error)
  }
})

// 收藏操作
async function onCollect() {
  if (!arxivEntry.value) return

  try {
    if (!collected.value) {
      await addCollection({
        item_type: FeedOrigin.Arxiv,
        item_id: arxivEntry.value.arxiv_id,
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
          col.item_id === arxivEntry.value?.arxiv_id &&
          col.item_type === 'arxiv',
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
  if (!arxivEntry.value) return

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
      await claimResource(FeedOrigin.Arxiv, arxivEntry.value.arxiv_id)
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
        FeedOrigin.Arxiv,
        arxivEntry.value.arxiv_id,
      )
      const claim = claimResponse.data.find(
        clm => clm.user.id === currentUserId,
      )

      if (claim) {
        await unclaimResource(FeedOrigin.Arxiv, claim.resource_id)
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
        // 理论上不会进入这个分支，因为 claimed.value 是 true
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
        <!-- Title -->
        <h1 class="mb-4 flex items-center justify-between text-2xl font-bold">
          <span v-if="arxivEntry">{{ arxivEntry.title }}</span>
          <Skeleton v-else height="2rem" />

          <div class="flex items-center gap-x-2">
            <!-- 收藏按钮 -->
            <Button
              :icon="collected ? 'pi pi-star-fill' : 'pi pi-star'"
              class="h-10 w-12"
              severity="warn"
              @click="onCollect"
            />
          </div>
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
        v-if="arxivEntry"
        :origin="FeedOrigin.Arxiv"
        :resource="arxivEntry.arxiv_id"
      />
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "_title": "{title} - @:app.name",
  "_fallbackTitle": "ArXiv 论文 - @:app.name",
  "title": "标题",
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
    "claimed": "取消认领",
    "unclaimed": "认领",
    "claimButton": "认领按钮"
  },
  "authors": "作者",
  "summary": "摘要",
  "categories": "类别",
  "published": "发布时间：",
  "updated": "更新时间：",
  "viewOriginal": "查看原文",
  "downloadPdf": "下载 PDF",
  "claimedAuthorsTitle": "认领作者",
  "claimedAuthorsPlaceholder": "暂无认领作者,快来认领吧"
}
</i18n>
