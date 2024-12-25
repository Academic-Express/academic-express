<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import debounce from 'lodash/debounce'

import ArxivItem from './ArxivItem.vue'
import GithubItem from './GithubItem.vue'
import {
  FeedOrigin,
  getSearchResult as getSearchResults,
  type HotFeed,
} from '@/services/api'
import { useCustomToast } from '@/services/toast'
import FeedSkeleton from './FeedSkeleton.vue'

const props = defineProps<{
  searchText: string
}>()

const { t } = useI18n()
const toast = useCustomToast()

const loading = ref(false)
const searchResults = ref<HotFeed[] | null>(null)

const fetchResults = debounce(async searchText => {
  try {
    const response = await getSearchResults(searchText)
    searchResults.value = response.data
  } catch (error) {
    toast.reportError(error)
  } finally {
    loading.value = false
  }
}, 250)

watch(
  () => props.searchText,
  searchText => {
    if (searchText) {
      loading.value = true
      if (searchResults.value && searchResults.value.length === 0) {
        searchResults.value = null
      }
      fetchResults(searchText)
    } else {
      fetchResults.cancel()
      loading.value = false
      searchResults.value = null
    }
  },
  { immediate: true },
)
</script>

<template>
  <Transition>
    <div
      v-if="searchResults && loading"
      class="mask absolute bottom-0 left-0 right-0 top-0 z-10 bg-black bg-opacity-20 dark:bg-opacity-60"
    ></div>
  </Transition>

  <template v-if="searchResults">
    <template v-for="(feed, index) in searchResults" :key="index">
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

    <p class="text-center text-muted-color">
      {{ searchResults.length > 0 ? t('end') : t('empty') }}
    </p>
  </template>

  <template v-else>
    <FeedSkeleton v-if="loading" />

    <p v-else class="text-center text-muted-color">
      {{ t('placeholder') }}
    </p>
  </template>
</template>

<style scoped>
.mask.v-enter-active,
.mask.v-leave-active {
  transition: opacity 0.3s;
}

.mask.v-enter-from,
.mask.v-leave-to {
  opacity: 0;
}
</style>

<i18n locale="zh-CN">
{
  "placeholder": "输入关键词，搜索相关内容",
  "empty": "没有找到相关内容",
  "end": "没有更多内容了",
  "toast": {
    "error": "搜索失败，请稍后重试",
  }
}
</i18n>
