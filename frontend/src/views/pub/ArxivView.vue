<script setup lang="ts">
import { ref, computed, watchEffect, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useHead } from '@unhead/vue'
import { useToast } from 'primevue/usetoast'
import debounce from 'lodash/debounce'

import CommentPanel from '@/components/comment/CommentPanel.vue'
import {
  getArxivEntry,
  type ArxivEntry,
  addCollection,
  removeCollection,
  getCollections,
  FeedOrigin,
} from '@/services/api'

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
const toast = useToast()

useHead({ title: pageTitle })

watch(
  collected,
  debounce(async (newValue: boolean) => {
    if (!arxivEntry.value) return

    try {
      if (newValue) {
        // 🎉 当 collected 变为 true，调用 addCollection
        console.log('📢 发送的请求数据:', {
          type: FeedOrigin.Arxiv,
          id: arxivEntry.value?.arxiv_id,
        })
        await addCollection({
          item_type: FeedOrigin.Arxiv,
          item_id: arxivEntry.value.arxiv_id,
        })
        toast.add({
          severity: 'success', // 成功提示
          summary: '收藏成功',
          detail: '您已成功收藏该项目',
          life: 3000, // 提示持续 3 秒
        })
        console.log('收藏成功')
      } else {
        // 🎉 当 collected 变为 false，调用 removeCollection
        const collectionResponse = await getCollections()
        const collection = collectionResponse.data.find(
          col =>
            col.item_id === arxivEntry.value?.arxiv_id &&
            col.item_type === 'arxiv',
        )
        if (collection) {
          await removeCollection(collection.id)
          toast.add({
            severity: 'warn', // 取消提示
            summary: '取消收藏成功',
            detail: '您已取消收藏该项目',
            life: 3000, // 提示持续 3 秒
          })
          console.log('取消收藏成功')
        } else {
          console.warn('未找到对应的收藏项，无法取消收藏')
        }
      }
    } catch (error) {
      console.error('收藏操作失败', error)
    }
  }, 500), // ✅ 500ms 的防抖
)

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
    // 获取用户的收藏列表
    const collectionResponse = await getCollections()
    collected.value = collectionResponse.data.some(
      col =>
        col.item_id === arxivEntry.value?.arxiv_id && col.item_type === 'arxiv',
    )
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
  <div class="flex justify-center">
    <div class="container mx-auto w-2/3 max-w-[960px] p-4">
      <div class="rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950">
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
          ></Button>
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
      <CommentPanel />
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
