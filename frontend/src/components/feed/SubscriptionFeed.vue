<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ArxivItem from './ArxivItem.vue'
import {
  FeedOrigin,
  getSubscriptionFeed,
  type SubscriptionFeed,
} from '@/services/api'
import { useEvent } from '@/bus'
import GithubItem from './GithubItem.vue'

const subscriptionFeeds = ref<SubscriptionFeed[]>([])

async function fetchSubscriptionFeed() {
  try {
    const response = await getSubscriptionFeed()
    subscriptionFeeds.value = response.data
  } catch (error) {
    console.error(error)
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
</template>
