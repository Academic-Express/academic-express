<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ArxivItem from './ArxivItem.vue'
import { FeedOrigin, getFollowFeed, type FollowFeed } from '@/services/api'

const followFeeds = ref<FollowFeed[]>([])

onMounted(async () => {
  try {
    const response = await getFollowFeed()
    followFeeds.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <template v-for="(feed, index) in followFeeds" :key="index">
    <span v-if="feed.source.scholar_names?.length">
      <template v-for="(name, id) in feed.source.scholar_names" :key="id">
        <Tag
          :value="name"
          severity="warn"
          icon="pi pi-user"
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
