<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import ArxivItem from './ArxivItem.vue'
import {
  FeedOrigin,
  getSubscriptionFeed,
  type SubscriptionFeed,
} from '@/services/api'
import { useEvent } from '@/bus'
import GithubItem from './GithubItem.vue'
import { useCustomToast } from '@/services/toast'
import FeedSkeleton from './FeedSkeleton.vue'

const { t } = useI18n()
const toast = useCustomToast()

const loading = ref(false)
const subscriptionFeeds = ref<SubscriptionFeed[]>([])

async function fetchSubscriptionFeed() {
  loading.value = true
  try {
    const response = await getSubscriptionFeed()
    subscriptionFeeds.value = response.data
  } catch (error) {
    toast.reportError(error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchSubscriptionFeed)

useEvent('subscriptionUpdated', fetchSubscriptionFeed)
</script>

<template>
  <template v-for="(feed, index) in subscriptionFeeds" :key="index">
    <div v-if="feed.source.topics?.length" class="mb-4 space-x-4">
      <template v-for="(topic, id) in feed.source.topics" :key="id">
        <Tag
          :value="topic"
          severity="info"
          icon="pi pi-tag"
          class="shadow"
        ></Tag>
      </template>
    </div>
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

  <FeedSkeleton v-if="loading && subscriptionFeeds.length === 0" />

  <p v-if="!loading" class="text-center text-muted-color">
    {{ subscriptionFeeds.length > 0 ? t('end') : t('empty') }}
  </p>
</template>

<i18n locale="zh-CN">
{
  "empty": "暂无订阅推荐，试试添加一些订阅话题吧",
  "end": "没有更多内容了",
  "toast": {
    "error": "订阅推荐加载失败",
  },
}
</i18n>
