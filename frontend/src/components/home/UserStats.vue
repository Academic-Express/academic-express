<script setup lang="ts">
import { onActivated, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

import { useUserStore } from '@/stores/user'
import { type UserStats, getSelfStats } from '@/services/api'
import { useBus } from '@/bus'

const { t } = useI18n()
const userStore = useUserStore()
const bus = useBus()

const STAT_ITEMS = [
  { icon: 'pi pi-tag', key: 'topic_count', label: 'topics' },
  { icon: 'pi pi-user', key: 'scholar_count', label: 'scholars' },
  { icon: 'pi pi-bookmark', key: 'collection_count', label: 'collections' },
  { icon: 'pi pi-check', key: 'claim_count', label: 'claimed' },
  { icon: 'pi pi-comment', key: 'comment_count', label: 'comments' },
  { icon: 'pi pi-history', key: 'history_count', label: 'history' },
] as const

const stats = ref<UserStats | null>(null)

const fetchStats = async () => {
  if (!userStore.user) {
    stats.value = null
    return
  }

  try {
    const response = await getSelfStats()
    stats.value = response.data
  } catch (error) {
    console.error(error)
    stats.value = null
  }
}

watch(
  () => userStore.user,
  () => {
    fetchStats()
  },
  { immediate: true, deep: true },
)

bus.on('subscriptionUpdated', () => {
  fetchStats()
})

onActivated(() => {
  fetchStats()
})
</script>

<template>
  <ul class="grid grid-cols-1 gap-x-4 gap-y-2 xl:grid-cols-2">
    <Chip v-for="item in STAT_ITEMS" :key="item.key">
      <span :class="item.icon"></span>
      <span>{{ t(item.label) }}</span>
      <span class="ml-auto">{{ stats?.[item.key] ?? '--' }}</span>
    </Chip>
  </ul>
</template>

<i18n locale="zh-CN">
{
  "topics": "订阅话题",
  "scholars": "关注学者",
  "collections": "收藏项目",
  "claimed": "认领工作",
  "comments": "发表评论",
  "history": "历史记录",
}
</i18n>
