<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ArxivItem from './ArxivItem.vue'
import {
  FeedOrigin,
  getSubscriptionFeed,
  type SubscriptionFeed,
} from '@/services/api'

const subscriptionFeeds = ref<SubscriptionFeed[]>([])

onMounted(async () => {
  try {
    const response = await getSubscriptionFeed()
    subscriptionFeeds.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <template v-for="(feed, index) in subscriptionFeeds" :key="index">
    <span v-if="feed.source.topics?.length">
      <template v-for="(topic, id) in feed.source.topics" :key="id">
        <Tag
          :value="topic"
          severity="secondary"
          icon="pi pi-tag"
          class="shadow"
        ></Tag>
      </template>
    </span>
    <ArxivItem
      v-if="feed.origin === FeedOrigin.Arxiv"
      :arxivEntry="feed.item"
    ></ArxivItem>
  </template>
</template>
