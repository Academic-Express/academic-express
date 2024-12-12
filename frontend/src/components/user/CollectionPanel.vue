<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { DataTable, Column } from 'primevue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import {
  getCollections,
  removeCollection,
  type Collection,
} from '@/services/api'
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()

// 动态从 API 加载的收藏列表
const collections = ref<Collection[]>([])

const router = useRouter()
const toast = useToast()

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
    second: '2-digit',
  }
  return new Date(date).toLocaleDateString(undefined, options)
}

// 从 API 加载收藏列表
const loadCollections = async () => {
  loading.value = true
  try {
    const response = await getCollections()
    collections.value = response.data
    console.log('加载的收藏数据:', collections.value)
  } catch (error) {
    console.error('加载收藏列表时出错:', error)
  } finally {
    loading.value = false
  }
}

// 页面加载时，调用 API 加载收藏列表
onMounted(() => {
  loadCollections()
})

// 删除收藏项
const deleteCollection = async (id: number) => {
  try {
    await removeCollection(id)
    collections.value = collections.value.filter(col => col.id !== id)
    console.log('删除收藏成功:', id)
    toast.add({
      severity: 'warn', // 取消提示
      summary: '取消收藏成功',
      detail: '您已取消收藏该项目',
      life: 3000, // 提示持续 3 秒
    })
  } catch (error) {
    console.error('删除收藏项时出错:', error)
  }
}
</script>

<template>
  <div>
    <DataTable
      :value="collections"
      tableStyle="min-width: 50rem"
      :paginator="paginator"
      :rows="rows"
      :loading="loading"
    >
      <!-- 自定义表头 -->
      <template #header>
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span class="text-xl font-bold">{{ t('collections.title') }}</span>
          <Button
            icon="pi pi-refresh"
            rounded
            raised
            @click="loadCollections"
            :label="t('common.refresh')"
          />
        </div>
      </template>

      <!-- 标题列，动态判断 item_type 来展示 title (arXiv) 或 name (GitHub) -->
      <Column :header="t('collections.table.title')">
        <template #body="slotProps">
          <span v-if="slotProps.data.item_type === 'arxiv'">
            {{ slotProps.data.item?.title || '-' }}
          </span>
          <span v-else-if="slotProps.data.item_type === 'github'">
            {{ slotProps.data.item?.name || '-' }}
          </span>
        </template>
      </Column>

      <!-- 作者列，动态显示 arXiv 作者列表或 GitHub 所有者 -->
      <Column :header="t('collections.table.authors')">
        <template #body="slotProps">
          <span v-if="slotProps.data.item_type === 'arxiv'">
            <template
              v-for="(author, i) in slotProps.data.item?.authors || []"
              :key="i"
            >
              {{ author.name
              }}<span v-if="i !== slotProps.data.item.authors.length - 1"
                >,</span
              >
            </template>
          </span>
          <span v-else-if="slotProps.data.item_type === 'github'">
            {{ slotProps.data.item?.owner?.login || '-' }}
          </span>
        </template>
      </Column>

      <!-- 项目类型列 (arxiv 或 github) -->
      <Column :header="t('collections.table.type')">
        <template #body="slotProps">
          {{ slotProps.data.item_type }}
        </template>
      </Column>

      <!-- 链接列，动态渲染 arXiv PDF 链接 或 GitHub URL -->
      <Column :header="t('collections.table.link')">
        <template #body="slotProps">
          <!-- arXiv 链接 -->
          <a
            v-if="slotProps.data.item_type === 'arxiv'"
            :href="slotProps.data.item?.link"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:underline"
          >
            {{ slotProps.data.item_id }}
            <!-- 显示 item_id，而不是 "View" -->
          </a>

          <!-- GitHub 链接 -->
          <a
            v-else-if="slotProps.data.item_type === 'github'"
            :href="slotProps.data.item?.html_url"
            target="_blank"
            rel="noopener noreferrer"
            class="text-blue-500 hover:underline"
          >
            {{ slotProps.data.item?.full_name }}
            <!-- 直接显示仓库的 "octocat/Hello-World" -->
          </a>
        </template>
      </Column>

      <!-- 保存日期列，格式化显示 -->
      <Column :header="t('collections.table.savedDate')">
        <template #body="slotProps">
          {{ formatDate(slotProps.data.created_at) }}
        </template>
      </Column>

      <!-- 操作按钮列 -->
      <Column :header="t('collections.table.actions')">
        <template #body="slotProps">
          <div class="flex flex-nowrap gap-2 text-nowrap">
            <!-- 视图按钮，动态使用 Vue Router 进行页面跳转 -->
            <Button
              :label="t('common.view')"
              icon="pi pi-eye"
              class="p-button-text"
              @click="
                () => {
                  if (slotProps.data.item_type === 'arxiv') {
                    router.push(`/pub/arxiv/${slotProps.data.item_id}`)
                  } else if (slotProps.data.item_type === 'github') {
                    router.push(
                      `/pub/github/${slotProps.data.item?.owner?.login}/${slotProps.data.item?.name}`,
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
              @click="deleteCollection(slotProps.data.id)"
            />
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<i18n locale="zh-CN">
  {
    "collections": {
      "title": "我的收藏",
      "table": {
        "title": "标题",
        "authors": "作者/拥有者",
        "type": "类型",
        "link": "链接",
        "savedDate": "保存时间",
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

<style scoped>
.p-datatable {
  font-size: 14px;
}

.p-button {
  margin: 0.25rem;
}
</style>
