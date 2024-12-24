<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useToast } from 'primevue'
import { AxiosError } from 'axios'

import { useUserStore } from '@/stores/user'
import { usePromiseConfirm } from '@/services/confirm'
import {
  type ResourceClaim,
  type FeedOrigin,
  getResourceClaims,
  claimResource,
  unclaimResource,
  type ErrorResponse,
} from '@/services/api'

const props = defineProps<{
  origin: FeedOrigin
  resource: string
}>()

const { t } = useI18n()
const toast = useToast()
const confirm = usePromiseConfirm()
const userStore = useUserStore()

const claims = ref<ResourceClaim[]>([])

watch(
  [() => props.origin, () => props.resource],
  async ([origin, resource]) => {
    try {
      const response = await getResourceClaims(origin, resource)
      claims.value = response.data
    } catch (error) {
      let detail = t('toast.unknownError')
      if (error instanceof AxiosError && error.response?.data) {
        const data = error.response.data as ErrorResponse
        detail = data.detail ?? detail
      }
      console.error('Failed to fetch claims:', error)
      toast.add({
        severity: 'error',
        summary: t('toast.error'),
        detail: detail,
        life: 5000,
      })
    }
  },
  { immediate: true },
)

const claimed = computed(() =>
  claims.value.some(x => x.user.id === userStore.user?.id),
)
const confirmGroup = computed(
  () => `resource-claim-${props.origin}-${props.resource}`,
)

const onClaim = async () => {
  if (!userStore.user) {
    return
  }

  const ret = await confirm.require({
    group: confirmGroup.value,
    header: t('confirm.header'),
    icon: 'pi pi-info-circle',
    acceptLabel: t('confirm.yes'),
    rejectLabel: t('confirm.no'),
    rejectProps: { severity: 'secondary', outlined: true },
  })
  if (!ret) {
    return
  }

  try {
    const response = await claimResource(props.origin, props.resource)
    claims.value.push(response.data)

    toast.add({
      severity: 'success',
      summary: t('toast.claimSuccess'),
      detail: t('toast.claimSuccessDetail'),
      life: 3000,
    })
  } catch (error) {
    let detail = t('toast.unknownError')
    if (error instanceof AxiosError && error.response?.data) {
      const data = error.response.data as ErrorResponse
      detail = data.detail ?? detail
    }
    console.error('Failed to claim resource:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.claimError'),
      detail: detail,
      life: 5000,
    })
  }
}

const onUnclaim = async () => {
  if (!userStore.user) {
    return
  }

  const ret = await confirm.require({
    message: t('confirm.unclaim'),
    header: t('confirm.header'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('confirm.yes'),
    rejectLabel: t('confirm.no'),
    acceptProps: { severity: 'danger' },
    rejectProps: { severity: 'secondary', outlined: true },
  })
  if (!ret) {
    return
  }

  try {
    await unclaimResource(props.origin, props.resource)
    claims.value = claims.value.filter(
      claim => claim.user.id !== userStore.user!.id,
    )

    toast.add({
      severity: 'warn',
      summary: t('toast.unclaimSuccess'),
      detail: t('toast.unclaimSuccessDetail'),
      life: 3000,
    })
  } catch (error) {
    let detail = t('toast.unknownError')
    if (error instanceof AxiosError && error.response?.data) {
      const data = error.response.data as ErrorResponse
      detail = data.detail ?? detail
    }
    console.error('Failed to unclaim resource:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.unClaimError'),
      detail: detail,
      life: 5000,
    })
  }
}
</script>

<template>
  <div
    class="flex flex-col gap-4 rounded-lg bg-surface-0 p-6 shadow-md dark:bg-surface-950"
  >
    <div class="flex items-center">
      <!-- 面板标题 -->
      <h3 class="text-lg font-bold">{{ t('title') }}</h3>

      <!-- 认领按钮 -->
      <Button
        v-if="userStore.user && !claimed"
        icon="pi pi-check"
        :label="t('claim')"
        class="ml-auto h-10 w-32"
        :aria-label="t('claim')"
        @click="onClaim"
      />
    </div>

    <!-- 认领的作者列表 -->
    <ul class="space-y-2">
      <template v-if="claims.length > 0">
        <li
          v-for="{ user } in claims"
          :key="user.id"
          class="flex items-center gap-4"
        >
          <img
            :src="user.avatar"
            alt="Author Avatar"
            class="h-10 w-10 rounded-full shadow"
          />
          <div>
            <p class="font-medium">
              <RouterLink
                :to="{
                  name: 'user-profile',
                  params: { userId: user.id },
                }"
                class="transition-colors hover:text-blue-500 hover:underline"
              >
                {{ user.nickname }}
              </RouterLink>
            </p>
          </div>

          <!-- 如果当前用户是认领作者，则显示认领标识和取消认领按钮 -->
          <Tag
            v-if="user.id === userStore.user?.id"
            :value="t('me')"
            severity="info"
            class="shadow"
          />

          <Button
            v-if="user.id === userStore.user?.id"
            icon="pi pi-times"
            :label="t('unclaim')"
            class="ml-auto h-10 w-32"
            :aria-label="t('unclaim')"
            severity="danger"
            outlined
            @click="onUnclaim"
          />
        </li>
      </template>
      <!-- 当没有认领作者时，显示提示文本 -->
      <template v-else>
        <li class="text-muted-color">
          {{ t('notClaimed') }}
        </li>
      </template>
    </ul>

    <ConfirmDialog :group="confirmGroup">
      <template #message>
        <span class="pi pi-info-circle p-confirmdialog-icon"></span>
        <div>
          <p>{{ t('confirm.claim1') }}</p>
          <ul class="list-inside list-disc">
            <li>{{ t('confirm.claim2') }}</li>
            <li>{{ t('confirm.claim3') }}</li>
            <li>{{ t('confirm.claim4') }}</li>
          </ul>
          <p>{{ t('confirm.claim5') }}</p>
        </div>
      </template>
    </ConfirmDialog>
  </div>
</template>

<i18n locale="zh-CN">
{
  "title": "认领作者",
  "notClaimed": "暂无认领作者",
  "claim": "认领",
  "unclaim": "取消认领",
  "me": "我",
  "toast": {
    "error": "错误",
    "unknownError": "未知错误",
    "claimSuccess": "认领成功",
    "claimSuccessDetail": "您已成功认领该项目",
    "unclaimSuccess": "取消认领成功",
    "unclaimSuccessDetail": "您已取消认领该项目",
    "claimError": "认领失败",
    "unClaimError": "取消认领失败",
  },
  "confirm": {
    "header": "提示",
    "claim1": "您即将认领此项目。",
    "claim2": "该项目将显示在您的个人主页。",
    "claim3": "您在该项目的评论区将以“作者”身份标识参与互动。",
    "claim4": "您可以随时取消认领。",
    "claim5": "请确认是否要认领此项目。",
    "unclaim": "确认取消认领该项目吗？",
    "yes": "确定",
    "no": "取消",
  },
}
</i18n>
