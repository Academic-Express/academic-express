<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  getTopicSubscriptions,
  subscribeTopic,
  unsubscribeTopic,
  type TopicSubscription,
} from '@/services/api'

const { t } = useI18n()

const followedTopics = ref<TopicSubscription[]>([])
const newTopic = ref<string>('')
const recommendedTopics = ref<string[]>([
  'Large Language Model',
  'Computer Vision',
  'Reinforcement Learning',
  'Pre-Training',
  'RLHF',
  'Fine-Tuning',
  'In-Context Learning',
  'CoT',
  'Multi-Agent',
  'Multi-Step Reasoning',
])
const hoveredIndex = ref<number>(-1)

function isTopicFollowed(name: string) {
  return followedTopics.value.some(Topic => Topic.topic === name)
}

async function addTopic(topic: string) {
  if (isTopicFollowed(topic)) {
    return
  }

  try {
    const response = await subscribeTopic({
      topic: topic,
    })
    followedTopics.value.push(response.data)
  } catch (error) {
    console.error(error)
  }
}

async function onAddTopic() {
  await addTopic(newTopic.value)
  newTopic.value = ''
}

async function onRemoveTopic(index: number) {
  try {
    const removedTopic = followedTopics.value[index]
    await unsubscribeTopic(removedTopic.id)

    followedTopics.value.splice(index, 1)
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  try {
    const response = await getTopicSubscriptions()
    followedTopics.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <div class="container mx-auto">
    <div class="mb-6 flex space-x-2">
      <InputText
        v-model="newTopic"
        :placeholder="t('inputBox')"
        class="min-w-0 max-w-[320px] flex-1"
      />
      <Button
        :label="t('addButton')"
        icon="pi pi-plus"
        @click="onAddTopic"
      ></Button>
    </div>

    <div class="mb-4 text-lg">
      <p v-if="followedTopics.length > 0" class="font-bold">
        {{ t('followedTopics') }}
      </p>
      <p v-else>{{ t('placeholder') }}</p>
    </div>
    <div
      v-if="followedTopics.length > 0"
      class="mb-4 mt-4 flex flex-wrap gap-4"
    >
      <Chip
        v-for="(topic, index) in followedTopics"
        :key="index"
        :label="topic.topic"
        class="cursor-pointer hover:text-red-500"
        :icon="hoveredIndex === index ? 'pi pi-times' : 'pi pi-check'"
        @mouseenter="hoveredIndex = index"
        @mouseleave="hoveredIndex = -1"
        @click="onRemoveTopic(index)"
      />
    </div>

    <p class="text-lg font-bold">{{ t('recommended') }}</p>
    <div class="mt-4 flex flex-wrap gap-4">
      <template v-for="(topic, index) in recommendedTopics" :key="index">
        <Chip
          v-if="!isTopicFollowed(topic)"
          :label="topic"
          class="cursor-pointer hover:text-blue-500"
          icon="pi pi-plus"
          @click="addTopic(topic)"
        />
      </template>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
    "followedTopics": "已订阅的话题",
    "addButton": "添加",
    "recommended": "推荐订阅话题",
    "placeholder": "暂无订阅话题",
    "inputBox": "请输入话题"
}
</i18n>
