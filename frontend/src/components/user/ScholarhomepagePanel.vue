<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import { DataTable, Column } from 'primevue'
import {
  getUserClaims,
  unclaimResource,
  type UserResourceClaim,
  FeedOrigin,
  type ArxivEntry,
  type GithubRepo,
} from '@/services/api'
import { useUserStore } from '@/stores/user'

const { t } = useI18n()
const router = useRouter()
const userStore = useUserStore()

// 用户认领的资源列表
const claims = ref<UserResourceClaim[]>([])

// 加载状态
const loading = ref(true)

// 分页配置
const paginator = ref(true)
const rows = ref(5)

// 格式化日期的函数
const formatDate = (date: string) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
  return new Date(date).toLocaleDateString(undefined, options)
}

// 加载用户认领的资源
const loadClaims = async () => {
  loading.value = true
  try {
    const currentUserId = userStore.user?.id
    if (!currentUserId) return

    const response = await getUserClaims(currentUserId)
    claims.value = response.data
    console.log('加载的认领资源:', claims.value)
  } catch (error) {
    console.error('加载认领资源时出错:', error)
  } finally {
    loading.value = false
  }
}

// 页面加载时调用
onMounted(() => {
  loadClaims()
})
</script>

<template>
  <div>
    <DataTable
      :value="claims"
      tableStyle="min-width: 50rem"
      :paginator="paginator"
      :rows="rows"
      :loading="loading"
    >
      <!-- 表头 -->
      <template #header>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-xl font-bold">{{ t('claims.title') }}</span>
          <Button
            icon="pi pi-refresh"
            rounded
            raised
            @click="loadClaims"
            :label="t('common.refresh')"
          />
        </div>
      </template>

      <!-- 标题列 -->
      <Column :header="t('claims.table.title')" class="w-80">
        <template #body="slotProps">
          <span v-if="slotProps.data.resource_type === FeedOrigin.Arxiv">
            {{ (slotProps.data.resource as ArxivEntry).title || '-' }}
          </span>
          <span v-else-if="slotProps.data.resource_type === FeedOrigin.Github">
            {{ (slotProps.data.resource as GithubRepo).full_name || '-' }}
          </span>
        </template>
      </Column>

      <!-- 作者列 -->
      <Column :header="t('claims.table.authors')" class="w-80">
        <template #body="slotProps">
          <span v-if="slotProps.data.resource_type === FeedOrigin.Arxiv">
            <template
              v-for="(author, i) in (slotProps.data.resource as ArxivEntry)
                .authors || []"
              :key="i"
            >
              {{ author.name }}
              <span
                v-if="
                  i !==
                  (slotProps.data.resource as ArxivEntry).authors.length - 1
                "
                >,
              </span>
            </template>
          </span>
          <span v-else-if="slotProps.data.resource_type === FeedOrigin.Github">
            {{ (slotProps.data.resource as GithubRepo).owner.login || '-' }}
          </span>
        </template>
      </Column>

      <!-- 链接列 -->
      <Column :header="t('claims.table.link')" class="text-nowrap">
        <template #body="slotProps">
          <!-- arXiv 链接 -->
          <a
            v-if="slotProps.data.resource_type === FeedOrigin.Arxiv"
            :href="(slotProps.data.resource as ArxivEntry).link"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:underline"
          >
            {{ (slotProps.data.resource as ArxivEntry).arxiv_id }}
          </a>
          <!-- GitHub 链接 -->
          <a
            v-else-if="slotProps.data.resource_type === FeedOrigin.Github"
            :href="(slotProps.data.resource as GithubRepo).html_url"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:underline"
          >
            {{ (slotProps.data.resource as GithubRepo).full_name }}
          </a>
        </template>
      </Column>

      <!-- 认领时间列 -->
      <Column :header="t('claims.table.claimedDate')" class="w-60">
        <template #body="slotProps">
          {{ formatDate(slotProps.data.created_at) }}
        </template>
      </Column>

      <!-- 操作列 -->
      <Column :header="t('claims.table.actions')" class="w-40 text-nowrap">
        <template #body="slotProps">
          <Button
            :label="t('common.view')"
            icon="pi pi-eye"
            class="p-button-text"
            @click="
              () => {
                const resource = slotProps.data.resource
                if (slotProps.data.resource_type === FeedOrigin.Arxiv) {
                  router.push(`/pub/arxiv/${resource.arxiv_id}`)
                } else if (slotProps.data.resource_type === FeedOrigin.Github) {
                  router.push(
                    `/pub/github/${resource.owner.login}/${resource.name}`,
                  )
                }
              }
            "
          />
          <!-- 删除按钮 -->
          <Button
            :label="t('common.delete')"
            icon="pi pi-trash"
            class="p-button-danger p-button-text"
            @click="
              async () => {
                if (slotProps.data.resource_type === FeedOrigin.Arxiv) {
                  await unclaimResource(
                    slotProps.data.resource_type,
                    (slotProps.data.resource as ArxivEntry).arxiv_id,
                  )
                } else if (slotProps.data.resource_type === FeedOrigin.Github) {
                  await unclaimResource(
                    slotProps.data.resource_type,
                    (slotProps.data.resource as GithubRepo).repo_id,
                  )
                }
                claims = claims.filter(
                  claim =>
                    !(
                      claim.resource_type === slotProps.data.resource_type &&
                      claim.resource === slotProps.data.resource
                    ),
                )
              }
            "
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<i18n locale="zh-CN">
  {
    "claims": {
      "title": "我的认领资源",
      "table": {
        "title": "标题",
        "authors": "作者",
        "link": "链接",
        "claimedDate": "认领时间",
        "actions": "操作"
      }
    },
    "common": {
      "refresh": "刷新",
      "view": "查看",
      "delete": "删除"
    }
  }
  </i18n>
