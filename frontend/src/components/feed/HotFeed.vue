<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ArxivItem from './ArxivItem.vue'
import GithubItem from './GithubItem.vue'
import { FeedOrigin, getHotFeed, type HotFeed } from '@/services/api'

const hotFeeds = ref<HotFeed[]>([])

async function fetchHotFeed() {
  try {
    const response = await getHotFeed()
    hotFeeds.value = response.data
  } catch (error) {
    console.error(error)
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
</template>
