<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ArxivItem from '../feed/ArxivItem.vue'
import GithubItem from '../feed/GithubItem.vue'
import {
  FeedOrigin,
  type UserResourceClaim,
  getUserClaims,
} from '@/services/api'
import { useToast } from 'primevue/usetoast'
import { useI18n } from 'vue-i18n'

// i18n 功能初始化
const { t } = useI18n()

// 定义响应式变量，用于存储用户认领的资源
const claims = ref<UserResourceClaim[]>([])

// 获取用户信息的状态管理
const props = defineProps<{
  userId: number
}>()

// 定义 toast，用于提示用户操作结果
const toast = useToast()

// 异步函数，获取当前用户的认领资源数据
async function fetchUserClaims() {
  // 动态获取当前用户 ID
  const currentUserId = props.userId
  if (!currentUserId) {
    // 如果无法获取用户 ID，提示错误信息并返回
    toast.add({
      severity: 'error',
      summary: t('error.noUserIdSummary'),
      detail: t('error.noUserIdDetail'),
      life: 3000,
    })
    return
  }

  try {
    // 调用 API 获取用户认领的资源
    const response = await getUserClaims(currentUserId)
    claims.value = response.data // 将返回的数据保存到响应式变量中
  } catch (error) {
    // 如果获取数据失败，提示用户并打印错误信息
    toast.add({
      severity: 'error',
      summary: t('error.fetchClaimsSummary'),
      detail: t('error.fetchClaimsDetail'),
      life: 3000,
    })
    console.error(error)
  }
}

// 在组件挂载时，调用 fetchUserClaims 获取用户认领数据
onMounted(fetchUserClaims)
</script>

<template>
  <div>
    <!-- 遍历用户认领的资源 -->
    <template v-for="(claim, index) in claims" :key="index">
      <!-- 如果资源类型是 Arxiv，调用 ArxivItem 子组件 -->
      <ArxivItem
        v-if="claim.resource_type === FeedOrigin.Arxiv"
        :arxivEntry="claim.resource"
      />
      <!-- 如果资源类型是 GitHub，调用 GithubItem 子组件 -->
      <GithubItem
        v-else-if="claim.resource_type === FeedOrigin.Github"
        :githubRepo="claim.resource"
      />
      <!-- 分隔线 -->
      <hr class="my-4" />
    </template>

    <!-- 如果没有认领的资源，显示提示信息 -->
    <div v-if="claims.length === 0" class="text-muted mt-4 text-center">
      {{ t('info.noClaims') }}
    </div>
  </div>
</template>

<i18n locale="zh-CN">
{
  "error": {
    "noUserIdSummary": "无法获取用户 ID",
    "noUserIdDetail": "请稍后重试",
    "fetchClaimsSummary": "获取认领数据失败",
    "fetchClaimsDetail": "请检查网络或稍后重试"
  },
  "info": {
    "noClaims": "暂无认领的资源"
  }
}
</i18n>
