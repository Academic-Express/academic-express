<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import {
  getScholarSubscriptions,
  subscribeScholar,
  unsubscribeScholar,
  type ScholarSubscription,
} from '@/services/api'

const { t } = useI18n()

const followedScholars = ref<ScholarSubscription[]>([])
const newScholar = ref<string>('')
const recommendedScholars = ref<string[]>([
  'Ilya Sutskever',
  'Jeff Wu',
  'Alec Radford',
  'Jared Kaplan',
  'Dario Amodei',
  'Christopher Olah',
  'Tom B Brown',
])
const hoveredIndex = ref<number>(-1)

function isScholarFollowed(name: string) {
  return followedScholars.value.some(Scholar => Scholar.scholar_name === name)
}

async function addScholar(scholarName: string) {
  if (isScholarFollowed(scholarName)) {
    return
  }

  try {
    const response = await subscribeScholar({
      scholar_name: scholarName,
    })
    followedScholars.value.push(response.data)
  } catch (error) {
    console.error(error)
  }
}

async function onAddScholar() {
  await addScholar(newScholar.value)
  newScholar.value = ''
}

async function onRemoveTopic(index: number) {
  try {
    const removedScholar = followedScholars.value[index]
    await unsubscribeScholar(removedScholar.id)

    followedScholars.value.splice(index, 1)
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  try {
    const response = await getScholarSubscriptions()
    followedScholars.value = response.data
  } catch (error) {
    console.error(error)
  }
})
</script>

<template>
  <div class="container mx-auto">
    <div class="mb-6 flex space-x-2">
      <InputText
        v-model="newScholar"
        :placeholder="t('inputBox')"
        class="min-w-0 max-w-[320px] flex-1"
      />
      <Button
        :label="t('addButton')"
        icon="pi pi-plus"
        :disabled="newScholar.length === 0"
        @click="onAddScholar"
      ></Button>
    </div>

    <div class="mb-4 text-lg">
      <p v-if="followedScholars.length > 0" class="font-bold">
        {{ t('followedScholars') }}
      </p>
      <p v-else>{{ t('placeholder') }}</p>
    </div>
    <div
      v-if="followedScholars.length > 0"
      class="mb-4 mt-4 flex flex-wrap gap-4"
    >
      <Chip
        v-for="(scholar, index) in followedScholars"
        :key="index"
        :label="scholar.scholar_name"
        class="cursor-pointer hover:text-red-500"
        :icon="hoveredIndex === index ? 'pi pi-times' : 'pi pi-check'"
        @mouseenter="hoveredIndex = index"
        @mouseleave="hoveredIndex = -1"
        @click="onRemoveTopic(index)"
      />
    </div>

    <p class="text-lg font-bold">{{ t('recommended') }}</p>
    <div class="mt-4 flex flex-wrap gap-4">
      <template v-for="(scholar, index) in recommendedScholars" :key="index">
        <Chip
          v-if="!isScholarFollowed(scholar)"
          :label="scholar"
          class="cursor-pointer hover:text-blue-500"
          icon="pi pi-plus"
          @click="addScholar(scholar)"
        />
      </template>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "followedScholars": "已关注的学者",
  "addButton": "添加",
  "recommended": "推荐关注学者",
  "placeholder": "暂无关注学者",
  "inputBox": "请输入学者姓名"
}
</i18n>
