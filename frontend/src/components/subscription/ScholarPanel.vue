<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { onMounted, ref } from 'vue'

import {
  getScholarSubscriptions,
  subscribeScholar,
  unsubscribeScholar,
  type ScholarSubscription,
} from '@/services/api'
import { useBus } from '@/bus'
import { useCustomToast } from '@/services/toast'
import { useUserStore } from '@/stores/user'

const { t } = useI18n()
const bus = useBus()
const toast = useCustomToast()
const userStore = useUserStore()

const followedScholars = ref<ScholarSubscription[]>([])
const newScholar = ref<string>('')
const recommendedScholars = ref<string[]>([
  'Geoffrey Hinton',
  'Yoshua Bengio',
  'Yann LeCun',
])
const hoveredIndex = ref<number>(-1)

function isScholarFollowed(name: string) {
  return followedScholars.value.some(scholar => scholar.scholar_name === name)
}

async function addScholar(scholarName: string) {
  if (!userStore.user) {
    toast.add({
      severity: 'error',
      summary: t('toast.addError'),
      detail: t('toast.notLoggedIn'),
      life: 5000,
    })
    return
  }

  if (isScholarFollowed(scholarName)) {
    return
  }

  try {
    const response = await subscribeScholar({
      scholar_name: scholarName,
    })
    followedScholars.value.push(response.data)
    bus.emit('subscriptionUpdated', 'scholar')
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.addError'),
    })
  }
}

async function onAddScholar() {
  await addScholar(newScholar.value)
  newScholar.value = ''
}

async function onRemoveScholar(index: number) {
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
    const removedScholar = followedScholars.value[index]
    await unsubscribeScholar(removedScholar.id)

    followedScholars.value.splice(index, 1)
    bus.emit('subscriptionUpdated', 'scholar')
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.removeError'),
    })
  }
}

onMounted(async () => {
  if (!userStore.user) {
    return
  }

  try {
    const response = await getScholarSubscriptions()
    followedScholars.value = response.data
  } catch (error) {
    toast.reportError(error, {
      summary: t('toast.fetchError'),
    })
  }
})
</script>

<template>
  <div class="space-y-6 p-4">
    <!-- Sub-component 1 -->
    <div class="flex space-x-2">
      <InputText
        v-model="newScholar"
        :placeholder="t('inputBox.placeholder')"
        class="min-w-0 flex-1"
        size="small"
      />
      <Button
        :label="t('inputBox.addButton')"
        icon="pi pi-plus"
        size="small"
        @click="onAddScholar"
      ></Button>
    </div>

    <!-- Sub-component 2 -->
    <div class="space-y-2">
      <h3 class="font-bold">{{ t('recommendedScholars') }}</h3>
      <div class="flex flex-wrap gap-2">
        <template v-for="(scholar, index) in recommendedScholars" :key="index">
          <Chip
            v-if="!isScholarFollowed(scholar)"
            :label="scholar"
            class="cursor-pointer text-sm hover:text-blue-500"
            icon="pi pi-plus"
            @click="addScholar(scholar)"
          />
        </template>
      </div>
    </div>

    <!-- Sub-component 3-->
    <div class="space-y-2">
      <template v-if="followedScholars.length === 0">
        <p>{{ t('followed.placeholder') }}</p>
      </template>
      <template v-else>
        <h3 class="font-bold">{{ t('followed.followedScholars') }}</h3>
        <div class="flex flex-wrap gap-2">
          <Chip
            v-for="(scholar, index) in followedScholars"
            :key="index"
            :label="scholar.scholar_name"
            class="cursor-pointer text-sm hover:text-red-500"
            :icon="hoveredIndex === index ? 'pi pi-times' : 'pi pi-check'"
            @mouseenter="hoveredIndex = index"
            @mouseleave="hoveredIndex = -1"
            @click="onRemoveScholar(index)"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "inputBox": {
    "placeholder": "请输入学者姓名",
    "addButton": "添加"
  },
  "recommendedScholars": "推荐的学者",
  "followed": {
    "placeholder": "暂未关注任何学者",
    "followedScholars" :"已关注的学者",
  },
  "toast": {
    "addError": "关注失败",
    "removeError": "取消关注失败",
    "fetchError": "获取关注学者失败",
    "notLoggedIn": "登录后才能关注学者",
  }
}
</i18n>
