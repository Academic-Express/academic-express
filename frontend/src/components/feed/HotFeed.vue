<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import ArxivItem from './ArxivItem.vue'
import GithubItem from './GithubItem.vue'
import { FeedOrigin, getHotFeed, type HotFeed } from '@/services/api'
import { useCustomToast } from '@/services/toast'
import FeedSkeleton from './FeedSkeleton.vue'

const { t } = useI18n()
const toast = useCustomToast()

const loading = ref(false)
const hotFeeds = ref<HotFeed[]>([])

async function fetchHotFeed() {
  loading.value = true
  try {
    const response = await getHotFeed()
    hotFeeds.value = response.data
  } catch (error) {
    toast.reportError(error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchHotFeed)
</script>

<template>
  <template v-for="(feed, index) in hotFeeds" :key="index">
    <ArxivItem
      v-if="feed.origin === FeedOrigin.Arxiv"
      :arxivEntry="feed.item"
    />
    <GithubItem
      v-else-if="feed.origin === FeedOrigin.Github"
      :githubRepo="feed.item"
    />
    <hr class="my-4" />
  </template>

  <FeedSkeleton v-if="loading && hotFeeds.length === 0" />

  <p v-if="!loading" class="text-center text-muted-color">
    {{ hotFeeds.length > 0 ? t('end') : t('empty') }}
  </p>
</template>

<i18n locale="zh-CN">
{
  "empty": "暂无热点追踪",
  "end": "没有更多内容了",
  "toast": {
    "error": "热点追踪加载失败",
  }
}
</i18n>
