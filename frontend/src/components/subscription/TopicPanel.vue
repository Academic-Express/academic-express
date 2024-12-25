<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { onActivated, ref, watch } from 'vue'

import {
  getTopicSubscriptions,
  subscribeTopic,
  unsubscribeTopic,
  type TopicSubscription,
} from '@/services/api'
import { useBus } from '@/bus'
import { useCustomToast } from '@/services/toast'
import { useUserStore } from '@/stores/user'

const { t } = useI18n()
const bus = useBus()
const toast = useCustomToast()
const userStore = useUserStore()

const followedTopics = ref<TopicSubscription[]>([])
const newTopic = ref<string>('')
const recommendedTopics = ref<string[]>([
  'Large Language Model',
  'Computer Vision',
  'Reinforcement Learning',
])
const hoveredIndex = ref<number>(-1)

function isTopicFollowed(name: string) {
  return followedTopics.value.some(Topic => Topic.topic === name)
}

async function addTopic(topic: string) {
  if (!userStore.user) {
    toast.add({
      severity: 'error',
      summary: t('toast.addError'),
      detail: t('toast.notLoggedIn'),
      life: 5000,
    })
    return
  }

  if (isTopicFollowed(topic)) {
    return
  }

  try {
    const response = await subscribeTopic({
      topic: topic,
    })
    followedTopics.value.push(response.data)
    bus.emit('subscriptionUpdated', 'topic')
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.addError'),
    })
  }
}

async function onAddTopic() {
  await addTopic(newTopic.value)
  newTopic.value = ''
}

async function onRemoveTopic(index: number) {
  if (!userStore.user) {
    toast.add({
      severity: 'error',
      summary: t('toast.removeError'),
      detail: t('toast.notLoggedIn'),
      life: 5000,
    })
    return
  }

  try {
    const removedTopic = followedTopics.value[index]
    await unsubscribeTopic(removedTopic.id)

    followedTopics.value.splice(index, 1)
    bus.emit('subscriptionUpdated', 'topic')
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.removeError'),
    })
  }
}

const fetchTopics = async () => {
  if (!userStore.user) {
    followedTopics.value = []
    return
  }

  try {
    const response = await getTopicSubscriptions()
    followedTopics.value = response.data
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.fetchError'),
    })
  }
}

watch(() => userStore.user, fetchTopics, { immediate: true })

onActivated(fetchTopics)
</script>

<template>
  <div class="space-y-6 p-4">
    <!-- Sub-component 1 -->
    <div class="flex space-x-2">
      <InputText
        v-model="newTopic"
        :placeholder="t('inputBox.placeholder')"
        class="min-w-0 flex-1"
        size="small"
      />
      <Button
        :label="t('inputBox.addButton')"
        icon="pi pi-plus"
        size="small"
        @click="onAddTopic"
      ></Button>
    </div>

    <!-- Sub-component 2 -->
    <div class="space-y-2">
      <h3 class="font-bold">{{ t('recommendedTopics') }}</h3>
      <div class="flex flex-wrap gap-2">
        <template v-for="(topic, index) in recommendedTopics" :key="index">
          <Chip
            v-if="!isTopicFollowed(topic)"
            :label="topic"
            class="cursor-pointer text-sm hover:text-blue-500"
            icon="pi pi-plus"
            @click="addTopic(topic)"
          />
        </template>
      </div>
    </div>

    <!-- Sub-component 3-->
    <div class="space-y-2">
      <template v-if="followedTopics.length === 0">
        <p>{{ t('followed.placeholder') }}</p>
      </template>
      <template v-else>
        <h3 class="font-bold">{{ t('followed.followedTopics') }}</h3>
        <div class="flex flex-wrap gap-2">
          <Chip
            v-for="(topic, index) in followedTopics"
            :key="index"
            :label="topic.topic"
            class="cursor-pointer text-sm hover:text-red-500"
            :icon="hoveredIndex === index ? 'pi pi-times' : 'pi pi-check'"
            @mouseenter="hoveredIndex = index"
            @mouseleave="hoveredIndex = -1"
            @click="onRemoveTopic(index)"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "inputBox": {
    "placeholder": "请输入感兴趣的话题",
    "addButton": "添加"
  },
  "recommendedTopics": "推荐的话题",
  "followed": {
    "followedTopics": "已订阅的话题",
    "placeholder": "暂未订阅任何话题",
  },
  "toast": {
    "addError": "添加订阅话题失败",
    "removeError": "取消订阅话题失败",
    "fetchError": "获取订阅话题失败",
    "notLoggedIn": "登录后才能订阅话题",
  }
}
</i18n>
