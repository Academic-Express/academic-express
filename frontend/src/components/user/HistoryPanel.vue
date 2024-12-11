<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

import ArxivItem from '../feed/ArxivItem.vue'
import GithubItem from '../feed/GithubItem.vue'
import {
  FeedOrigin,
  getHistory,
  removeHistoryItem,
  type History,
} from '@/services/api'

const historyItems = ref<History[]>([])

const { t } = useI18n()

onMounted(async () => {
  try {
    const response = await getHistory()
    historyItems.value = response.data
  } catch (error) {
    console.error(error)
  }
})

const deleteHistoryItem = async (id: number) => {
  try {
    await removeHistoryItem(id)
    historyItems.value = historyItems.value.filter(item => item.id !== id)
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <template v-if="historyItems.length === 0">
    <p>{{ t('historyNotFound') }}</p>
  </template>
  <template v-else>
    <template v-for="(item, index) in historyItems" :key="index">
      <div class="flex flex-wrap">
        <p class="flex items-center">
          {{ new Date(item.viewed_at).toLocaleString() }}
        </p>
        <div class="ml-auto flex items-center">
          <Button
            icon="pi pi-trash"
            variant="text"
            severity="secondary"
            @click="deleteHistoryItem(item.id)"
          ></Button>
        </div>
      </div>

      <ArxivItem
        v-if="item.content_type === FeedOrigin.Arxiv"
        :arxivEntry="item.entry_data"
      />
      <GithubItem
        v-else-if="item.content_type === FeedOrigin.Github"
        :githubRepo="item.entry_data"
      />
    </template>
  </template>
</template>

<i18n locale="zh-CN">
{
  "historyNotFound": "未找到历史记录",  
}
</i18n>
