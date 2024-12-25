<script lang="ts" setup>
import { onMounted, ref, computed, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

import ArxivItem from '../feed/ArxivItem.vue'
import GithubItem from '../feed/GithubItem.vue'
import {
  FeedOrigin,
  getHistory,
  removeHistoryItem,
  type History,
} from '@/services/api'

dayjs.extend(relativeTime).locale('zh-cn')

const router = useRouter()

const loading = ref(false)

const historyItems = ref<History[]>([])
const timelineItems = computed(() => {
  // Group history items by viewed_at.
  const groupedItems = historyItems.value.reduce(
    (acc, item) => {
      const viewedAt = dayjs(item.viewed_at).fromNow()
      if (!acc[viewedAt]) {
        acc[viewedAt] = []
      }
      acc[viewedAt].push(item)
      return acc
    },
    {} as Record<string, History[]>,
  )

  groupedItems[''] = []

  // Convert grouped items to timeline items.
  return Object.entries(groupedItems).map(([viewedAt, items]) => ({
    viewed_at: viewedAt,
    items,
  }))
})

const { t } = useI18n()

const fetchHistory = async () => {
  loading.value = true
  try {
    const response = await getHistory()
    historyItems.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchHistory)
onActivated(fetchHistory)

const viewHistoryItem = (item: History) => {
  if (item.content_type === FeedOrigin.Arxiv) {
    router.push({
      name: 'pub-arxiv',
      params: {
        arxivId: item.entry_data.arxiv_id,
        slug: item.entry_data.slug,
      },
    })
  } else if (item.content_type === FeedOrigin.Github) {
    router.push({
      name: 'pub-github',
      params: {
        owner: item.entry_data.owner.login,
        repo: item.entry_data.name,
      },
    })
  }
}

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
  <div class="mb-2 p-4">
    <h3 class="text-xl font-bold">{{ t('history') }}</h3>
  </div>

  <template v-if="loading">
    <div class="space-y-4 p-4">
      <Skeleton v-for="i in 5" :key="i" height="1.5em" />
    </div>
  </template>
  <template v-else-if="historyItems.length === 0">
    <p class="px-4">{{ t('historyNotFound') }}</p>
  </template>
  <template v-else>
    <Timeline class="history" :value="timelineItems" align="left">
      <template #opposite="{ item }">
        <p class="text-right">{{ item.viewed_at }}</p>
      </template>

      <template #content="{ item: { items } }">
        <template v-if="items.length === 0">
          <p class="text-center">{{ t('endOfTimeline') }}</p>
        </template>

        <template v-for="item in items" :key="item.id">
          <div class="flex">
            <div class="mr-4 flex-1">
              <ArxivItem
                v-if="item.content_type === FeedOrigin.Arxiv"
                :arxivEntry="item.entry_data"
              />
              <GithubItem
                v-else-if="item.content_type === FeedOrigin.Github"
                :githubRepo="item.entry_data"
              />
            </div>

            <div class="flex flex-col justify-center">
              <Button
                class="hover:!text-primary"
                icon="pi pi-link"
                variant="text"
                severity="secondary"
                @click="viewHistoryItem(item)"
              ></Button>
              <Button
                class="hover:!text-red-600"
                icon="pi pi-trash"
                variant="text"
                severity="secondary"
                @click="deleteHistoryItem(item.id)"
              ></Button>
              <!-- <Button
                class="hover:!text-blue-600"
                icon="pi pi-star"
                variant="text"
                severity="secondary"
              ></Button> -->
            </div>
          </div>

          <hr class="my-4" />
        </template>
      </template>
    </Timeline>
  </template>
</template>

<style scoped>
.history :deep(.p-timeline-event-opposite) {
  flex: 0;
  min-width: 100px;
}
</style>

<i18n locale="zh-CN">
{
  "history": "历史记录",
  "historyNotFound": "未找到历史记录",
  "endOfTimeline": "没有更多记录了",
}
</i18n>
