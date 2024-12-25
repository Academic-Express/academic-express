<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import ArxivItem from './ArxivItem.vue'
import { FeedOrigin, getFollowFeed, type FollowFeed } from '@/services/api'
import { useEvent } from '@/bus'
import { useCustomToast } from '@/services/toast'

const { t } = useI18n()
const toast = useCustomToast()

const loading = ref(false)
const followFeeds = ref<FollowFeed[]>([])

async function fetchFollowFeed() {
  loading.value = true
  try {
    const response = await getFollowFeed()
    followFeeds.value = response.data
  } catch (error) {
    toast.reportError(error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchFollowFeed)

useEvent('subscriptionUpdated', async category => {
  if (['scholar', 'institution'].includes(category)) {
    await fetchFollowFeed()
  }
})
</script>

<template>
  <template v-for="(feed, index) in followFeeds" :key="index">
    <div v-if="feed.source.scholar_names?.length" class="mb-4 space-x-4">
      <template v-for="(name, id) in feed.source.scholar_names" :key="id">
        <Tag
          :value="name"
          severity="warn"
          icon="pi pi-user"
          class="shadow"
        ></Tag>
      </template>
    </div>
    <ArxivItem
      v-if="feed.origin === FeedOrigin.Arxiv"
      :arxivEntry="feed.item"
    ></ArxivItem>
    <hr class="my-4" />
  </template>

  <template v-if="loading && followFeeds.length === 0">
    <Skeleton v-for="i in 5" :key="i" class="mb-4" />
  </template>

  <p v-if="!loading" class="text-center text-muted-color">
    {{ followFeeds.length > 0 ? t('end') : t('empty') }}
  </p>
</template>

<i18n locale="zh-CN">
{
  "empty": "暂无关注动态，试试关注一些学者吧",
  "end": "没有更多内容了",
  "toast": {
    "error": "关注动态加载失败",
  }
}
</i18n>
